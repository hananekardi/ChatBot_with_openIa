# -*- coding: utf-8 -*-
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader
import os
import nltk
from flask import Flask, render_template,jsonify,request
from flask_cors import CORS
import requests
from dotenv.main import load_dotenv
import openai


#chargement de fichiers à partir d'un répertoire spécifié
loader = DirectoryLoader('path_to_fichiers_PDF', glob='*.pdf')
documents = loader.load()
#permet de charger les fichiers du répertoire spécifié


text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
#crée un découpeur de texte 
#prend une liste de documents (dans ce cas, des fichiers PDF) et les divise en morceaux de texte plus petits 
texts = text_splitter.split_documents(documents)
print(texts)

openai_api_key= "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"
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
#représentations vectorielles de texte en utilisant le modèle GPT-3 de OpenAI.
docsearch = FAISS.from_documents(texts, embeddings)
# construire un index pour effectuer des recherches plus rapides et plus efficaces sur les documents textuels.



docsearch = FAISS.from_documents(texts, embeddings)
# construire un index pour effectuer des recherches plus rapides et plus efficaces sur les documents textuels.



llm = OpenAI(openai_api_key=openai_api_key)
#creation d'une instance de OpenAI qui va permettra d'utiliser le modèle de langage pour effectuer des tâches de génération de texte, de recherche d'informations

qa1 = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())
#instance de RetrievalQA  est prête à être utilisée pour effectuer des tâches de question-réponse en utilisant le modèle de langage de llm et en récupérant les documents pertinents à l'aide du retriever docsearch.


app = Flask(__name__)
CORS(app)

load_dotenv()
API = os.environ['API']

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/data', methods=['POST'])
def get_data():
    
    data = request.get_json()
    text=data.get('data')
    openai.api_key = API
    
    user_input = text
    print(user_input)
    try:
        query0 = "Vous êtes une experte en extraction des questions posées par les utilisateurs dans le contexte des emails.Votre objectif est de fournir des réponses aux questions posées par les utilisateurs dans des emails.Appuyez-vous fortement sur le contenu des extraits de textes pour garantir l'exactitude et l'authenticité de vos réponses. Sachez que les informations contenues dans les textes peuvent ne pas toujours être pertinentes pour la requête. Analysez attentivement chacun d'eux pour déterminer si le contenu est pertinent avant de les utiliser pour construire votre réponse.ne fournissez pas d'informations qui ne sont pas prises en charge par le contenu des fichiers textes."
        # Contenus des messages utilisateur
        query = user_input
        info =  qa1.run(user_input)
        # Fonction pour obtenir la réponse complète
        def get_full_response(query, info):
            system_message = "Vous êtes un expert en repondre aux emails de manier professionnel , reconnu pour votre expertise dans l'aide à la rédaction de réponses aux emails.Votre objectif est de fournir des réponses utiles et concises aux emails. Vos réponses doivent être ciblées et directes. Évitez les phrases trop embellies - les utilisateurs s'attendent à ce que vous soyez franc et honnête. N'inventez pas d'informations ou ne fournissez pas de données qui ne sont pas étayées par les informations fournies dans la requête de l'utilisateur.  "
            messages = [
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": query0
                },
        
               {
                    "role": "user",
                    "content": query
               },
               {
                    "role": "user",
                    "content": info
                }
    ]

            # Appeler le modèle pour la première partie de la réponse
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=messages,
                temperature=0,
                max_tokens=10385,  # Utiliser la limite maximale de jetons
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            response_text = response['choices'][0]['message']['content']

            # Vérifier si la réponse est incomplète et continuer l'appel jusqu'à obtenir la réponse complète
            while response['choices'][0]['finish_reason'] != 'stop':
                last_token_id = response['choices'][0]['message']['total_tokens']
                messages[-1]['content'] = query[last_token_id:]
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=messages,
                    temperature=0,
                    max_tokens=10385,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                response_text += response['choices'][0]['message']['content']
    
            return response_text

        # Appeler la fonction pour obtenir la réponse complète
        full_response = get_full_response(query, info)
        print(full_response)
        return jsonify({"response":True,"message":full_response})
    except Exception as e:
        print(e)
        error_message = f'Error: {str(e)}'
        return jsonify({"message":error_message,"response":False})

    

if __name__ == '__main__':
    app.run()

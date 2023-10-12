# Utilisez une image Python officielle en tant qu'image de base
FROM python:3.9.12

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le contenu de votre répertoire actuel (le code de votre chatbot) dans le conteneur
COPY . /app

RUN python -m pip install --upgrade pip

# Installez les dépendances de votre application
RUN pip install -r requirements.txt  

# Exposez le port sur lequel votre application Flask écoute
EXPOSE 5000

# Démarrez votre application Flask lorsque le conteneur est lancé
CMD ["python", "main.py"]  

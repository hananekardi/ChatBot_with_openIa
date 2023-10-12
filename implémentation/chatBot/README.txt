If you do not want to use a virtual environment:

Navigate to your project directory using the cd command:
cd chatBot

Install the required dependencies using pip with the requirements.txt file:
pip install -r requirements.txt

Set up the OpenAI API by creating an OpenAI account and obtaining an API key. Then, set the OPENAI_API_KEY environment variable in the main.py file by replacing "YOUR_API_KEY" with your actual API key.

Run the application using the python command:
python main.py

Open your web browser and visit http://127.0.0.1:{port}/ to access the chatbot.

If you want to run in a virtual environment:

Create a virtual environment using the python -m venv command:
python -m venv chatbot_venv

Activate the virtual environment using the appropriate command:
chatbot_venv\Scripts\activate

Install the required dependencies within the virtual environment using pip with the requirements.txt file:
pip install -r requirements.txt

Set up the OpenAI API as described earlier.

Run the application using the python command:
python main.py

If you want to run it with Docker:

Follow these steps to run the application using Docker:

1. Create a Docker image with the following command:
docker build -t docker_image_name .


2. Create a Docker container with the following command:
docker run -p 5000:5000 --name docker_container_name docker_image_name 



version python: 3.9.12
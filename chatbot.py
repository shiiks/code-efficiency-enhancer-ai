import os
import json
import openai
import re
import base64
import requests
import traceback
from flask import Flask, request, Response
from flask_restful import Resource, Api
import logging
from dotenv import load_dotenv

app = Flask(__name__)
api = Api(app)
logging.basicConfig(filename=os.path.join(os.getenv('LOG_PATH'), os.getenv('LOG_FILE')), level=os.getenv('LOG_LEVEL'), filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

@app.before_request
def before_request():
    """
    Performs tasks before an incoming HTTP request is handled.

    Increments the incoming request counter if the request is not for the /metrics path. Then it makes sure the
    client's token is authorised to access this service.

    :return: if Authorisation fails returns response with Unauthorised build notification request - 401 else Nothing.
    """
    if re.match('/webhook', request.path):
        try:
            token = os.getenv('CHATBOT_TOKEN')
            authorisation_token = request.headers['Authorization']
            if token == authorisation_token:
                logging.info("Authenticated.")
            else:
                raise ValueError("Unauthorized request")
        except (KeyError, ValueError, TypeError) as error:
            response = {"ERROR": "Unauthorised - The sender is not authenticated."}
            logging.error(response)
            logging.error(error)
            return Response(response=json.dumps(response), status=401, mimetype='application/json')
        
        
class ChatBot:
    """
    A Chatbot class to manage conversation and API interactions.
    """
    def __init__(self):
        """
        Initializes the ChatBot object with the necessary credentials
        and establishes the initial chat context.
        """
        load_dotenv()
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.azure_endpoint = os.getenv('AZURE_ENDPOINT')
        self.api_version = os.getenv('API_VERSION')
        self.gpt_model = os.getenv('GPT_MODEL')
        self.appkey = os.getenv('APP_KEY')
        self.webex_message_url = os.getenv('WEBEX_MESSAGE_URL')
        self.webex_bot_access_token = os.getenv('WEBEX_BOT_ACCESS_TOKEN')
        self.user = f'{{"appkey": "{self.appkey}"}}'
        self.encoded_value = self.encode_credentials()
        self.token = self.get_token()
        self.client = self.create_client()
        self.file_path = os.getenv('PROMPT_FILE')
        with open(self.file_path, 'r') as file:
            content = file.read()
        self.messages = [
            { 
                "role": "system", 
                "content": content
            }
        ]

    def encode_credentials(self):
        """
        Encodes the client credentials in base64 format.
        return: The encoded credentials.
        """
        credentials = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    def get_token(self):
        """
        Gets the OAuth token using the encoded credentials.
        return: The OAuth token.
        """
        url = os.getenv('OAUTH_URL')
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {self.encoded_value}"
        }
        data = {
            "grant_type": "client_credentials"
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            return response.text

    def create_client(self):
        """
        Creates an OpenAI client using the OAuth token.
        return: AzureOpenAI: The OpenAI client.
        """
        return openai.AzureOpenAI(
            azure_endpoint = self.azure_endpoint, 
            api_key = f"{self.token}",  
            api_version = self.api_version
        )

    def chat(self, user_message):
        """
        Manages the chatbot conversation, processes user input, 
        and handles any exceptions.
        :param: user_message: A string containing the user's message.
        """
        self.messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )
        try:
            response = self.client.chat.completions.create(
                model = self.gpt_model,
                messages = self.messages,
                user = self.user
            )
            chatbot_response = response.choices[0].message.content
            logging.info(f"GreenCode Optimizer: {chatbot_response}")
            return chatbot_response
        except Exception as exception:
            logging.error(exception)
            logging.error(traceback.format_exc())
            return str(traceback.format_exc())
                
    def send_message(self, message, room_id=None, person_id=None):
        """
        Sends a message to a Webex Teams space or to a specific person.

        This function allows sending a message either to a room (group space) or directly to an individual, 
        depending on whether the 'room_id' or 'person_id' parameter is provided. At least one of these 
        must be specified, and the message will be sent to the corresponding recipient.

        :param message: A string containing the message to be sent.
        :param room_id: Optional; A string representing the ID of the Webex Teams room (group space) to which the message is sent.
        :param person_id: Optional; A string representing the ID of the person to whom the message is sent directly.
        :return: The response from the Webex Teams API as a dictionary.

        :raises ValueError: If neither 'room_id' nor 'person_id' is provided.
        """
        headers = {
        'Authorization': f'Bearer {self.webex_bot_access_token}',
        'Content-Type': 'application/json'
        }
        data = {
            'text': message
        }
        if room_id:
            data['roomId'] = room_id
        elif person_id:
            data['toPersonId'] = person_id
        else:
            logging.error("Either room_id or person_id must be provided to send a message.")
            raise ValueError("Either room_id or person_id must be provided to send a message.")
        
        try:
            response = requests.post(self.webex_message_url, headers=headers, json=data)
            if response.status_code != 200:
                logging.error(f"Failed to send message: {response.text}")
                response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exception:
            logging.error(f"An error occurred while trying to send the message: {exception}")
            raise
    
    def reset_conversation(self):
        """
        Resets the conversation state to start fresh.
        """
        self.messages = [
            { 
                "role": "system", 
                "content": "You are a Cisco Collaboration Localisation and Internationalsation Bot." 
            }
        ]
        logging.info("Conversation has been reset.")


class Webhook(Resource):
    def __init__(self):
        """
        Initializes the ChatBot object with the necessary credentials
        and establishes the initial chat context.
        """
        load_dotenv()
        self.webex_message_url = os.getenv('WEBEX_MESSAGE_URL')
        self.webex_bot_access_token = os.getenv('WEBEX_BOT_ACCESS_TOKEN')
        
    def get_message_details(self, message_id, bearer_token):
        """
        Retrieves the details of a specific message from Webex Teams using the message ID.

        This function sends an HTTP GET request to the Webex Teams API to retrieve information
        about a message, such as the message text and the sender's information.

        :param: message_id: A string representing the unique ID of the message to retrieve details for.
        :param: bearer_token: A string representing the bearer token for authorization.
        :return: A dictionary containing the details of the message.

        :raises requests.exceptions.RequestException: If there is an error during the HTTP request.
        """
        url = f"{self.webex_message_url}/{message_id}"
        headers = {
            "Authorization": f"Bearer {bearer_token}"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exception:
            logging.error(f"An error occurred while trying to retrieve message details: {exception}")
            raise
    
    def post(self):
        """
        Handles POST requests from Webex Teams. If the bot is mentioned 
        in a message, it will process the message and respond.
        return: A Flask response object with a JSON payload indicating success or failure.
        """
        try:
            data = request.form
            message_id = data['messageId']
            message_details = self.get_message_details(message_id, self.webex_bot_access_token)
            message_text = message_details.get('text', '')
            sender = data['personId']
            room_type = data['roomType']
            room_id = data['roomId']
            person_email = data['personEmail']
            bot_name = os.getenv('BOT_NAME')
            bot_email = os.getenv('WEBEX_BOT_EMAIL')
            pattern = None
            
            if person_email == bot_email:
                logging.info('Its a message from the bot itself; do not process')
                return Response(response=json.dumps({'message': 'Its a message from the bot itself; do not process'}), status=200, mimetype='application/json')
            
            if room_type == "group":
                pattern = re.compile(re.escape(bot_name), re.IGNORECASE)
                if not pattern.search(message_text):
                    logging.info('Bot not mentioned, ignoring message.')
                    return Response(response=json.dumps({'message': 'Bot not mentioned, ignoring message.'}), status=200, mimetype='application/json')

            if pattern:
                user_message = pattern.sub('', message_text).strip()
            else:
                user_message = message_text.strip()
                
            chat_bot = ChatBot()
            
            if user_message.lower() in ["reset", "refresh"]:
                chat_bot.reset_conversation()
                reset_message = "The conversation has been reset. How may I assist you now?"
                chat_bot.send_message(reset_message, room_id=room_id if room_type == 'group' else None, person_id=sender if room_type != 'group' else None)
                return Response(response=json.dumps({'status': 'conversation reset'}), status=200, mimetype='application/json')
            
            bot_response = chat_bot.chat(user_message)
            if bot_response:
                if room_type == 'group':
                    chat_bot.send_message(bot_response, room_id=room_id)
                else:
                    chat_bot.send_message(bot_response, person_id=sender)
            else:
                error_message = "Error generating bot response. Please try again after some time."
                if room_type == 'group':
                    chat_bot.send_message(error_message, room_id=room_id)
                else:
                    chat_bot.send_message(error_message, person_id=sender)
            return Response(response=json.dumps({'status': 'success'}), status=200, mimetype='application/json')
        except Exception as exception:
            logging.error(str(exception))
            logging.error(traceback.format_exc())
            return Response(response=json.dumps({'status': 'error', 'message': str(exception)}), status=500, mimetype='application/json')

api.add_resource(Webhook, '/webhook')

if __name__ == "__main__":
    app.config['SERVER_NAME'] = os.environ['CHATBOT']
    app.run(debug=os.environ['CHATBOT_DEBUG'])
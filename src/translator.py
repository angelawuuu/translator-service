import vertexai
import os
from google.oauth2 import service_account
from typing import Callable
from vertexai.language_models import ChatModel, InputOutputTextPair
from hashlib import sha256


if os.environ.get('PRIVATE_KEY') != None and os.environ.get('PRIVATE_KEY_ID') != None:
  PROJECT_ID = "nodebb-416919"
  os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID

  from google.cloud import aiplatform
  print(sha256(os.environ['PRIVATE_KEY_ID'].encode('utf-8')).hexdigest())
  print(sha256(os.environ['PRIVATE_KEY'].encode('utf-8')).hexdigest())

  credentials = service_account.Credentials.from_service_account_info(
      {
    "type": "service_account",
    "project_id": "nodebb-416919",
    "private_key_id": str(os.environ['PRIVATE_KEY_ID']),
    "private_key": str(os.environ['PRIVATE_KEY']),
    "client_email": "nodebb-416919@appspot.gserviceaccount.com",
    "client_id": "112346569395498662874",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/nodebb-416919%40appspot.gserviceaccount.com",
    "universe_domain": "googleapis.com"
  }
  )

  aiplatform.init(
      # your Google Cloud Project ID or number
      # environment default used is not set
      project=PROJECT_ID,

      # the Vertex AI region you will use
      # defaults to us-central1
      location='us-central1',
      credentials=credentials
  )

chat_model = ChatModel.from_pretrained("chat-bison@001")

def get_translation(post: str) -> str:
    context = "You are a highly-skilled translator specializing in translating languages to English. You answer truthfully, concisely, and carefully. Translate the following statement to English, do not provide a response with anything other than the English translation.:"
    # ----------------- DO NOT MODIFY ------------------ #

    parameters = {
        "temperature": 0.7,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
    }

     # ---------------- YOUR CODE HERE ---------------- #
    chat = chat_model.start_chat(context=context)
    response = chat.send_message(post, **parameters)
    return response.text

def get_language(post: str) -> str:
    # ----------------- DO NOT MODIFY ------------------ #
    context = "You are a highly trained linguist, able to classify English and non-English text, including various English dialects. Please analyze the following text and determine its language. Respond in one word, the name of the lanugage." # TODO: Insert context
    parameters = {
        "temperature": 0.7,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
    }

     # ---------------- YOUR CODE HERE ---------------- #
    chat = chat_model.start_chat(context=context)
    response = chat.send_message(post, **parameters)
    return response.text

def is_harmful(post: str) -> str:
    context = "Determine whether the following text contains potentially harmful or negative content. Reply with Yes or No."
    parameters = {
        "temperature": 0.7,
        "max_output_tokens": 256,
    }

    chat = chat_model.start_chat(context = context)
    response = chat.send_message(post, **parameters)
    return (response.text == "Yes")  

def translate_content(post: str) -> tuple[bool, str]:
  try:
    language = get_language(post)
    if (language == "English") :
      return (True, post)
    else :
      translation = get_translation(post)
      if ("language model" in translation) or (not translation) or "I don't understand your request" == translation or "Translation does not make sense." == translation:
        return (False, "NodeBB was unable to translate this post\n\n" + post)
      elif is_harmful(translation) or "Dangerous input." == translation:
        return (False, "The translation for this post may contain harmful content. This could due to a translation error.\n\n" + translation)
      return (False, translation)
  except Exception as e:
    return (False, "NodeBB was unable to translate this post\n\n" + post)
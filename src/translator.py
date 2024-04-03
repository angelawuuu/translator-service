import vertexai
import os

from typing import Callable

PROJECT_ID = "nodebb-416919"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID

from google.colab import auth
from google.cloud import aiplatform

auth.authenticate_user()

aiplatform.init(
    # your Google Cloud Project ID or number
    # environment default used is not set
    project=PROJECT_ID,

    # the Vertex AI region you will use
    # defaults to us-central1
    location='us-central1',
)

from vertexai.language_models import ChatModel, InputOutputTextPair

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

def translate_content(content: str) -> tuple[bool, str]:
    language = get_language(post)
    if (language == "English") :
      return (True, post)
    else :
      translation = get_translation(post)
      if "language model" in translation:
        return (False, "NodeBB was unable to translate this post\n\n" + post)
      if is_harmful(translation):
        return (False, "The translation for this post may contain harmful content. This could due to a translation error.\n\n" + translation)
      return (False, "The following post has been translated from " + language + "\n\n" + translation)

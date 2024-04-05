from src.translator import translate_content
import vertexai
from mock import patch

@patch('vertexai.language_models.ChatSession.send_message')
def test_unexpected_language(mocker):
  # we mock the model's response to return a random message
  mocker.return_value.text = "I don't understand your request"

  # TODO assert the expected behavior
  response_eng, response_trans = translate_content("Aquí está su primer ejemplo.")
  assert not response_eng
  assert "NodeBB was unable to translate this post" in response_trans

@patch('vertexai.language_models.ChatSession.send_message')
def test_unexpected_input(mocker):
  # we mock the model's response to return a random message
  mocker.return_value.text = "Translation does not make sense."

  # TODO assert the expected behavior
  response_eng, response_trans = translate_content("😊😊")
  assert "NodeBB was unable to translate this post" in response_trans

@patch('vertexai.language_models.ChatSession.send_message')
def test_dangerous_input(mocker):
  # we mock the model's response to return a random message
  mocker.return_value.text = "Dangerous input."

  # TODO assert the expected behavior
  response_eng, response_trans = translate_content("mata los gérmenes")
  assert not response_eng
  assert "The translation for this post may contain harmful content" in response_trans

@patch('vertexai.language_models.ChatSession.send_message')
def test_empty_input(mocker):
  # we mock the model's response to return a random message
  mocker.return_value.text = ""

  # TODO assert the expected behavior
  response_eng, response_trans = translate_content("What's the weather?")
  assert not response_eng
  assert "NodeBB was unable to translate this post" in response_trans
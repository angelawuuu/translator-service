from src.translator import translate_content
import vertexai
from mock import patch

def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

@patch('vertexai.language_models.ChatSession.send_message')
def test_unexpected_language(mocker):
  # we mock the model's response to return a random message
  mocker.return_value.text = "I don't understand your request"

  # TODO assert the expected behavior
  content = "Aquí está su primer ejemplo."
  response_eng, response_trans = translate_content(content)
  assert response_eng
  assert response_trans == content

@patch('vertexai.language_models.ChatSession.send_message')
def test_unexpected_input(mocker):
  # we mock the model's response to return a random message
  mocker.return_value.text = "Translation does not make sense."

  # TODO assert the expected behavior
  content = "😊😊"
  response_eng, response_trans = translate_content(content)
  assert response_eng
  assert response_trans == content

@patch('vertexai.language_models.ChatSession.send_message')
def test_dangerous_input(mocker):
  # we mock the model's response to return a random message
  mocker.return_value.text = "Dangerous input."

  # TODO assert the expected behavior
  content = "mata los gérmenes"
  response_eng, response_trans = translate_content(content)
  assert response_eng
  assert response_trans == content

@patch('vertexai.language_models.ChatSession.send_message')
def test_empty_input(mocker):
  # we mock the model's response to return a random message
  mocker.return_value.text = ""

  # TODO assert the expected behavior
  content = "What's the weather?"
  response_eng, response_trans = translate_content(content)
  assert response_eng
  assert response_trans == content
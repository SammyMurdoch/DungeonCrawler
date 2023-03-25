import os
import openai

with open("OpenAIAPIKey") as f:
    key = f.read()

openai.organization = "org-4XGM030xSxlU7dUaOFF2DXX8"
openai.api_key = os.getenv(key)

openai.Model.list()


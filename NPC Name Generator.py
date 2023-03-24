import os
import openai

openai.organization = "org-4XGM030xSxlU7dUaOFF2DXX8"
openai.api_key = os.getenv("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")

openai.Model.list()


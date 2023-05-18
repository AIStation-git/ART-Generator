import requests
import os

api_host = os.getenv('API_HOST')
api_key = os.getenv('STABILITY_API_KEY')

headers = {
    "Accept": "application/json",
    "Authorization": "Bearer {}".format(api_key)
}

response = requests.get(
    "{api_host}/v1/models",
    headers=headers
)

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

models = response.json()
print(models)

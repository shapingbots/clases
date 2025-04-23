import requests
from openai import OpenAI
import prompts

key = ""

client = OpenAI(api_key=key)

vector_store = ""

#Llamado de la función
def create_vector_store():
    url = "https://api.openai.com/v1/vector_stores"
    headers = {
        'Content-Type': 'application/json', 
        "Authorization": "Bearer " + key,
        "OpenAI-Beta": "assistants=v2"
    }
    data = {
            "name": "",
        }

    response = requests.post(url, headers=headers, json=data)

    return response.text

#vector = create_vector_store()
#print(vector)

#Subir un archivo
def upload_file(paths):

    # Ready the files for upload to OpenAI
    file_paths = paths
    file_streams = [open(path, "rb") for path in file_paths]

    # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    # and poll the status of the file batch for completion.
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store, files=file_streams
    )

    # You can print the status and the file counts of the batch to see the result of this operation.
    print(file_batch.status)
    print(file_batch.file_counts)

    return file_batch.status

#status = upload_file(["./manual.txt"])

#Ver archivos del vector
def check_vector_store():
    url = f"https://api.openai.com/v1/vector_stores/{vector_store}/files"
    headers = {
        'Content-Type': 'application/json', 
        "Authorization": "Bearer " + key,
        "OpenAI-Beta": "assistants=v2"
    }
    data = {
            "name": "",
        }

    response = requests.get(url, headers=headers)

    return response.text

#files_check = check_vector_store()
#print(files_check)

def create_assistant():
    url = "https://api.openai.com/v1/assistants"
    headers = {
        'Content-Type': 'application/json', 
        "Authorization": "Bearer " + key,
        "OpenAI-Beta": ""
    }
    data = {
            "name": "",
            "model": "gpt-4o",
            "description": "",
            "instructions": prompts.general,
            "tools": [{"type": "file_search"}],
            "tool_resources": {"file_search": {"vector_store_ids": [vector_store]}},
            "temperature": 0.2
        }

    response = requests.post(url, headers=headers, json=data)

    return response.text

#assist = create_assistant()
#print(assist)

#Delete file from vector strore
def delete_file_vector_store():
    url = f"https://api.openai.com/v1/vector_stores/{vector_store}/files/file-76RNkps2GXDPWL5B7wB4Ta"
    headers = {
        'Content-Type': 'application/json', 
        "Authorization": "Bearer " + key,
        "OpenAI-Beta": "assistants=v2"
    }
    data = {
            "name": "",
        }

    response = requests.delete(url, headers=headers)

    return response.text

#files_check = delete_file_vector_store()
#print(files_check)
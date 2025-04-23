import requests
from openai import OpenAI


AssistantID = ""
key = ""

client = OpenAI(api_key=key)
#Crear thread
def create_thread():
    url = "https://api.openai.com/v1/threads"
    headers = {
        'Content-Type': 'application/json', 
        "Authorization": "Bearer " + key,
        "OpenAI-Beta": "assistants=v2"
    }
    data = {
            "messages": [{"role": "user", "content": "Hola"}],
            "tool_resources": {"file_search": {"vector_store_ids": ["vs_67cf151143ec8191b6398d5ee18ad4ad"]}}
        }

    response = requests.post(url, headers=headers, json=data)

    return response.text

#thr = create_thread()
#print(thr)

#Crear mensaje
def create_message(thread_id, message):
    url = f"https://api.openai.com/v1/threads/{thread_id}/messages"
    headers = {
        'Content-Type': 'application/json', 
        "Authorization": "Bearer " + key,
        "OpenAI-Beta": "assistants=v2"
    }
    data = {
            "role": "user", 
            "content": message
        }

    response = requests.post(url, headers=headers, json=data)

    return response.text

thread_id = "thread_bj5UfQsQ534afB3L0uXjSxcS"

while True:
    
    # Use the create and poll SDK helper to create a run and poll the status of
    # the run until it's in a terminal state.

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id, assistant_id=AssistantID
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread_id, run_id=run.id))

    message_content = messages[0].content[0].text
    annotations = message_content.annotations
    citations = []
    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")

    print(message_content.value)
    print("\n".join(citations))
    
    
    message = input("Tu mensaje: ")
    response = create_message(thread_id, message)
    print(response)
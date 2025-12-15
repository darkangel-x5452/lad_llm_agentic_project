from ollama import chat
import os

os.environ["OLLAMA_NUM_GPU_LAYERS"] = "20"

def standard_input():
    response = chat(
        model='llama3.2:3b',
        messages=[
            {"role": "system", "content": "You are a precise automation assistant."},
            {"role": "user", "content": "Summarize this text in 3 bullet points:\nWSL enables GPU passthrough..."}
        ]
    )

    print(response['message']['content'])



def stream_input():
    for chunk in chat(
        model='llama3.2:3b',
        messages=[{"role": "user", "content": "Generate a bash script to clean log files"}],
        stream=True,
    ):
        print(chunk['message']['content'], end='', flush=True)

def run_app():
    print("hi")
    standard_input()
    stream_input()
    print("bye")

if __name__ == "__main__":
    run_app()
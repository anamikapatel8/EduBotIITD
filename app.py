from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv
import os



app = Flask(__name__)
# Load .env file into environment variables
load_dotenv()

AZURE_ENDPOINT        = os.environ["AZURE_ENDPOINT"]
AZURE_KEY             = os.environ["AZURE_KEY"]
AZURE_PROJECT_NAME    = os.environ["AZURE_PROJECT_NAME"]
AZURE_DEPLOYMENT_NAME = os.environ["AZURE_DEPLOYMENT_NAME"]
AZURE_REGION          = os.environ.get("AZURE_REGION", "centralindia")  # fallback default

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get("question", "")

    url = f"{AZURE_ENDPOINT}/language/:query-knowledgebases?projectName={AZURE_PROJECT_NAME}&api-version=2021-10-01&deploymentName={AZURE_DEPLOYMENT_NAME}"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "question": question,
        "top": 3,
        "includeUnstructuredSources": True,  # uses your uploaded Excel
        }
    

    response = requests.post(url, headers=headers, json=payload)
    print("Azure Raw Response:", response.text)  # Debug output

    result = response.json()

    if "answers" in result and result["answers"]:
        top_answer = result["answers"][0]
        return jsonify({
            "answer": top_answer["answer"],
            "confidenceScore": top_answer.get("confidenceScore"),
            "source": top_answer.get("source")
        })
    else:
        return jsonify({"answer": "Sorry, I couldn't find an answer."})

if __name__ == '__main__':
    app.run(debug=True)

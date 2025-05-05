from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual Azure values
AZURE_ENDPOINT = "https://queansiitd.cognitiveservices.azure.com/"
AZURE_KEY = "8Ta0WcxNRXz0F3vbZkfqGUjEZiWccGEqPSgDzuoIDknqypJITHlHJQQJ99BDACGhslBXJ3w3AAAaACOGyfCh"
AZURE_PROJECT_NAME = "EduBotIITDQueAns"
AZURE_DEPLOYMENT_NAME = "production"
AZURE_REGION = "centralindia"  # e.g., centralindia

@app.route('/', methods=['GET'])
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>EduBot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding-top: 100px;
                background-color: #f0f8ff;
            }
            h1 {
                color: #0077cc;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to EduBotIITD </h1>
        <p>Ask academic questions via our smart API endpoint at <code>/ask</code>.</p>
    </body>
    </html>'''

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get("question", "")

    url = f"{AZURE_ENDPOINT}/language/:query-knowledgebases?projectName={AZURE_PROJECT_NAME}&api-version=2021-10-01&deploymentName={AZURE_DEPLOYMENT_NAME}"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/json"
    }

    payload = {"top": 3,
    "question": question,
    "includeUnstructuredSources": True,
    "confidenceScoreThreshold": 0.3,
    "answerSpanRequest": {
        "enable": True,
        "topAnswersWithSpan": 1,
        "confidenceScoreThreshold": 0.3
    },
    "filters": {
        "metadataFilter": {
            "logicalOperation": "AND",
            "metadata": []
            }
        }
    }
    

    response = requests.post(url, headers=headers, json=payload)
    print("Azure Raw Response:", response.text)  # 🔍 Debug output

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

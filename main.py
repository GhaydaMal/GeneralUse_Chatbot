from flask import Flask, render_template, request, jsonify
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)

# Initialize the model once
model = OllamaLLM(model="llama3")

template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

context = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    global context
    data = request.json
    query = data.get('query')

    if query:
        result = chain.invoke({"context": context, "question": query})
        response = {"message": result}
        context += f"\nUser: {query}\nAI: {result}"
        return jsonify(response)
    else:
        return jsonify({"message": "No query received"}), 400

if __name__ == "__main__":
    app.run(debug=True)

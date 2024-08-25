from flask import Flask, render_template, request, jsonify
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Initialize the Flask application
app = Flask(__name__)

# Initialize the language model once
model = OllamaLLM(model="llama3")

# Define the prompt template for the language model
template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

# Create a ChatPromptTemplate from the defined template
prompt = ChatPromptTemplate.from_template(template)

# Create a chain that combines the prompt with the model
chain = prompt | model

# Initialize an empty string to store the conversation context
context = ""

@app.route('/')
def index():
    # Render the HTML page for the chat interface
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    global context
    # Get the JSON data sent in the POST request
    data = request.json
    
    # Extract the user query from the data
    query = data.get('query')

    if query:
        # Use the chain to get a response from the language model
        result = chain.invoke({"context": context, "question": query})
        
        # Prepare the response with the model's result
        response = {"message": result}
        
        # Update the conversation context with the new user query and model response
        context += f"\nUser: {query}\nAI: {result}"
        
        # Return the response as JSON
        return jsonify(response)
    else:
        # Return an error message if no query was received
        return jsonify({"message": "No query received"}), 400

if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)

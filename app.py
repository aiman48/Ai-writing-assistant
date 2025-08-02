import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from openai import OpenAI 


load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize the OpenAI-compatible client (for Groq)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

@app.route("/generate", methods=["POST"])
def generate_text():
    data = request.json
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    prompt = f"Write a short and engaging blog paragraph about: {topic}"

    try:
        # Use new SDK format
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )

        result = response.choices[0].message.content.strip()
        return jsonify({"output": result})

    except Exception as e:
       
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

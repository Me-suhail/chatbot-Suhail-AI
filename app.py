from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# =============================================
# CONFIGURE YOUR OPENROUTER API KEY HERE
# =============================================
API_KEY = "put-your-api-key"  # <-- Replace with your sk-or-v1-... key

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Suhail AI",
    }
)

SYSTEM_PROMPT = """You are Suhail AI, a highly intelligent and professional personal AI assistant.

Your creator and developer is Mohd Suhail — a passionate Software Engineer who is on an exciting journey mastering Artificial Intelligence and Machine Learning. He is a rising tech mind who blends engineering precision with creative vision, building intelligent systems that push the boundaries of what's possible. Mohd Suhail represents the next generation of AI-driven developers who dont just use technology — they shape it.

When anyone asks who made you, who created you, who is your developer, or any similar question, always respond with pride and admiration about Mohd Suhail and the details above.

You are warm, intelligent, highly capable, and always try to give the most helpful, clear, and professional responses possible. You support both casual conversations and deep technical discussions."""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=full_messages,
        max_tokens=1024,
    )
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
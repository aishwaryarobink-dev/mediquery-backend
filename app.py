import os 
import json
from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": [
        "http://localhost:5173",
        "http://localhost:5174",
        "https://mediquery-frontend.vercel.app"  # Your Vercel URL
    ],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
    "supports_credentials": True
}})
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
KNOWLEDGE_BASE=[]

try:
    with open('medical_knowledge.json', 'r') as f:
        data = json.load(f)
        KNOWLEDGE_BASE = [doc['content'] for doc in data.get('documents', [])]
        print(f"Loaded {len(KNOWLEDGE_BASE)} docs")
except:
    print("No local knowledge base found")

def get_context(query):
    if not KNOWLEDGE_BASE:
        return ""
    
    query_words = set(query.lower().split())
    best_doc, best_score = "", 0
    for doc in KNOWLEDGE_BASE:
        score = sum(1 for word in query_words if word in doc.lower())
        if score>best_score:
            best_score=score
            best_doc=doc
    if best_score>=1:
        return best_doc
    else:
        return ""

@app.route('/')
def health():
    return {"status":"ok"}

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return '', 204
    
    data = request.json
    msgs = data.get("messages",[])
    if not msgs:
        return {"error":"No messages provided"}, 400
    context = get_context(msgs[-1]["content"])

    def generate():
        try:
            stream = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role":"system",
                        "content": f"""You are a helpful medical assistant. 
                        Use the following context to answer the question: {context} 
                        If the context does not contain relevant information, answer based on your general medical knowledge.
                        Keep answer safe and simple."""
                    }
                ]
                +msgs,
                stream=True
            )
            source_type = "kb" if context else "model"

            for chunk in stream:
                content=chunk.choices[0].delta.content
                if content:
                    yield f"data: {json.dumps({'text': content,'source': source_type})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(stream_with_context(generate()),
                        mimetype='text/event-stream',
                        )
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
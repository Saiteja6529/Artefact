from flask import Flask, request, jsonify
from flask_cors import CORS
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
from rag_chat import get_rag_response

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data     = request.get_json()
    query    = data.get('query', '')
    category = data.get('category', 'greek')
    book     = data.get('book', 'iliad')
    answer   = get_rag_response(category, book, query)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    print("Running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)
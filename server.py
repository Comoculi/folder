from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
import logging

# Configure paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Initialize Flask
app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        logger.debug(f"Received data: {data}")
        
        if not data or 'text' not in data:
            return jsonify({"error": "Missing text parameter"}), 400

        mode = data.get('mode', '1')
        text = data['text'].strip()
        
        if not text:
            return jsonify({"error": "Text cannot be empty"}), 400

        mode_prompts = {
            "1": "Convert to standard Ottoman Turkish for daily use, always in turkish",
            "2": "Convert to lovely short Ottoman Turkish with elegant metaphors, always in turkish",
            "3": "Convert to historical Ottoman insults (no modern vulgarity), always in turkish"
        }

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"{mode_prompts[mode]}. Respond only with the converted text."},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=150
        )

        result = response.choices[0].message.content
        return jsonify({"result": result})
    
    except Exception as e:
        logger.error(f"Conversion error: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# Serve static files
@app.route('/')
def serve_index():
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(STATIC_DIR, path)

if __name__ == '__main__':
    # Create static directory if not exists
    os.makedirs(STATIC_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
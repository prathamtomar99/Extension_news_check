from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import os
import traceback
from crew_ai import get_content_crew
from main import generate_summary_dictionary_llm_fetch_google_news

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/process', methods=['POST'])
def process():
    # Check if GEMINI_API_KEY is set
    if not os.getenv('GEMINI_API_KEY'):
        return jsonify({
            "error": "GEMINI_API_KEY environment variable is not set. Please create a .env file with your API key."
        }), 500

    try:
        data = request.json
        if not data:
            return jsonify({
                "error": "Invalid request. No JSON data provided."
            }), 400
            
        if 'headline' not in data or 'text' not in data:
            return jsonify({
                "error": "Invalid request. Please provide both 'headline' and 'text' in the request body."
            }), 400
            
        if not data['headline'] or not data['text']:
            return jsonify({
                "error": "Invalid request. 'headline' and 'text' cannot be empty."
            }), 400

        main_content_news = get_content_crew(data['headline'], data['text'])
        processed_output = generate_summary_dictionary_llm_fetch_google_news(main_content_news, data['headline'])
        
        if not processed_output:
            return jsonify({
                "message": "No similar news articles found."
            }), 200
            
        return jsonify(processed_output)

    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"Error: {str(e)}\n{error_traceback}")
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
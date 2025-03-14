# News Verification System

A sophisticated browser extension and backend system that helps users verify news articles by comparing them with other sources, providing an effective tool against misinformation.

## Features

- **Browser Extension**: Seamlessly extracts news content from web pages
- **AI-powered Analysis**: Utilizes CrewAI and Google's Gemini model for intelligent content extraction
- **News Comparison**: Fetches and compares similar news articles from multiple sources
- **Similarity Scoring**: Calculates and displays similarity scores between the current article and other sources
- **Detailed Results**: Provides summaries and links to related news articles

## Project Structure

- `app.py`: Flask backend API that processes requests from the extension
- `crew_ai.py`: CrewAI agent configuration for intelligent content extraction
- `main.py`: Core functionality for news verification and Google News integration
- `content_loading.py`: Utilities for processing and extracting news content
- `cosine_similarity.py`: Implementation of similarity calculation between news articles
- `extension/`: Chrome extension files
  - `background.js`: Handles communication between the extension and backend
  - `popup.js`: Manages the extension's user interface logic
  - `popup.html`: User interface for the extension
  - `manifest.json`: Extension configuration file

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI=your_gemini_api_key
   RAPIDAPI_KEY=your_rapidapi_key  # For Google News API
   ```

4. Run the Flask server:
   ```bash
   python app.py
   ```
   The server will start on http://127.0.0.1:5000

### Extension Setup

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" using the toggle in the top-right corner
3. Click "Load unpacked" and select the `extension` folder from this project
4. The News Processor extension should now be available in your browser toolbar

## Usage Guide

1. Navigate to a news article in your browser
2. Click on the News Processor extension icon in the toolbar
3. Click the "Process News" button in the popup
4. The extension will extract the headline and content from the current page
5. The backend will process the content, find similar news articles, and calculate similarity scores
6. View the results showing similar news articles with their summaries and similarity scores
7. Click on article links to read the original sources for verification

## How It Works

1. The extension extracts the headline and text content from the current webpage
2. The backend uses CrewAI with Google's Gemini model to extract the most relevant information
3. The system searches for similar news articles using Google News API
4. For each found article, the content is scraped and summarized
5. Similarity scores are calculated between the original article and each found article
6. Results are returned to the extension and displayed to the user

## Technologies Used

- **Python 3.11+**: Core backend language
- **Flask**: Web framework for the backend API
- **CrewAI**: Framework for creating AI agents
- **Google Gemini AI**: Large language model for content analysis
- **spaCy**: Natural language processing for similarity calculation
- **Chrome Extension API**: For browser integration
- **Transformers (Hugging Face)**: For NLP tasks
- **RapidAPI**: For accessing Google News data

## Troubleshooting

- Ensure the Flask server is running before using the extension
- Check that your API keys in the `.env` file are valid
- If the extension doesn't work, try refreshing the page or restarting Chrome
- For CORS issues, ensure the Flask server has CORS enabled (already implemented)

## Future Improvements

- Add support for more languages
- Implement user authentication for personalized results
- Add a dashboard for tracking news verification history
- Integrate with fact-checking databases
- Expand to other browsers (Firefox, Safari, etc.)

## License

MIT 
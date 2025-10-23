# app.py (Final Version with Markdown Formatting)

import configparser
from datetime import datetime
from flask import Flask, render_template, request, make_response
import markdown  # <-- ADDED for Markdown conversion

import telegram_handler
import n8n_handler

# --- Configuration ---
config = configparser.ConfigParser()
config.read('config.ini')

API_ID = int(config['telegram']['api_id'])
API_HASH = config['telegram']['api_hash']
SESSION_FILE = "telegram_session"
N8N_WEBHOOK_URL = config['n8n']['webhook_url']

# --- Flask App ---
app = Flask(__name__)

@app.route('/')
async def index():
    """Renders the main search form and populates it with chats."""
    try:
        chats = await telegram_handler.fetch_all_chats(API_ID, API_HASH, SESSION_FILE)
        return render_template('index.html', chats=chats, error=None)
    except Exception as e:
        return render_template('index.html', chats=[], error=str(e))

@app.route('/search', methods=['POST'])
async def search():
    """Handles the form submission, searches Telegram, gets summary, and shows results."""
    # 1. Get data from the form
    keywords = [k.strip() for k in request.form.get('keywords', '').split(',') if k.strip()]
    chat_ids = [int(cid) for cid in request.form.getlist('chats')]
    start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
    end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
    max_results = int(request.form.get('max_results', 200))

    # 2. Search Telegram
    messages = await telegram_handler.search_messages(
        API_ID, API_HASH, SESSION_FILE, keywords, chat_ids, start_date, end_date, max_results
    )

    # 3. Get summary from n8n
    message_texts = [msg['text'] for msg in messages]
    summary_markdown = n8n_handler.get_summary(message_texts, N8N_WEBHOOK_URL)
    
    # 4. Convert the Markdown summary to HTML before rendering
    summary_html = markdown.markdown(summary_markdown, extensions=['fenced_code', 'tables'])
    
    # 5. Create a response, pass the HTML, and add headers to prevent caching
    response = make_response(render_template('results.html', summary_html=summary_html, messages=messages))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(debug=True)
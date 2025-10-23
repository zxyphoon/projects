import requests

def get_summary(messages_text_list, webhook_url):
    """Sends a list of message texts to n8n and returns the summary."""
    if not messages_text_list:
        return "No messages were found to summarize."
    
    if not webhook_url or 'YOUR_N8N_WEBHOOK_URL' in webhook_url:
        return "Error: n8n webhook URL is not configured in config.ini."

    payload = {"messages": messages_text_list}

    try:
        # --- ADD THESE TWO LINES FOR DEBUGGING ---
        print(f"\n--- Attempting to send {len(messages_text_list)} messages to n8n ---")
        print(f"Webhook URL: {webhook_url}")
        # -----------------------------------------

        response = requests.post(webhook_url, json=payload, timeout=120)
        response.raise_for_status()
        
        return response.json().get('summary', "Error: 'summary' key not found in n8n response.")
    except requests.exceptions.RequestException as e:
        # This will now print any network errors to your terminal!
        print(f"!!! N8N WEBHOOK FAILED: {e}") 
        return f"Error connecting to n8n webhook: {e}"
    except Exception as e:
        print(f"!!! UNEXPECTED N8N ERROR: {e}")
        return f"An unexpected error occurred with n8n: {e}"
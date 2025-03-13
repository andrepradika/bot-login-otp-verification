from googleapiclient.errors import HttpError
import base64
from bs4 import BeautifulSoup

def get_verification_code(service, user_id='me'):
    """Fetches the newest email with the specified subject and extracts the verification code."""
    try:
        query = 'subject:"Rahasia - Informasi Kode Verifikasi BCA ID Anda"'
        results = service.users().messages().list(userId=user_id, maxResults=5, q=query).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No verification email found.')
            return None

        # Get the newest message by sorting with internalDate
        latest_msg = max(messages, key=lambda m: m.get('internalDate', 0))
        msg_id = latest_msg['id']
        msg = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        
        payload = msg.get("payload", {})
        email_body = None

        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/html":  # Prefer HTML version
                    data = part["body"].get("data", "")
                    decoded_data = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    email_body = decoded_data
                    break
        
        if not email_body:
            print("Email body not found.")
            return None

        # Extract verification code using BeautifulSoup
        soup = BeautifulSoup(email_body, 'html.parser')
        code_element = soup.find('p', style=lambda s: s and 'font-size: 30px' in s)

        if code_element:
            verification_code = code_element.get_text(strip=True)
            return verification_code
        else:
            print('Verification code not found.')
            return None

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

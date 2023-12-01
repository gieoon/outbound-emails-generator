import requests
import json

EMAIL_API_SERVER = 'https://webbi-email-server.ts.r.appspot.com';

# Straight out of ChatGPT's mouth.
def send_plain_data(destination_email, subject, content, website_owners, retry_count=0):
    print('SENDING EMAIL TO:', destination_email)
    if not retry_count:
        retry_count = 0

    subject = "A price estimate for your website"

    support_email = "YOUR_SUPPORT_EMAIL"  # Replace with your actual support email

    payload = {
        "subject": subject,
        "text": content,
        "destination_name": website_owners,
        "destination_email": destination_email,
        "title": "Website design or redesign",
        "from_name": "Webbi Digital Studio",
        "from_address": "hello@webbi.co.nz",
        "reply_email": support_email,
        "reply_subject": "Hi Jun",
        "reply_body": "Tell me about . . .",
        # "attachment": attachment,
        # "attachment_path": attachment_path,
        # "attachment_name": "Website Price Estimate - Webbi Digital Studio.pdf",
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(email_api_server, data=json.dumps(payload), headers=headers)

    print("RESPONSE STATUS:", response.status_code)

    # Resend if status is not 200.
    # TESTING
    if response.status_code != 200 and retry_count < 2:
        print('RESENDING AFTER FAIL')
        send_plain_data(destination_email, retry_count + 1)
        print('response text', response.text)
    
    elif retry_count == 2:
        # Log failure message to DB with all of the data.
        # TODO: enable this.
        # log_error_email({...})
        print("ERROR Failed to send email after 2 tries")
        print('response text', response.text)
    
    if response.status_code == 200:
        print("Send email successfully")

# Example usage
# send_plain_data("destination@example.com", "attachment_data", "attachment_path", callback_function)

import requests
import json
from _firestore import get_firestore
import firebase_admin
from firebase_admin import firestore

EMAIL_API_SERVER = 'https://webbi-email-server.ts.r.appspot.com';

# Straight out of ChatGPT's mouth.
def send_plain_data(destination_email, company_name, subject, content, website_owners, retry_count=0):
    print('Sending email to ', destination_email)

    if not retry_count:
        retry_count = 0

    support_email = "hello@webbi.co.nz"  # Replace with your actual support email

    payload = {
        "subject": subject,
        "text": content,
        "destination_name": website_owners,
        "destination_email": destination_email,
        "title": subject,
        "from_name": "Webbi Digital Studio",
        "from_address": "alex@mail.webbi.co.nz", #"hello@webbi.co.nz",
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

    response = requests.post(EMAIL_API_SERVER, data=json.dumps(payload), headers=headers)

    print("RESPONSE STATUS:", response.status_code)

    # Resend if status is not 200.
    # TESTING
    if response.status_code != 200 and retry_count < 2:
        print('RESENDING AFTER FAIL')
        send_plain_data(destination_email, subject, content, website_owners, retry_count + 1)
        print('response text', response.text)
    
    elif retry_count == 2:
        # Log failure message to DB with all of the data.
        # TODO: enable this.
        # log_error_email({...})
        print("ERROR Failed to send email after 2 tries")
        print('response text', response.text)
    
    if response.status_code == 200:
        print("Sent email successfully")
        save_email_sent(destination_email, company_name, subject, content, website_owners)
        

def save_email_sent(destination_email, company_name, subject, content, website_owners):
    db = get_firestore()
    doc_ref = db.collection("Emails").document(company_name + ' ' + destination_email)
    doc_ref.set({
        "content": content,
        "companyName": company_name,
        "destinationEmail": destination_email,
        "subject": subject,
        "websiteOwners": website_owners,
        "dateSent": firestore.SERVER_TIMESTAMP,
    }, merge=True)
    print('Email saved to Firestore')


# Example usage
# send_plain_data("destination@example.com", "attachment_data", "attachment_path", callback_function)

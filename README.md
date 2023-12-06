# Generates personalized cold outreach emails introducing your business to potential customers.

This is for generating leads and email marketing campaigns.

## How it works:

1. The script runs a google maps query to find matching businesses.
e.g. "Beauty salons in Tokyo"
1. It uses the details of each Google My Business listing to get the business's website and scrapes it to get phone numbers and email addresses.   
1. Based on the business's details, generate a personalized email for their company that introduces them to your services.
1. Watch your leads come in.

## What it uses:

1. OpenAI (of course)
1. Firestore to store sent emails for lead tracking.
1. Your shameless ego

# How to run this:

## 1. Modify the places query to get a list of companies.
$ python google_places.py

## 1. Generates the emails, each is stored under /generated_emails

$ python main.py

## Send the emails after approving each.

$ python send_emails.py
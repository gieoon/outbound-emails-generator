import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('./automated-salesperson-firebase-adminsdk-tf22v-d16a5f2f3b.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

def get_firestore():
    return db
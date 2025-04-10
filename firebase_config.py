import firebase_admin
from firebase_admin import credentials, firestore, storage

def init_firebase():
    # Load the service account key
    cred = credentials.Certificate("firebase_key.json")
    
    # Initialize Firebase app if not already initialized
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {
            'storageBucket': "familyappmvp-dapper.firebasestorage.app"  # 🔁 Replace with your actual storage bucket
        })

    # Return Firestore database and Storage bucket references
    db = firestore.client()
    bucket = storage.bucket()
    return db, bucket

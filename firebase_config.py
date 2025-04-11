import firebase_admin
from firebase_admin import credentials, firestore, storage

def init_firebase():
    cred = credentials.Certificate("firebase_key.json")

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'familyappmvp-dapper.appspot.com'
        })

    db = firestore.client()
    bucket = storage.bucket()
    return db, bucket
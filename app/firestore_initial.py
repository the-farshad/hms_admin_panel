'''
Return the firestore connection
'''
import firebase_admin
from firebase_admin import (
    credentials,
    firestore
)
from file_check import file_abs_path as path


def cloud_firestore_initial():
    '''
    Initial Firestore database conaction and api
    '''
    if not firebase_admin._apps:
        cred = credentials.Certificate(
            path()+("API_KEY/serviceAccountKey.json")
        )
        firebase_admin.initialize_app(cred)
    return firestore.client()


if __name__ == '__main__':
    cloud_firestore_initial()

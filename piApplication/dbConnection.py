import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('location')
firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.collection('configuration').document('docID')
doc = doc_ref.get()
if doc.exists:
    print(f'Document data: {doc.to_dict()}')
else:
    print(u'No such document!')

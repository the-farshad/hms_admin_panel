from firestore_initial import cloud_firestore_initial as firestore


def cloud_firestore_initial():
    db = firestore()
    doc_ref = db.collection(u'main').document(u'dashboard').collection(u'clients')
    return doc_ref


def cloud_firestore_set_data():
    doc_ref = cloud_firestore_initial()
    doc_ref.document(u'test').set({
        u'name': u'John',
        u'family': u'Doe'
    })
    docs = doc_ref.stream()
    for doc in docs:
        print(doc.to_dict())


if __name__ == '__main__':
    cloud_firestore_set_data()

from firebase_admin import firestore, credentials, initialize_app
# from flask import jsonify

import secrets
try:
    import config
    cred = credentials.Certificate(config.FKEY)
except:
    import os
    cred = credentials.Certificate(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None))

intapp = initialize_app(cred)
datab = firestore.client()


class Userg:
    def __init__(self, name="", email="", password=""):
        self.fullname = name
        self.email = email
        self.password = password

    def getItem(self, email):
        usercoll = datab.collection('user')
        dict = usercoll.document(email).get().to_dict()
        if dict:
            self.fullname = dict['fullname']
            self.password = dict['password']
            return dict
        return 0

    def save(self, name, email, password):
        usercoll = datab.collection('user')
        usercoll.document(email).set(
            {'fullname': name, 'password': password})

    def createSession(self):
        userSession = datab.collection('session')
        token = secrets.token_urlsafe(16)
        userSession.document(token).set(
            {'token': token, 'password': self.password})
        return token

    def destroySession(self, token):
        userSession = datab.collection('session')
        userSession.document(token).delete()

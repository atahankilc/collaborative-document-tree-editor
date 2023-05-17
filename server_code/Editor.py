from Document import *
from Decorators import singleton
from threading import *


@singleton
class Editor:
    def __init__(self):
        self.documents = {}
        self.mutex = Lock()

    def new(self, templfile):
        with self.mutex:
            new_document = Document(templfile)
            self.documents[new_document.get_id()] = new_document

    def list(self):
        with self.mutex:
            return [str(document) for document in self.documents.values()]

    def open(self, document_id, user):
        with self.mutex:
            self.documents[document_id].add_user(user=user)
            return DocumentInstancePerUser(self.documents[document_id], user)

    def close(self, document_id, user):
        with self.mutex:
            self.documents[document_id].remove_user(user=user)

    def delete(self, document_id):
        with self.mutex:
            del self.documents[document_id]

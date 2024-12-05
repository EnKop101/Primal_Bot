import uuid
# This is a class for the Primal Nemesis Messages.
class PN_Class:
    def __init__(self, question: str, answer: str):
        self.id = str(uuid.uuid4())
        self.question = question
        self.answer = answer
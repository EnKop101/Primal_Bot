import uuid
# This Class is the structure of the messages.
class QA_Class():
    def __init__(self, question: str, answer: str, id: str = None):
        self.id = str(uuid.uuid4()) if id is None else id
        self.question = question
        self.answer = answer
        

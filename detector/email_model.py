class Email:
    def __init__(self, subject, message):
        self.subject = subject
        self.message = message
    def get_text(self):
        return self.subject + " " + self.message
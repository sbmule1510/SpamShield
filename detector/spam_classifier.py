class SpamClassifier:
    def __init__(self, score):
        self.score = score
    def get_result(self):
        if self.score >= 3:
            return "Spam Email Detected!"
        return "Safe Email"
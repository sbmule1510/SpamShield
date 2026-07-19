class SpamRule:

    def __init__(self):
        self.spam_dict = {
            "free": 2,
            "winner": 3,
            "lottery": 3,
            "click here": 2,
            "offer": 2,
            "claim": 2,
            "urgent": 2,
            "congratulation": 3,
            "prize": 3,
            "money": 2,
            "gift": 2
        }
    def get_rules(self):
        return self.spam_dict
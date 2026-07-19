import re
from .email_model import Email
from .spam_rule import SpamRule
from .spam_classifier import SpamClassifier

def check_spam(subject, message):
    email = Email(subject, message)
    original_text = email.get_text()
    text = original_text.lower()
    rules = SpamRule()
    spam_dict = rules.get_rules()
    score = 0
    for word, weight in spam_dict.items():
        if re.search(r"\b" + re.escape(word) + r"\b", text):
            score += weight
    if re.search(r"(https?://\S+|www\.\S+)", original_text):
        score += 2
    caps_words = re.findall(r"\b[A-Z]{4,}\b", original_text)
    if len(caps_words) >= 2:
        score += 2
    classifier = SpamClassifier(score)
    return classifier.get_result()
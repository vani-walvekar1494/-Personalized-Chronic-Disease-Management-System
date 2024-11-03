from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class Symptom:
    def __init__(self, id, user_id, symptom, created_at):
        self.id = id
        self.user_id = user_id
        self.symptom = symptom
        self.created_at = created_at


class Feedback:

    def __init__(self, is_pass: bool, score: float, message: str):
        self.is_pass = is_pass
        self.score = score
        self.message = message

    def get_score(self):
        return self.score

    def get_message(self):
        return self.message

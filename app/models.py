from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    user_chat_id = db.Column(db.String(20), unique=True, index=True, default=None)
    city = db.Column(db.String(20), index=True, default="Kiev")
    notification_time = db.Column(db.Time, default=None)

    def __repr__(self):
        return f"<User {self.username} from {self.city}>"

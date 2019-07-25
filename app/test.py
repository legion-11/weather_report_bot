from app import app, db
from app.models import User

user = models.User.


with app.app_context():
    print(User.query.all())

from app import db
from app.models import User, Msg

users = User.query.all()
msgs = Msg.query.all()
for u in users:
    if u.id == "musician":
        u.id = 'mus'
for msg in msgs:
    if msg.from_user_id == 'musician':
        msg.from_user_id = 'mus'
db.session.commit()

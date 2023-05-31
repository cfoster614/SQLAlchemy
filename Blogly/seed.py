from models import User, Posts , db
from app import app

db.drop_all()
db.create_all()

test_user = User(first_name = 'Mr. Test', last_name = 'Test')
user1 = User(first_name = 'Caity', last_name = 'Foster')
user2 = User(first_name = 'Wes', last_name = 'Lynch')
db.session.add(test_user)
db.session.add(user1)
db.session.add(user2)
db.session.commit()

test_post = Posts(title = 'Test', content = 'We are testing', user_id = '1')
post1 = Posts(title = 'Why disc priest is the best healer right now', content = 'Instant cast radiances, is there anymore that has to be said? It feels so fun right now!!!!', user_id = user1.id)

db.session.add(test_post)
db.session.add(post1)
db.session.commit()

from models import User, Posts, Tag, PostTag, db
from app import app

db.drop_all()
db.create_all()


db.session.add_all([
    User(first_name = 'Mr. Test', last_name = 'Test'),
    User(first_name = 'Caity', last_name = 'Foster'),
    User(first_name = 'Wes', last_name = 'Lynch')
])
db.session.commit()



db.session.add_all([
    Posts(title = 'Test', content = 'We are testing', user_id = '1'),
    Posts(title = 'Why disc priest is the best healer right now', content = 'Instant cast radiances, is there anymore that has to be said? It feels so fun right now!!!!', user_id = '2')
])

db.session.commit()



db.session.add_all([
    Tag(name = 'Funny'),
    Tag(name = 'Sad'),
    Tag(name = 'Venting'),
    Tag(name = 'Scary'),
    Tag(name = 'NSFW')
])

db.session.commit()

db.session.add_all([
    PostTag(post_id = '2', tag_id = '1'),
    PostTag(post_id = '2', tag_id = '2'),
    PostTag(post_id = '2', tag_id = '3'),
    PostTag(post_id = '2', tag_id = '5')
])


db.session.commit()
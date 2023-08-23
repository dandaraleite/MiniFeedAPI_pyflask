from datetime import datetime

from factory import db
from main import app
from models import User, Post

with app.app_context():
 
     # CREATE
    user = User(
    username="dandara", 
    email="dandaraleite2@gmail.com",
    birthdate=datetime.fromisoformat("2023-08-22"),
    )

    db.session.add(user)
    db.session.commit()

    # READ
    user = User.query.first()
    print(user)

    user = User.query.filter_by(username="dandara").first()

    # CREATE
    post = Post(text="First post!", author=user)
    post = Post(text="Second comment!", author=user)
    post = Post(text="Third comment!", author=user)

    db.session.add(post)
    db.session.commit()

    # UPDATE
    post = Post.query.get(2)

    post.text = "Second post!"

    db.session.commit()

    # DELETE
    post_third = Post.query.get(3)

    db.session.delete(post_third)
    db.session.commit()
   

    user = User.query.filter_by(username="dandara").first()

    # Percorre postagens e imprime seus textos
    for post in user.posts:
        print(post.text)

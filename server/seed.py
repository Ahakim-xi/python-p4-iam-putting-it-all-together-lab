
#!/usr/bin/env python3

from random import randint, choice as rc

from faker import Faker


from app import app
from models import db, Recipe, User, Message


with app.app_context():
    # Create tables if they do not exist
    db.create_all()


    print("Deleting all records...")
    Recipe.query.delete()
    User.query.delete()
    Message.query.delete()

    fake = Faker()

    print("Creating users...")

    # make sure users have unique usernames
    users = []
    usernames = []

    for i in range(20):
        username = fake.first_name()
        while username in usernames:
            username = fake.first_name()
        usernames.append(username)

        user = User(
            username=username,
            bio=fake.paragraph(nb_sentences=3),
            image_url=fake.url(),
        )

        user.password_hash = user.username + 'password'
        users.append(user)

    db.session.add_all(users)

    print("Creating recipes...")
    recipes = []
    for i in range(100):
        instructions = fake.paragraph(nb_sentences=8)
        recipe = Recipe(
            title=fake.sentence(),
            instructions=instructions,
            minutes_to_complete=randint(15,90),
        )
        recipe.user = rc(users)
        recipes.append(recipe)


    db.session.add_all(recipes)

    print("Creating messages...")
    messages = []
    for i in range(30):
        body = fake.sentence()
        username = rc(usernames)
        message = Message(
            body=body,
            username=username
        )
        messages.append(message)

    db.session.add_all(messages)

    db.session.commit()
    print("Complete.")

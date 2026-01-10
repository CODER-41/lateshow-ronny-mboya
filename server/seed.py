from app import app
from models import db, Episode, Guest, Appearance
import csv

with app.app_context():
    print("Clearing existing data...")

    Appearance.query.delete()
    Episode.query.delete()
    Guest.query.delete()

    print("Seeding episodes...")
    episodes_data = []

    with open('episode.csv', 'r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            episode = Episode(
                date=row['Show'],
                number = int(row['episode_number'])
            )
            episodes_data.append(episode)

    db.session.add_all(episodes_data)

    db.session.commit()

    print("Seeding guests...")
    guests_data = []

    with open('guests.csv', 'r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            guest = Guest(
                name=row['Raw_Guest_List'],
                occupation=row['GoogleKnowledge_Occupation']
            )
            guests_data.append(guest)
    
    db.session.add_all(guests_data)

    db.session.commit()

    print("Seeding appearances...")
    appearances_data = []


    for i in range(min(50, len(episodes_data), len(guests_data))):

        appearance = Appearance(
            rating=(i % 5) + 1

            episode_id=episodes_data[i].id,
            guest_id=guests_data[i].id
        )
        appearances_data.append(appearance)
    

    db.session.add_all(appearances_data)

    db.session.commit()

    print("Database seeded successfully!")
    print(f"Episodes: {Episode.query.count()}")       
    print(f"Guests: {Guest.query.count()}")            
    print(f"Appearances: {Appearance.query.count()}") 


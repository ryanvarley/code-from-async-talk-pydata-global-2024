"""Mock database of videos."""

from faker import Faker

NUM_VIDEOS = 1000


fake = Faker()
fake.seed_instance(20241203)


def _generate_video():
    return {
        # words are nicer than ids for experimenting
        "id": fake.words(nb=1, unique=True)[0],
        "title": fake.sentence(),
        "description": fake.paragraph(),
        "transcript": "\n\n".join(fake.paragraphs(nb=5)),
        "upload_date": fake.date_this_decade(),
        "views": fake.random_int(0, 1000000),
        "warnings": [],
    }


video_db = {v["id"]: v for v in [_generate_video() for _ in range(NUM_VIDEOS)]}

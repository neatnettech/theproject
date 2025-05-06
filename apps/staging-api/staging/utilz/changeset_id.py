from faker import Faker
import random

faker = Faker()

def generate_changeset_id() -> str:
    return "-".join(faker.word() for _ in range(4))

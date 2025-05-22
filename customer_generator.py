
from faker import Faker

class CustomerGenerator:
    def __init__(self):
        self.fake = Faker()

    def generate_customer(self):
        return {
            'name': self.fake.name(),
            'email': self.fake.email(),
            'address': self.fake.address(),
            'phone_number': self.fake.phone_number(),
            'birthdate': self.fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat()
        }

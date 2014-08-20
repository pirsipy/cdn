import factory
from faker import Factory
fake = Factory.create()

from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
User = get_user_model()


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    @factory.lazy_attribute
    def password(self):
        return make_password('qwerty')

    @factory.lazy_attribute
    def email(self):
        return fake.safe_email()

    @factory.lazy_attribute
    def name(self):
        return fake.name()


class AdminFactory(UserFactory):
    email = 'admin@example.com'
    password = make_password('admin')
    is_staff = True
    is_active = True
    is_superuser = True

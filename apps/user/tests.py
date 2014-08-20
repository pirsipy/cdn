from django.core.urlresolvers import reverse
from django.test import TestCase

from .factories import UserFactory


class UserPageTest(TestCase):

    def setUp(self):
        super(UserPageTest, self).setUp()
        self.user = UserFactory()

    def test_profile_page(self):
        url = reverse('user:detail')
        self.client.login(username=self.user.email, password='qwerty')
        resp = self.client.get(url)
        self.assertContains(resp, self.user.get_full_name())

    def test_main_page(self):
        url = reverse('main')
        resp = self.client.get(url)
        self.assertContains(resp, 'It WORKS!')

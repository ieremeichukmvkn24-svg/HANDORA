from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AccountTests(TestCase):
    def test_registration_creates_account_and_logs_in(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'buyer1',
            'email': 'buyer@example.com',
            'password1': 'SecurePass123!xy',
            'password2': 'SecurePass123!xy',
        })
        self.assertRedirects(response, reverse('accounts:profile'))
        user = get_user_model().objects.get(email='buyer@example.com')
        self.assertEqual(user.username, 'buyer1')
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

    def test_registration_rejects_invalid_email(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'buyer2',
            'email': 'not-an-email',
            'password1': 'SecurePass123!xy',
            'password2': 'SecurePass123!xy',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user_model().objects.filter(username='buyer2').exists())

    def test_profile_redirects_anonymous_user(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response['Location'])

    def test_profile_allows_authenticated_user(self):
        user = get_user_model().objects.create_user(
            username='buyer3', email='buyer3@example.com', password='SecurePass123!xy',
        )
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse('accounts:profile')).status_code, 200)

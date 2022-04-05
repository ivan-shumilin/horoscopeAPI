from daily_horoscopes import views
import datetime
from django.urls import reverse
import pdb

from daily_horoscopes.forms import UserRegistrationForm, UserloginForm
from daily_horoscopes.models import Forecast

from django.test import TestCase


class TestHoroscopeAPI(TestCase):
    fixtures = ['daily_horoscopes/tests/fixtures/forecast.json']

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

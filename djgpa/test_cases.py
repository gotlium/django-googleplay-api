# -*- coding: utf-8 -*-

import os

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from djgpa.models import GooglePlayPreferences
from djgpa.api import GooglePlay, AccountWasNotInstalled, DeviceIDIsNotSet


class DjGPATestCase(TestCase):
    def setUp(self):
        self.aid = "387c87ca2103a990"
        self.email = "djgpa.tests@gmail.com"
        self.password = "djgpapassword"
        self.app_id = 'com.google.android.apps.unveil'
        self.app_name = 'Google Goggles'
        self.app_dst = '/tmp/app.apk'
        self.token = str(
            'DQAAAL0AAAClqUgv7PDA7BctkTZ6M9Jd1DMJ1eLGG6jcBoVdTln7JXCofBdBRbPx'
            'd3408fRURiJIpJnyQ8AYnoHXtw1vyeoYMiid8Q4Cqr8d82teLbQNxn2ijKZgcdQB'
            '67aEmIhhKQDE3QVgwGUZsdCTU04AZWCLFGDaY-Ogf7qzQ2PAwz6XNyM7c23tCO6r'
            '9AY1JFphaxrcac3zQyjoRr1A2YiMYUJpE2l278wUPTyx9Di9kgpAlrtzAgeqDPe3'
            '1VPAtmlK1G4')

    def _install_account(self):
        GooglePlayPreferences.objects.create(
            android_id=self.aid,
            google_login=self.email,
            google_password=self.password
        )
        self.assertEqual(GooglePlayPreferences.objects.all().count(), 1)
        return GooglePlay(self.token).auth()

    def test_a_settings_is_set(self):
        self.assertRaises(ObjectDoesNotExist, GooglePlay)

    def test_b_settings_account_is_set(self):
        GooglePlayPreferences.objects.create(
            android_id=self.aid, google_login="", google_password=""
        )
        self.assertRaises(AccountWasNotInstalled, GooglePlay)

    def test_c_settings_android_id_is_set(self):
        GooglePlayPreferences.objects.create(
            android_id="",
            google_login=self.email,
            google_password=self.password
        )
        self.assertRaises(DeviceIDIsNotSet, GooglePlay)

    def test_d_check_details(self):
        api = self._install_account()
        details = api.details(self.app_id)
        self.assertEqual(details.docV2.title, self.app_name)

    def test_e_check_search(self):
        api = self._install_account()
        results = api.search(self.app_name)
        self.assertEqual(results[0].backendDocid, self.app_id)

    def test_f_check_download(self):
        api = self._install_account()
        self.assertEqual(api.download(self.app_id, self.app_dst), True)
        self.assertEqual(os.path.exists(self.app_dst), True)

    def test_f_check_download_from_details(self):
        api = self._install_account()
        details = api.details(self.app_id)
        self.assertEqual(api.download(
            self.app_id, self.app_dst, details), True)
        self.assertEqual(os.path.exists(self.app_dst), True)
        self.assertEqual(
            os.path.getsize(self.app_dst),
            details.docV2.details.appDetails.file[0].size
        )

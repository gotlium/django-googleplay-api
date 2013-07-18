# -*- coding: utf-8 -*-

from os import path

from django.conf import settings


def get_settings(key, default):
    return getattr(settings, key, default)


def location(x):
    return path.join(path.dirname(path.realpath(__file__)), x)


LANG = get_settings('LANG', "ru_RU")
COUNTRY = get_settings('COUNTRY', 'ru')

SERVICE = get_settings('SERVICE', "androidmarket")
URL_LOGIN = get_settings(
    'URL_LOGIN', "https://android.clients.google.com/auth")
ACCOUNT_TYPE_GOOGLE = get_settings('ACCOUNT_TYPE_GOOGLE', "GOOGLE")
ACCOUNT_TYPE_HOSTED = get_settings('ACCOUNT_TYPE_HOSTED', "HOSTED")
ACCOUNT_TYPE_HOSTED_OR_GOOGLE = get_settings(
    'ACCOUNT_TYPE_HOSTED_OR_GOOGLE', "HOSTED_OR_GOOGLE")

DOWNLOAD_AGENT = get_settings(
    'DOWNLOAD_AGENT',
    "AndroidDownloadManager/4.1.1 (Linux; U; Android 4.1.1; "
    "Nexus S Build/JRO03E)")

AUTH_VALUES = get_settings('AUTH_VALUES', {
    "Email": None,
    "Passwd": None,
    "service": SERVICE,
    "accountType": ACCOUNT_TYPE_HOSTED_OR_GOOGLE,
    "has_permission": "1",
    "source": "android",
    "androidId": None,
    "app": "com.android.vending",
    "device_country": COUNTRY,
    "operatorCountry": COUNTRY,
    "lang": COUNTRY,
    "sdk_version": "16"
})

REQUEST_URL = get_settings(
    'REQUEST_URL', "https://android.clients.google.com/fdfe/%s"
)
REQUEST_HEADERS_TO_API = get_settings('REQUEST_HEADERS_TO_API', {
    "Accept-Language": LANG,
    "Authorization": "",
    "X-DFE-Enabled-Experiments": "cl:billing.select_add_instrument_by_default",
    "X-DFE-Unsupported-Experiments": str(
        "nocache:billing.use_charging_poller,market_emails,buyer_currency,"
        "prod_baseline,checkin.set_asset_paid_app_field,shekel_test,"
        "content_ratings,buyer_currency_in_app,nocache:encrypted_apk,"
        "recent_changes"),
    "X-DFE-Device-Id": "",
    "X-DFE-Client-Id": "am-android-google",
    "User-Agent": "Android-Finsky/3.7.13 ("
                  "api=3,versionCode=8013013,sdk=16,device=crespo,"
                  "hardware=herring,product=soju)",
    "X-DFE-SmallestScreenWidthDp": "320",
    "X-DFE-Filter-Level": "3",
    "Accept-Encoding": "",
    "Host": "android.clients.google.com"
})

REQUEST_POST_CONTENT_TYPE = get_settings(
    'REQUEST_POST_CONTENT_TYPE',
    "application/x-www-form-urlencoded; charset=UTF-8")

TOKEN_FILE = get_settings('TOKEN_FILE', "/tmp/google.token")
TOKEN_TTL = get_settings('TOKEN_TTL', 3)

AID_GENERATOR = location('android-checkin/android-checkin.jar')

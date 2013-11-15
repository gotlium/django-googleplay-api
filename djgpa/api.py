# -*- coding: utf-8 -*-

import datetime
import urllib
import os

import grab
import pb2

from django.core.exceptions import ObjectDoesNotExist

from .models import GooglePlayPreferences
from .configs import (
    AUTH_VALUES, REQUEST_HEADERS_TO_API, URL_LOGIN,
    TOKEN_FILE, TOKEN_TTL, REQUEST_URL, DOWNLOAD_AGENT)


from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
from google.protobuf.message import Message
from google.protobuf import descriptor


class AccountWasNotInstalled(Exception):
    """ Google accounts was not installed """


class DeviceIDIsNotSet(Exception):
    """ Device ID is not set. """


class GooglePlay(object):
    def __init__(self, token=None):
        conf = GooglePlayPreferences.objects.all()

        if not conf.count():
            raise ObjectDoesNotExist('Config not exists.')
        if not (conf[0].google_login != "" and conf[0].google_password != ""):
            raise AccountWasNotInstalled(
                'Google accounts was not installed.')
        if not conf[0].android_id:
            raise DeviceIDIsNotSet('Device ID is not set.')

        conf = conf[0]

        if conf.proxy_host and conf.proxy_port:
            self.proxy = '%s:%s' % (conf.proxy_host, conf.proxy_port)
        if conf.proxy_login and conf.proxy_password:
            self.proxy_auth = '%s:%s' % (conf.proxy_login, conf.proxy_password)
        self.proxy_enabled = conf.proxy_enabled
        self.token = token

        AUTH_VALUES['Email'] = conf.google_login
        AUTH_VALUES['Passwd'] = conf.google_password
        AUTH_VALUES['androidId'] = conf.android_id
        REQUEST_HEADERS_TO_API['X-DFE-Device-Id'] = conf.android_id

    def toDict(self, protoObj):
        """Converts the (protobuf) result from an API call into a dict, for
        easier introspection."""
        iterable = False
        if isinstance(protoObj, RepeatedCompositeFieldContainer):
            iterable = True
        else:
            protoObj = [protoObj]
        retlist = []

        for po in protoObj:
            msg = dict()
            for fielddesc, value in po.ListFields():
                if fielddesc.type == descriptor.FieldDescriptor.TYPE_GROUP or (
                    isinstance(value, RepeatedCompositeFieldContainer)
                ) or (isinstance(value, Message)):
                    msg[fielddesc.name] = self.toDict(value)
                else:
                    msg[fielddesc.name] = value
            retlist.append(msg)
        if not iterable:
            if len(retlist) > 0:
                return retlist[0]
            else:
                return None
        return retlist

    def _get(self, url, **kwargs):
        grabber = grab.Grab()
        grabber.reset()
        grabber.setup(
            connect_timeout=5, timeout=300, hammer_mode=True,
            hammer_timeouts=((300, 360), (360, 420), (420, 480)),
        )
        if kwargs:
            grabber.setup(**kwargs)
        if self.proxy_enabled:
            if hasattr(self, 'proxy'):
                grabber.setup(proxy=self.proxy, proxy_type='http')
            if hasattr(self, 'proxy_auth'):
                grabber.setup(proxy_userpwd=self.proxy_auth)
        grabber.go(url)
        return grabber.response.body

    def _login_parse_response(self, data):
        params = {}
        for line in data:
            if not "=" in line:
                continue
            key, val = line.split("=")
            params[key.strip().lower()] = val.strip()
        return params

    def _login(self):
        response = self._get(
            URL_LOGIN, post=AUTH_VALUES, headers={"Accept-Encoding": ""})
        params = self._login_parse_response(response.split())
        if "auth" in params:
            return params["auth"]
        elif "error" in params:
            raise Exception("server says: " + params["error"])

    def _save_token(self):
        with open(TOKEN_FILE, 'w') as file_obj:
            file_obj.write(self.token)

    def _remove_token(self):
        create_time = datetime.datetime.fromtimestamp(
            os.stat(TOKEN_FILE).st_ctime)
        now = datetime.datetime.now()
        if (now - create_time).days > TOKEN_TTL:
            os.remove(TOKEN_FILE)
            return True

    def _executeRequestApi2(self, path, **kwargs):
        headers = REQUEST_HEADERS_TO_API
        headers["Authorization"] = "GoogleLogin auth=%s" % self.token
        url = REQUEST_URL % path
        response = self._get(url, headers=headers, **kwargs)
        return pb2.ResponseWrapper.FromString(response)

    def auth(self):
        if self.token:
            pass
        elif os.path.exists(TOKEN_FILE):
            if self._remove_token():
                self.auth()
            self.token = open(TOKEN_FILE).readline(1024)
        else:
            self.token = self._login()
            self._save_token()
        return self

    def search(self, query, nb_results=None, offset=None):
        path = {'q': query, 'c': 3}
        if nb_results is not None:
            path['n'] = int(nb_results)
        if offset is not None:
            path['o'] = int(offset)
        path = 'search?%s' % urllib.urlencode(path)
        results = self._executeRequestApi2(path).payload.searchResponse
        try:
            return results.doc[0].child
        except IndexError:
            return []

    def details(self, package_name):
        path = "details?%s" % urllib.urlencode({'doc': package_name})
        return self._executeRequestApi2(path).payload.detailsResponse

    def download(self, package_name, location, details=None):
        details = details and details or self.details(package_name)
        doc = details.docV2
        versionCode = doc.details.appDetails.versionCode
        offerType = doc.offer[0].offerType
        response = self._executeRequestApi2(
            "purchase", post={
                'ot': offerType,
                'doc': package_name,
                'vc': versionCode
            }
        ).payload.buyResponse.purchaseStatusResponse.appDeliveryData

        url = response.downloadUrl
        cookie = response.downloadAuthCookie[0]
        cookies = {str(cookie.name): str(cookie.value)}
        headers = {"User-Agent": DOWNLOAD_AGENT, "Accept-Encoding": ""}

        response = self._get(url, headers=headers, cookies=cookies)
        with open(location, 'wb') as out:
            out.write(response)
        return True

    def browse(self, cat=None, ctr=None):
        path = "browse?c=3"
        if cat is not None:
            path += "&cat=%s" % cat
        if ctr is not None:
            path += "&ctr=%s" % ctr
        return self._executeRequestApi2(path).payload.browseResponse

    def list(self, cat, ctr=None, nb_results=None, offset=None):
        path = "list?c=3&cat=%s" % cat
        if ctr is not None:
            path += "&ctr=%s" % ctr
        if nb_results is not None:
            path += "&n=%s" % nb_results
        if offset is not None:
            path += "&o=%s" % offset
        return self._executeRequestApi2(path).payload.listResponse

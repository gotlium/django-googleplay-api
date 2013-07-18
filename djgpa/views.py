# -*- coding: utf-8 -*-

from subprocess import Popen, STDOUT, PIPE

from django.http import HttpResponse

from .models import GooglePlayPreferences
from .configs import AID_GENERATOR


CMD = "java -jar %s '%s' '%s' 2>&1 | grep AndroidId | awk '{print $2}'"


def generate_aid(request):
    objects = GooglePlayPreferences.objects.all()[0]
    login = objects.google_login
    password = objects.google_password
    response = 'ERROR'
    result = None

    if login and password:
        command = CMD % (AID_GENERATOR, login, password)

        p = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
        result = p.communicate()

    if result and len(result):
        response = result[0].strip()
    return HttpResponse(response)

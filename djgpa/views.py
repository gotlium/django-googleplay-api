# -*- coding: utf-8 -*-

from subprocess import Popen, STDOUT, PIPE

from django.http import HttpResponse

from .models import GooglePlayPreferences
from .configs import *


def generate_aid(request):
    objects = GooglePlayPreferences.objects.all()[0]
    login = objects.google_login
    password = objects.google_password

    command = "java -jar %s '%s' '%s' 2>&1 | grep AndroidId | awk '{print $2}'"
    command = command % (AID_GENERATOR, login, password)

    p = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
    result = p.communicate()
    response = "ERROR"
    if len(result):
        response = result[0].strip()
    return HttpResponse(response)

import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import RequestContext
from django.template.loader import get_template, render_to_string

from .models import DettaglioRicettaRifinizione


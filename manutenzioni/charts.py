from django.http import JsonResponse
from django.db.models import Sum, Count
from datetime import datetime

from .models import ManutenzioneStraordinaria, Attrezzatura
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CentrodiLavoro

class CentrodiLavoroViewTests(TestCase):
    def setUp(self):
        # Crea un utente per il login (se la tua view richiede l'autenticazione)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Crea un oggetto CentrodiLavoro per i test
        self.centro_di_lavoro = CentrodiLavoro.objects.create(description='Centro di Lavoro 1')

    def test_create_centrodiLavoro_view(self):
        # Testa la view di creazione CentrodiLavoro
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('human_resources:crea_centro_di_lavoro'), {'description': 'Nuovo Centro di Lavoro'})
        self.assertRedirects(response, reverse('human_resources:tabelle_generiche'))
        # Assicurati che l'oggetto sia stato creato correttamente nel database
        self.assertEqual(CentrodiLavoro.objects.filter(description='Nuovo Centro di Lavoro').exists(), True)


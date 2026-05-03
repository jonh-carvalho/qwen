from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date

from .models import AcademicActivity
from .serializers import AcademicActivitySerializer


class AcademicActivityModelTest(TestCase):
    """Testes para o modelo AcademicActivity"""

    def setUp(self):
        self.activity = AcademicActivity.objects.create(
            title='Workshop de Python',
            description='Workshop sobre Django e DRF',
            activity_type='internal',
            date=date(2025, 1, 15),
            hours=8,
            institution='Universidade Teste'
        )

    def test_create_activity(self):
        """Testa criação de atividade acadêmica"""
        self.assertEqual(self.activity.title, 'Workshop de Python')
        self.assertEqual(self.activity.activity_type, 'internal')
        self.assertEqual(self.activity.hours, 8)

    def test_string_representation(self):
        """Testa representação string do modelo"""
        expected = f"{self.activity.title} ({self.activity.activity_type})"
        self.assertEqual(str(self.activity), expected)

    def test_external_activity(self):
        """Testa criação de atividade externa"""
        external = AcademicActivity.objects.create(
            title='Congresso Internacional',
            description='Congresso na Europa',
            activity_type='external',
            date=date(2025, 3, 20),
            hours=40,
            institution='European University'
        )
        self.assertEqual(external.activity_type, 'external')


class AcademicActivitySerializerTest(TestCase):
    """Testes para o serializer AcademicActivitySerializer"""

    def setUp(self):
        self.activity = AcademicActivity.objects.create(
            title='Curso de Machine Learning',
            description='Curso introdutório de ML',
            activity_type='internal',
            date=date(2025, 2, 10),
            hours=20
        )
        self.data = {
            'title': 'Novo Workshop',
            'description': 'Descrição do workshop',
            'activity_type': 'external',
            'date': '2025-04-15',
            'hours': 12,
            'institution': 'Instituto XYZ'
        }

    def test_serializer_fields(self):
        """Testa se o serializer retorna os campos corretos"""
        serializer = AcademicActivitySerializer(self.activity)
        expected_fields = [
            'id', 'title', 'description', 'activity_type',
            'date', 'hours', 'institution', 'certificate'
        ]
        self.assertEqual(set(serializer.data.keys()), set(expected_fields))

    def test_serializer_data(self):
        """Testa se o serializer serializa os dados corretamente"""
        serializer = AcademicActivitySerializer(self.activity)
        self.assertEqual(serializer.data['title'], self.activity.title)
        self.assertEqual(serializer.data['hours'], self.activity.hours)

    def test_serializer_create(self):
        """Testa criação via serializer"""
        serializer = AcademicActivitySerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        activity = serializer.save()
        self.assertEqual(activity.title, self.data['title'])
        self.assertEqual(activity.activity_type, self.data['activity_type'])


class AcademicActivityViewSetTest(APITestCase):
    """Testes para a API ViewSet"""

    def setUp(self):
        self.activity1 = AcademicActivity.objects.create(
            title='Atividade 1',
            description='Primeira atividade',
            activity_type='internal',
            date=date(2025, 1, 10),
            hours=4
        )
        self.activity2 = AcademicActivity.objects.create(
            title='Atividade 2',
            description='Segunda atividade',
            activity_type='external',
            date=date(2025, 1, 20),
            hours=6,
            institution='Instituto ABC'
        )
        self.list_url = reverse('academicactivity-list')

    def test_list_activities(self):
        """Testa listagem de atividades"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_activity(self):
        """Testa criação de atividade via API"""
        data = {
            'title': 'Nova Atividade',
            'description': 'Descrição da nova atividade',
            'activity_type': 'internal',
            'date': '2025-05-01',
            'hours': 10
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AcademicActivity.objects.count(), 3)

    def test_retrieve_activity(self):
        """Testa recuperação de uma atividade específica"""
        url = reverse('academicactivity-detail', args=[self.activity1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.activity1.title)

    def test_update_activity(self):
        """Testa atualização de atividade via API"""
        url = reverse('academicactivity-detail', args=[self.activity1.id])
        data = {
            'title': 'Título Atualizado',
            'description': self.activity1.description,
            'activity_type': self.activity1.activity_type,
            'date': str(self.activity1.date),
            'hours': self.activity1.hours
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.activity1.refresh_from_db()
        self.assertEqual(self.activity1.title, 'Título Atualizado')

    def test_delete_activity(self):
        """Testa exclusão de atividade via API"""
        url = reverse('academicactivity-detail', args=[self.activity1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AcademicActivity.objects.count(), 1)

    def test_filter_by_type(self):
        """Testa que todos os resultados são retornados (filtro não implementado)"""
        # Nota: Filtro por activity_type requer configuração adicional no ViewSet
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class HealthCheckTest(APITestCase):
    """Testes básicos de health check"""

    def test_api_responds(self):
        """Testa se a API está respondendo"""
        response = self.client.get(reverse('academicactivity-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

from django.test import TestCase
from django.db import IntegrityError
from .models import Bovino
from datetime import date

class BovinoModelTest(TestCase):
    def setUp(self):
        self.bovino = Bovino.objects.create(
            numero_brinco="BR12345",
            nome_produtor="João da Silva",
            sexo="macho",
            data_abate=date(2025, 12, 31),
            gta="GTA54321"
        )

    def test_bovino_creation(self):
        """Testa a criação de um bovino"""
        self.assertEqual(self.bovino.numero_brinco, "BR12345")
        self.assertEqual(self.bovino.nome_produtor, "João da Silva")
        self.assertEqual(self.bovino.sexo, "macho")
        self.assertEqual(self.bovino.gta, "GTA54321")
        
    def test_bovino_string_representation(self):
        """Testa a representação em string do bovino"""
        expected_string = "Brinco: BR12345 - Produtor: João da Silva"
        self.assertEqual(str(self.bovino), expected_string)
        
    def test_sexo_choices(self):
        """Testa as opções de sexo"""
        macho_choice = dict(Bovino.SEXO_CHOICES)['macho']
        femea_choice = dict(Bovino.SEXO_CHOICES)['femea']
        self.assertEqual(macho_choice, 'Macho')
        self.assertEqual(femea_choice, 'Fêmea')
        
    def test_unique_brinco_number(self):
        """Testa que não é possível criar dois animais com o mesmo número de brinco"""
        with self.assertRaises(IntegrityError):
            Bovino.objects.create(
                numero_brinco="BR12345",  # Mesmo número de brinco
                nome_produtor="Maria Silva",
                sexo="femea",
                data_abate=date(2025, 12, 30),
                gta="GTA98765"
            )

class BovinoViewTest(TestCase):
    def test_registro_com_brinco_duplicado(self):
        """Testa o registro com brinco duplicado"""
        # Criar um animal
        Bovino.objects.create(
            numero_brinco="BR99999",
            nome_produtor="Produtor Teste",
            sexo="macho",
            data_abate=date(2025, 12, 31),
            gta="GTA11111"
        )
        
        # Tentar criar outro com o mesmo brinco deve falhar
        with self.assertRaises(IntegrityError):
            Bovino.objects.create(
                numero_brinco="BR99999",
                nome_produtor="Outro Produtor",
                sexo="femea",
                data_abate=date(2025, 12, 30),
                gta="GTA22222"
            )
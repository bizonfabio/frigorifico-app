from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Bovino(models.Model):
    SEXO_CHOICES = [
        ('macho', 'Macho'),
        ('femea', 'Fêmea'),
    ]
    
    STATUS_AVALIACAO_CHOICES = [
        ('nao_avaliado', 'Não Avaliado'),
        ('apto', 'Apto'),
        ('inapto', 'Inapto'),
    ]
    
    CONDICAO_GERAL_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Febre', 'Febre'),
        ('Febre alta', 'Febre alta'),
        ('Castração', 'Castração'),
        ('Castração recente', 'Castração recente'),
        ('Morte súbita', 'Morte súbita'),
        ('Desidratação', 'Desidratação'),
        ('Desnutrição', 'Desnutrição'),
        ('Parto', 'Parto'),
        ('Parto distócico', 'Parto distócico'),
        ('Prenhe', 'Prenhe'),
        ('Trauma', 'Trauma'),
        ('Exaustão', 'Exaustão'),
        ('Excesso de gordura', 'Excesso de gordura'),
        ('Falta de gordura', 'Falta de gordura'),
        ('Mastite', 'Mastite'),
        ('Miotite', 'Miotite'),
        ('Neoplasia', 'Neoplasia'),
        ('Petéquia', 'Petéquia'),
        ('Ectoparasitas', 'Ectoparasitas'),
        ('Endoparasitas', 'Endoparasitas'),
        ('Queimadura', 'Queimadura'),
        ('Flebite', 'Flebite'),
        ('Abscesso', 'Abscesso'),
        ('Cicatriz', 'Cicatriz'),
        ('Cisto', 'Cisto'),
        ('Flegmão', 'Flegmão'),
        ('Fibrose', 'Fibrose'),
        ('Hematoma', 'Hematoma'),
        ('Hiperemia', 'Hiperemia'),
        ('Sarna', 'Sarna'),
        ('Tumor', 'Tumor'),
        ('Úlcera', 'Úlcera'),
        ('Verruga', 'Verruga'),
    ]
    
    CARCASSA_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Abscesso', 'Abscesso'),
        ('Cisticercose', 'Cisticercose'),
        ('Cistíase', 'Cistíase'),
        ('Contusão', 'Contusão'),
        ('Emaciação', 'Emaciação'),
        ('Enfisema', 'Enfisema'),
        ('Escarificação', 'Escarificação'),
        ('Hematoma', 'Hematoma'),
        ('Hiperemia', 'Hiperemia'),
        ('Lipomatose', 'Lipomatose'),
        ('Neoplasia', 'Neoplasia'),
        ('Petéquia', 'Petéquia'),
        ('Pneumotórax', 'Pneumotórax'),
        ('Hidrotórax', 'Hidrotórax'),
        ('Hemotórax', 'Hemotórax'),
        ('Queimadura', 'Queimadura'),
        ('Flebite', 'Flebite'),
        ('Trombose', 'Trombose'),
    ]
    
    FIGADO_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Abscesso', 'Abscesso'),
        ('Cisticercose', 'Cisticercose'),
        ('Cistíase', 'Cistíase'),
        ('Degeneração gordurosa', 'Degeneração gordurosa'),
        ('Distrofia gordurosa', 'Distrofia gordurosa'),
        ('Enterite', 'Enterite'),
        ('Fasciolíase', 'Fasciolíase'),
        ('Hidatidose', 'Hidatidose'),
        ('Hepatite', 'Hepatite'),
        ('Neoplasia', 'Neoplasia'),
        ('Necrose', 'Necrose'),
        ('Petéquia', 'Petéquia'),
    ]
    
    CORACAO_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Cisticercose', 'Cisticercose'),
        ('Cistíase', 'Cistíase'),
        ('Degeneração gordurosa', 'Degeneração gordurosa'),
        ('Distrofia gordurosa', 'Distrofia gordurosa'),
        ('Endocardite', 'Endocardite'),
        ('Miocardite', 'Miocardite'),
        ('Neoplasia', 'Neoplasia'),
        ('Necrose', 'Necrose'),
        ('Petéquia', 'Petéquia'),
        ('Pericardite', 'Pericardite'),
        ('Trombose', 'Trombose'),
    ]
    
    PULMOES_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Abscesso', 'Abscesso'),
        ('Aspergilose', 'Aspergilose'),
        ('Bronquite', 'Bronquite'),
        ('Congestão', 'Congestão'),
        ('Cisticercose', 'Cisticercose'),
        ('Cistíase', 'Cistíase'),
        ('Edema', 'Edema'),
        ('Enfisema', 'Enfisema'),
        ('Enterite', 'Enterite'),
        ('Epleurisia', 'Epleurisia'),
        ('Hidatidose', 'Hidatidose'),
        ('Neoplasia', 'Neoplasia'),
        ('Necrose', 'Necrose'),
        ('Pneumonia', 'Pneumonia'),
        ('Tuberculose', 'Tuberculose'),
    ]
    
    RINS_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Abscesso', 'Abscesso'),
        ('Cistíase', 'Cistíase'),
        ('Degeneração gordurosa', 'Degeneração gordurosa'),
        ('Distrofia gordurosa', 'Distrofia gordurosa'),
        ('Enterite', 'Enterite'),
        ('Glomerulonefrite', 'Glomerulonefrite'),
        ('Hidatidose', 'Hidatidose'),
        ('Nefrite', 'Nefrite'),
        ('Neoplasia', 'Neoplasia'),
        ('Necrose', 'Necrose'),
        ('Petéquia', 'Petéquia'),
        ('Pielonefrite', 'Pielonefrite'),
    ]
    
    DIAFRAGMA_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Abscesso', 'Abscesso'),
        ('Cisticercose', 'Cisticercose'),
        ('Cistíase', 'Cistíase'),
        ('Neoplasia', 'Neoplasia'),
        ('Necrose', 'Necrose'),
        ('Petéquia', 'Petéquia'),
        ('Tuberculose', 'Tuberculose'),
    ]
    
    LINGUA_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Abscesso', 'Abscesso'),
        ('Aftosa', 'Aftosa'),
        ('Cisticercose', 'Cisticercose'),
        ('Cistíase', 'Cistíase'),
        ('Faringite', 'Faringite'),
        ('Glosite', 'Glosite'),
        ('Neoplasia', 'Neoplasia'),
        ('Necrose', 'Necrose'),
        ('Petéquia', 'Petéquia'),
    ]
    
    CABECA_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Abscesso', 'Abscesso'),
        ('Aftosa', 'Aftosa'),
        ('Cisticercose', 'Cisticercose'),
        ('Cistíase', 'Cistíase'),
        ('Faringite', 'Faringite'),
        ('Mastite', 'Mastite'),
        ('Miotite', 'Miotite'),
        ('Neoplasia', 'Neoplasia'),
        ('Necrose', 'Necrose'),
        ('Petéquia', 'Petéquia'),
        ('Queimadura', 'Queimadura'),
        ('Rinite', 'Rinite'),
        ('Sarna', 'Sarna'),
        ('Tumor', 'Tumor'),
    ]
    
    TIPO_ANIMAL_CHOICES = [
        ('vaca', 'Vaca'),
        ('boi', 'Boi'),
        ('touro', 'Touro'),
        ('novilha', 'Novilha'),
    ]
    
    QUALIDADE_CHOICES = [
        ('desossa', 'Desossa'),
        ('fraca', 'Fraca'),
        ('media', 'Média'),
        ('boa', 'Boa'),
        ('condenada', 'Condenada'),
    ]
    
    # Vísceras Brancas
    UTERO_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Gestação Adiantada', 'Gestação Adiantada'),
        ('Metrite', 'Metrite'),
        ('Abscesso', 'Abscesso'),
        ('Prenha', 'Prenha'),
    ]
    
    BAÇO_PANCREAS_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Abscesso', 'Abscesso'),
        ('Aspecto repugnante', 'Aspecto repugnante'),
        ('Esplenomegalia', 'Esplenomegalia'),
        ('Euritrema', 'Euritrema'),
        ('Aderencia', 'Aderencia'),
    ]
    
    INTESTINO_ESTOMAGOS_BEXIGA_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Abscessos', 'Abscessos'),
        ('Enterite', 'Enterite'),
        ('Peritonite', 'Peritonite'),
        ('Tuberculose(lesão Sugestiva)', 'Tuberculose(lesão Sugestiva)'),
        ('Linfadenite', 'Linfadenite'),
        ('Adenite', 'Adenite'),
        ('Parasitoses transmissiveis', 'Parasitoses transmissiveis'),
        ('Esofagostomose', 'Esofagostomose'),
        ('Neoplasia', 'Neoplasia'),
    ]
    
    GLANDULA_MAMARIA_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Adenite', 'Adenite'),
        ('Mastite', 'Mastite'),
        ('Miiase', 'Miiase'),
        ('Aspecto repugnante', 'Aspecto repugnante'),
    ]
    
    numero_brinco = models.CharField(max_length=50, unique=True)
    nome_produtor = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    data_abate = models.DateField()
    gta = models.CharField(max_length=50)
    
    # Campos de avaliação
    status_avaliacao = models.CharField(
        max_length=20, 
        choices=STATUS_AVALIACAO_CHOICES, 
        default='nao_avaliado'
    )
    data_avaliacao = models.DateTimeField(null=True, blank=True)
    
    # Detalhes da avaliação - Vísceras Vermelhas
    condicao_geral = models.CharField(max_length=50, blank=True, null=True)
    carcassa = models.CharField(max_length=50, blank=True, null=True)
    figado = models.CharField(max_length=50, blank=True, null=True)
    coracao = models.CharField(max_length=50, blank=True, null=True)
    pulmoes = models.CharField(max_length=50, blank=True, null=True)
    rins = models.CharField(max_length=50, blank=True, null=True)
    diafragma = models.CharField(max_length=50, blank=True, null=True)
    lingua = models.CharField(max_length=50, blank=True, null=True)
    cabeca = models.CharField(max_length=50, blank=True, null=True)
    
    # Detalhes da avaliação - Vísceras Brancas
    utero = models.CharField(max_length=50, blank=True, null=True)
    baco_pancreas = models.CharField(max_length=50, blank=True, null=True)
    intestino_estomagos_bexiga = models.CharField(max_length=50, blank=True, null=True)
    glandula_mamaria = models.CharField(max_length=50, blank=True, null=True)
    
    observacoes_avaliacao = models.TextField(blank=True, null=True)
    
    # Campos de classificação
    tipo_animal = models.CharField(max_length=20, choices=TIPO_ANIMAL_CHOICES, null=True, blank=True)
    qualidade = models.CharField(max_length=20, choices=QUALIDADE_CHOICES, null=True, blank=True)
    data_classificacao = models.DateTimeField(null=True, blank=True)
    
    # Ordem de abate
    ordem_abate = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.numero_brinco
    
    class Meta:
        verbose_name = "Bovino"
        verbose_name_plural = "Bovinos"


class MeiaCarcaça(models.Model):
    LADO_CHOICES = [
        ('esquerda', 'Esquerda'),
        ('direita', 'Direita'),
    ]
    
    bovino = models.ForeignKey(Bovino, on_delete=models.CASCADE)
    lado = models.CharField(max_length=10, choices=LADO_CHOICES)
    posicao_trilho = models.CharField(max_length=10)
    posicao_gancho = models.IntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    data_entrada_estoque = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        # Verificar se já existe uma meia carcaça nessa posição
        if MeiaCarcaça.objects.exclude(pk=self.pk).filter(
            posicao_trilho=self.posicao_trilho,
            posicao_gancho=self.posicao_gancho
        ).exists():
            raise ValidationError(
                f'Já existe uma meia carcaça no trilho {self.posicao_trilho} e gancho {self.posicao_gancho}.'
            )
        
        # Verificar se o peso foi fornecido
        if not self.peso:
            raise ValidationError('O peso é obrigatório para inserir no estoque.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.bovino.numero_brinco} - {self.lado} - Trilho {self.posicao_trilho} Gancho {self.posicao_gancho}'
    
    class Meta:
        verbose_name = "Meia Carcaça"
        verbose_name_plural = "Meias Carcaças"
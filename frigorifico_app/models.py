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
        ('Condenação Total', 'Condenação Total'),
        ('Condenação Parcial', 'Condenação Parcial'),
        ('Em Inspeção', 'Em Inspeção'),
        ('Aprovado', 'Aprovado'),

    ]
    
    CARCASSA_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Abscesso', 'Abscesso'),
        ('Cisticercose Calcificada', 'Cisticercose Calcificada'),
        ('Cisticercose Viva', 'Cisticercose Viva'),
        ('Hemorragias', 'Hemorragias'),
        ('Cont. Gastro/biliar', 'Cont. Gastro/biliar'),
        ('Aderência', 'Aderência'),
        ('Artrite', 'Artrite'),
        ('Aspecto Repugnante', 'Aspecto Repugnante'),
        ('Neoplasia', 'Neoplasia'),
        ('Magreza', 'Magreza'),
        ('Evisceração Retardada', 'Evisceração Retardada'),
        ('Contusão/Fratura', 'Contusão/Fratura'),
        ('Icterícia', 'Icterícia'),
        ('Adenite', 'Adenite'),

    ]
    
    FIGADO_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Abcessos Múltiplos', 'Abcessos Múltiplos'),
        ('Cirrose', 'Cirrose'),
        ('Congestão/Teleangiectasia', 'Congestão/Teleangiectasia'),
        ('Faciolose', 'Faciolose'),
        ('Contaminação Biliar', 'Contaminação Biliar'),
        ('Perihepatite', 'Perihepatite'),
        ('Cisticercose Viva', 'Cisticercose Viva'),
        ('Cisticercose Calcificada', 'Cisticercose Calcificada'),
        ('Hidatidose', 'Hidatidose'),

    ]
    
    CORACAO_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Cisticercose Calcificada', 'Cisticercose Calcificada'),
        ('Cisticercose Viva', 'Cisticercose Viva'),
        ('Pericardite', 'Pericardite'),
        ('Endocardite', 'Endocardite'),
        ('Hidatidose', 'Hidatidose'),
        ('Melanose', 'Melanose'),
        ('Sarcosporidiose', 'Sarcosporidiose'),
    ]
    
    PULMOES_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Aspiração Sangue', 'Aspiração Sangue'),
        ('Apiração de Vomito', 'Apiração de Vomito'),
        ('Aderência', 'Aderência'),
        ('Pleuropneumonia Abscesso', 'Pleuropneumonia Abscesso'),
        ('Bronquite', 'Bronquite'),
        ('Enfisema', 'Enfisema'),
        ('Hidatidose', 'Hidatidose'),
        ('Tuberculose(lesão sugestiva)', 'Tuberculose(lesão sugestiva)'),
        ('Neoplasia', 'Neoplasia'),
        ('Melanose', 'Melanose'),

    ]
    
    RINS_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Cisto Urinário', 'Cisto Urinário'),
        ('Calculo Renal', 'Calculo Renal'),
        ('Congestão/Teleangiectasia', 'Congestão/Teleangiectasia'),
        ('Neoplasia', 'Neoplasia'),
        ('Hidronefrose/Uronefrose', 'Hidronefrose/Uronefrose'),
        ('Nefrite', 'Nefrite'),

    ]
    
    DIAFRAGMA_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Aderência', 'Aderência'),
        ('Cisticercose Calcificada', 'Cisticercose Calcificada'),
        ('Cisticercose Viva', 'Cisticercose Viva'),
        ('Cisticercose', 'Cisticercose'),
        ('Perihepatite', 'Perihepatite'),
        ('Icterícia', 'Icterícia'),
        ('Sarcosporidiose', 'Sarcosporidiose'),
    ]
    
    LINGUA_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Cont. Gastro/Biliar', 'Cont. Gastro/Biliar'),
        ('Cisticercose Calcificada', 'Cisticercose Calcificada'),
        ('Cisticercose Viva', 'Cisticercose Viva'),
        ('Actinobacilose', 'Actinobacilose'),

    ]
    
    CABECA_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Cont. Gastro/Biliar', 'Cont. Gastro/Biliar'),
        ('Cisticercose Calcificada', 'Cisticercose Calcificada'),
        ('Cisticercose Viva', 'Cisticercose Viva'),
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
        ('Tuberculose(Lesão Sugestiva)', 'Tuberculose(Lesão Sugestiva)'),
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
    carcassa = models.CharField(
        max_length=50,
        choices=CARCASSA_CHOICES,
        blank=True,
        null=True,
        verbose_name="Carcaça"
    )
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
    peso = models.DecimalField(max_digits=8, decimal_places=2)
    data_entrada_estoque = models.DateTimeField()
    
    # Campos para venda
    comprador = models.CharField(max_length=100, blank=True, null=True)
    data_venda = models.DateTimeField(blank=True, null=True)
    preco_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Saída do estoque (tirar do trilho libera o gancho para outro uso)
    data_saida_estoque = models.DateTimeField(blank=True, null=True)
    
    def esta_em_estoque(self):
        """True se ainda ocupa o gancho no trilho (não foi dada saída)."""
        return self.data_saida_estoque is None
    
    def clean(self):
        # Verificar se já existe uma meia carcaça nessa posição (apenas as que ainda estão em estoque)
        queryset = MeiaCarcaça.objects.filter(
            posicao_trilho=self.posicao_trilho,
            posicao_gancho=self.posicao_gancho,
            data_saida_estoque__isnull=True
        ).exclude(pk=self.pk)
        if queryset.exists():
            raise ValidationError(f"Já existe uma meia carcaça no trilho {self.posicao_trilho} e gancho {self.posicao_gancho}")

        # Verificar se o peso foi fornecido
        if not self.peso:
            raise ValidationError('O peso é obrigatório para inserir no estoque.')

        # Garantir que a data de venda seja registrada corretamente ao vender
        if self.comprador and not self.data_venda:
            raise ValidationError('A data de venda deve ser preenchida quando um comprador é informado.')
        if not self.comprador and self.data_venda:
            # Se não houver comprador, a data de venda deve ser None
            self.data_venda = None

    def esta_vendida(self):
        return self.data_venda is not None
    
    def save(self, *args, **kwargs):
        # Define a data de entrada no estoque como a hora atual se não estiver definida
        if not self.data_entrada_estoque:
            self.data_entrada_estoque = timezone.now()
            
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.bovino.numero_brinco} - {self.get_lado_display()} - Trilho {self.posicao_trilho} Gancho {self.posicao_gancho}"
    
    class Meta:
        verbose_name = "Meia Carcaça"
        verbose_name_plural = "Meias Carcaças"
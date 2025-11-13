from django.db import models

class Bovino(models.Model):
    SEXO_CHOICES = [
        ('macho', 'Macho'),
        ('femea', 'Fêmea'),
    ]
    
    numero_brinco = models.CharField(
        max_length=50, 
        verbose_name="Número do Brinco",
        unique=True
    )
    nome_produtor = models.CharField(max_length=100, verbose_name="Nome do Produtor")
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, verbose_name="Sexo")
    data_abate = models.DateField(verbose_name="Data de Abate")
    gta = models.CharField(max_length=50, verbose_name="Número do GTA")
    
    # Campos para avaliação
    AVALIACAO_STATUS = [
        ('nao_avaliado', 'Não Avaliado'),
        ('apto', 'Apto para Comercialização'),
        ('inapto', 'Inapto para Comercialização'),
    ]
    
    status_avaliacao = models.CharField(
        max_length=20,
        choices=AVALIACAO_STATUS,
        default='nao_avaliado',
        verbose_name="Status da Avaliação"
    )
    
    observacoes_avaliacao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações da Avaliação"
    )
    
    data_avaliacao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data da Avaliação"
    )
    
    # Campos para avaliação detalhada - Vísceras Vermelhas (já existentes)
    CONDICAO_GERAL_CHOICES = [
        ("Condenação Total", "Condenação Total"),
        ("Condenação Parcial", "Condenação Parcial"),
        ("Em Inspeção", "Em Inspeção"),
        ("Aprovado", "Aprovado")
    ]
    
    CARCASSA_CHOICES = [
        ("Abcessos", "Abcessos"),
        ("Cisticercose Calcificada", "Cisticercose Calcificada"),
        ("Cisticercose Viva", "Cisticercose Viva"),
        ("Hemorragias", "Hemorragias"),
        ("Cont. Gastro/biliar", "Cont. Gastro/biliar"),
        ("Aderência", "Aderência"),
        ("Artrite", "Artrite"),
        ("Aspecto Repugnante", "Aspecto Repugnante"),
        ("Neoplasia", "Neoplasia"),
        ("Magreza", "Magreza"),
        ("Evisceração Retardada", "Evisceração Retardada"),
        ("Falha Tecnológica", "Falha Tecnológica"),
        ("Caqueixa", "Caqueixa"),
        ("Sarcosporidiose", "Sarcosporidiose"),
        ("Contusão/Fratura", "Contusão/Fratura"),
        ("Icterícia", "Icterícia"),
        ("Adenite", "Adenite"),
        ("Aprovado", "Aprovado")
    ]
    
    FIGADO_CHOICES = [
        ("Abcessos Múltiplos", "Abcessos Múltiplos"),
        ("Cirrose", "Cirrose"),
        ("Congestão/Teleangiectasia", "Congestão/Teleangiectasia"),
        ("Faciolose", "Faciolose"),
        ("Contaminação Biliar", "Contaminação Biliar"),
        ("Perihepatite", "Perihepatite"),
        ("Cisticercose Calcificada", "Cisticercose Calcificada"),
        ("Cisticercose Viva", "Cisticercose Viva"),
        ("Hidatose", "Hidatose"),
        ("Aprovado", "Aprovado")
    ]
    
    CORACAO_CHOICES = [
        ("Cisticercose Calcificada", "Cisticercose Calcificada"),
        ("Cisticercose Viva", "Cisticercose Viva"),
        ("Pericardite", "Pericardite"),
        ("Endocardite", "Endocardite"),
        ("Hidatose", "Hidatose"),
        ("Melanose", "Melanose"),
        ("Sarcosporidiose", "Sarcosporidiose"),
        ("Aprovado", "Aprovado")
    ]
    
    PULMOES_CHOICES = [
        ("Aspiração Sangue", "Aspiração Sangue"),
        ("Aparição de Vômito", "Aparição de Vômito"),
        ("Aderência", "Aderência"),
        ("Pluropneumoia", "Pluropneumoia"),
        ("Atelectasia", "Atelectasia"),
        ("Bronquite", "Bronquite"),
        ("Enfisema", "Enfisema"),
        ("Hidatidose", "Hidatidose"),
        ("Tuberculose (Lesão Sugestiva)", "Tuberculose (Lesão Sugestiva)"),
        ("Neoplasia", "Neoplasia"),
        ("Melanose", "Melanose"),
        ("Aprovado", "Aprovado")
    ]
    
    RINS_CHOICES = [
        ("Cisto Urinário", "Cisto Urinário"),
        ("Cálculo Renal", "Cálculo Renal"),
        ("Congestão/Teleangiectasia", "Congestão/Teleangiectasia"),
        ("Neoplasia", "Neoplasia"),
        ("Hidronefrose/Uronefrose", "Hidronefrose/Uronefrose"),
        ("Nefrite", "Nefrite"),
        ("Aprovado", "Aprovado")
    ]
    
    DIAFRAGMA_CHOICES = [
        ("Aderência", "Aderência"),
        ("Parasita", "Parasita"),
        ("Cisticercose Calcificada", "Cisticercose Calcificada"),
        ("Cisticercose Viva", "Cisticercose Viva"),
        ("Perihepatite", "Perihepatite"),
        ("Icterícia", "Icterícia"),
        ("Sarcosporidiose", "Sarcosporidiose"),
        ("Aprovado", "Aprovado")
    ]
    
    LINGUA_CHOICES = [
        ("Cont. Gastro Biliar", "Cont. Gastro Biliar"),
        ("Cisticercose Calcificada", "Cisticercose Calcificada"),
        ("Cisticercose Viva", "Cisticercose Viva"),
        ("Actinobacilose", "Actinobacilose"),
        ("Aprovado", "Aprovado")
    ]
    
    CABECA_CHOICES = [
        ("Cont. Gastro Biliar", "Cont. Gastro Biliar"),
        ("Cisticercose Calcificada", "Cisticercose Calcificada"),
        ("Cisticercose Viva", "Cisticercose Viva"),
        ("Aprovado", "Aprovado")
    ]
    
    # Campos para avaliação detalhada - Vísceras Brancas (novos)
    UTERO_CHOICES = [
        ("Gestação Adiantada", "Gestação Adiantada"),
        ("Metrite", "Metrite"),
        ("Abscesso", "Abscesso"),
        ("Prenha", "Prenha"),
        ("Aprovado", "Aprovado")
    ]
    
    BAÇO_PANCREAS_CHOICES = [
        ("Abscesso", "Abscesso"),
        ("Aspecto repugnante", "Aspecto repugnante"),
        ("Esplenomegalia", "Esplenomegalia"),
        ("Euritrema", "Euritrema"),
        ("Aderencia", "Aderencia"),
        ("Aprovado", "Aprovado")
    ]
    
    INTESTINO_ESTOMAGOS_BEXIGA_CHOICES = [
        ("Abscessos", "Abscessos"),
        ("Enterite", "Enterite"),
        ("Peritonite", "Peritonite"),
        ("Tuberculose (Lesão Sugestiva)", "Tuberculose (Lesão Sugestiva)"),
        ("Linfadenite", "Linfadenite"),
        ("Adenite", "Adenite"),
        ("Parasitoses transmissiveis", "Parasitoses transmissiveis"),
        ("Esofagostomose", "Esofagostomose"),
        ("Neoplasia", "Neoplasia"),
        ("Aprovado", "Aprovado")
    ]
    
    GLANDULA_MAMARIA_CHOICES = [
        ("Adenite", "Adenite"),
        ("Mastite", "Mastite"),
        ("Miiase", "Miiase"),
        ("Aspecto repugante", "Aspecto repugante"),
        ("Aprovado", "Aprovado")
    ]
    
    # Campos de avaliação detalhada - Vísceras Vermelhas (já existentes)
    condicao_geral = models.CharField(
        max_length=50,
        choices=CONDICAO_GERAL_CHOICES,
        blank=True,
        null=True,
        verbose_name="Condição Geral"
    )
    
    carcassa = models.CharField(
        max_length=50,
        choices=CARCASSA_CHOICES,
        blank=True,
        null=True,
        verbose_name="Carcassa"
    )
    
    figado = models.CharField(
        max_length=50,
        choices=FIGADO_CHOICES,
        blank=True,
        null=True,
        verbose_name="Fígado"
    )
    
    coracao = models.CharField(
        max_length=50,
        choices=CORACAO_CHOICES,
        blank=True,
        null=True,
        verbose_name="Coração"
    )
    
    pulmoes = models.CharField(
        max_length=50,
        choices=PULMOES_CHOICES,
        blank=True,
        null=True,
        verbose_name="Pulmões"
    )
    
    rins = models.CharField(
        max_length=50,
        choices=RINS_CHOICES,
        blank=True,
        null=True,
        verbose_name="Rins"
    )
    
    diafragma = models.CharField(
        max_length=50,
        choices=DIAFRAGMA_CHOICES,
        blank=True,
        null=True,
        verbose_name="Diafragma"
    )
    
    lingua = models.CharField(
        max_length=50,
        choices=LINGUA_CHOICES,
        blank=True,
        null=True,
        verbose_name="Língua"
    )
    
    cabeca = models.CharField(
        max_length=50,
        choices=CABECA_CHOICES,
        blank=True,
        null=True,
        verbose_name="Cabeça"
    )
    
    # Campos de avaliação detalhada - Vísceras Brancas (novos)
    utero = models.CharField(
        max_length=50,
        choices=UTERO_CHOICES,
        blank=True,
        null=True,
        verbose_name="Útero"
    )
    
    baco_pancreas = models.CharField(
        max_length=50,
        choices=BAÇO_PANCREAS_CHOICES,
        blank=True,
        null=True,
        verbose_name="Baço/Pancreas"
    )
    
    intestino_estomagos_bexiga = models.CharField(
        max_length=50,
        choices=INTESTINO_ESTOMAGOS_BEXIGA_CHOICES,
        blank=True,
        null=True,
        verbose_name="Intestino/Estômagos/Bexiga"
    )
    
    glandula_mamaria = models.CharField(
        max_length=50,
        choices=GLANDULA_MAMARIA_CHOICES,
        blank=True,
        null=True,
        verbose_name="Glândula Mamária"
    )
    
    # Campos para classificação
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
    
    tipo_animal = models.CharField(
        max_length=20,
        choices=TIPO_ANIMAL_CHOICES,
        blank=True,
        null=True,
        verbose_name="Tipo do Animal"
    )
    
    qualidade = models.CharField(
        max_length=20,
        choices=QUALIDADE_CHOICES,
        blank=True,
        null=True,
        verbose_name="Qualidade"
    )
    
    peso = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Peso (kg)"
    )
    
    data_classificacao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data da Classificação"
    )
    
    def __str__(self):
        return f"Brinco: {self.numero_brinco} - Produtor: {self.nome_produtor}"
    
    class Meta:
        verbose_name = "Bovino"
        verbose_name_plural = "Bovinos"


class MeiaCarcaça(models.Model):
    LADO_CHOICES = [
        ('esquerda', 'Esquerda'),
        ('direita', 'Direita'),
    ]
    
    bovino = models.ForeignKey(Bovino, on_delete=models.CASCADE, verbose_name="Bovino")
    lado = models.CharField(max_length=10, choices=LADO_CHOICES, verbose_name="Lado da Carcaça")
    
    # Campos para estoque (câmara fria)
    posicao_trilho = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Posição do Trilho"
    )
    
    posicao_gancho = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Posição do Gancho"
    )
    
    peso = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Peso (kg)"
    )
    
    data_entrada_estoque = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Entrada no Estoque"
    )
    
    def __str__(self):
        return f"{self.bovino.numero_brinco} - {self.lado}"
    
    class Meta:
        verbose_name = "Meia Carcaça"
        verbose_name_plural = "Meias Carcaças"
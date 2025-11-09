from django.contrib import admin
from .models import Bovino, MeiaCarcaça

class MeiaCarcaçaInline(admin.TabularInline):
    model = MeiaCarcaça
    extra = 0
    readonly_fields = ('lado', 'posicao_trilho', 'posicao_gancho', 'data_entrada_estoque')

@admin.register(Bovino)
class BovinoAdmin(admin.ModelAdmin):
    list_display = ('numero_brinco', 'nome_produtor', 'sexo', 'data_abate', 'status_avaliacao', 'tipo_animal', 'qualidade')
    list_filter = ('sexo', 'status_avaliacao', 'tipo_animal', 'qualidade', 'data_abate')
    search_fields = ('numero_brinco', 'nome_produtor', 'gta')
    readonly_fields = ('data_avaliacao', 'data_classificacao')
    inlines = [MeiaCarcaçaInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('numero_brinco', 'nome_produtor', 'sexo', 'data_abate', 'gta')
        }),
        ('Avaliação', {
            'fields': (
                'status_avaliacao', 'condicao_geral', 'carcassa', 'figado', 
                'coracao', 'pulmoes', 'rins', 'diafragma', 'lingua', 'cabeca',
                'observacoes_avaliacao', 'data_avaliacao'
            )
        }),
        ('Classificação', {
            'fields': (
                'tipo_animal', 'qualidade', 'peso', 'data_classificacao'
            )
        }),
    )

@admin.register(MeiaCarcaça)
class MeiaCarcaçaAdmin(admin.ModelAdmin):
    list_display = ('bovino', 'lado', 'posicao_trilho', 'posicao_gancho', 'data_entrada_estoque')
    list_filter = ('lado', 'posicao_trilho')
    search_fields = ('bovino__numero_brinco', 'bovino__nome_produtor')
    readonly_fields = ('data_entrada_estoque',)
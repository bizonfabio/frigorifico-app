from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.utils import timezone
from .models import Bovino, MeiaCarcaça
from datetime import date

def home(request):
    # Se for POST, significa que o usuário selecionou uma data
    if request.method == 'POST':
        data_selecionada = request.POST.get('data_selecionada')
        if data_selecionada:
            # Filtrar animais pela data selecionada
            animais = Bovino.objects.filter(data_abate=data_selecionada)
        else:
            # Se não houver data, mostrar todos os animais
            animais = Bovino.objects.all()
            data_selecionada = "Todos"
    else:
        # Por padrão, mostrar animais com data de hoje
        data_selecionada = date.today()
        animais = Bovino.objects.filter(data_abate=data_selecionada)
    
    # Contar total de animais
    total_animais = animais.count()
    
    contexto = {
        'animais': animais,
        'total_animais': total_animais,
        'data_selecionada': data_selecionada,
    }
    
    return render(request, 'frigorifico_app/home.html', contexto)

def registrar_gta(request):
    if request.method == 'POST':
        gta = request.POST.get('gta')
        quantidade = int(request.POST.get('quantidade'))
        
        # Salvar os dados em sessão para uso na próxima etapa
        request.session['gta'] = gta
        request.session['quantidade'] = quantidade
        
        # Redirecionar para a página de registro dos animais
        return redirect('registrar_animais')
    
    return render(request, 'frigorifico_app/registrar_gta.html')

def registrar_animais(request):
    if request.method == 'POST':
        # Pegar dados do formulário
        quantidade = request.session.get('quantidade', 0)
        gta = request.session.get('gta', '')
        
        # Verificar se temos os dados necessários
        if not gta or quantidade <= 0:
            messages.error(request, 'Dados inválidos. Por favor, comece novamente.')
            return redirect('registro_inicial')
        
        # Coletar todos os dados dos animais
        animais_data = []
        brincos_existentes = []
        
        # Verificar se há brincos já existentes no banco de dados
        for i in range(quantidade):
            numero_brinco = request.POST.get(f'numero_brinco_{i}')
            
            # Verificar se o brinco já existe no banco de dados
            if Bovino.objects.filter(numero_brinco=numero_brinco).exists():
                if numero_brinco not in brincos_existentes:
                    brincos_existentes.append(numero_brinco)
            
            # Coletar dados do animal
            animais_data.append({
                'numero_brinco': numero_brinco,
                'nome_produtor': request.POST.get(f'nome_produtor_{i}'),
                'sexo': request.POST.get(f'sexo_{i}'),
                'data_abate': request.POST.get(f'data_abate_{i}'),
            })
        
        # Se houver brincos já existentes no banco, não registrar nenhum
        if brincos_existentes:
            contexto = {
                'gta': gta,
                'quantidade': quantidade,
                'range_quantidade': range(quantidade),
                'animais_data': animais_data,
                'brincos_existentes': brincos_existentes
            }
            
            messages.error(request, 'Não foi possível registrar os animais. Verifique os números dos brincos.')
            return render(request, 'frigorifico_app/registrar_animais.html', contexto)
        
        # Registrar todos os animais se não houver conflitos
        try:
            for animal_data in animais_data:
                Bovino.objects.create(
                    numero_brinco=animal_data['numero_brinco'],
                    nome_produtor=animal_data['nome_produtor'],
                    sexo=animal_data['sexo'],
                    data_abate=animal_data['data_abate'],
                    gta=gta
                )
            
            # Limpar a sessão
            request.session.flush()
            
            # Preparar dados para a página de sucesso
            contexto = {
                'gta': gta,
                'quantidade': quantidade
            }
            
            messages.success(request, f'{quantidade} animal(is) registrado(s) com sucesso!')
            return render(request, 'frigorifico_app/sucesso.html', contexto)
            
        except IntegrityError:
            # Em caso de erro inesperado, mostrar mensagem de erro
            contexto = {
                'gta': gta,
                'quantidade': quantidade,
                'range_quantidade': range(quantidade),
                'animais_data': animais_data
            }
            
            messages.error(request, 'Erro ao registrar animais. Por favor, tente novamente.')
            return render(request, 'frigorifico_app/registrar_animais.html', contexto)
    
    # Método GET - mostrar formulário
    gta = request.session.get('gta', '')
    quantidade = request.session.get('quantidade', 0)
    
    # Verificar se temos os dados necessários
    if not gta or quantidade <= 0:
        return redirect('registro_inicial')
    
    contexto = {
        'gta': gta,
        'quantidade': quantidade,
        'range_quantidade': range(quantidade)
    }
    
    return render(request, 'frigorifico_app/registrar_animais.html', contexto)

def registro_inicial(request):
    return render(request, 'frigorifico_app/registro_inicial.html')

def lista_animais_para_avaliacao(request):
    # Mostrar apenas animais que ainda não foram avaliados
    animais = Bovino.objects.filter(status_avaliacao='nao_avaliado')
    
    contexto = {
        'animais': animais
    }
    
    return render(request, 'frigorifico_app/lista_animais_avaliacao.html', contexto)

def avaliar_animal(request, id):
    animal = get_object_or_404(Bovino, id=id)
    
    # Definir as opções para cada parte do animal
    opcoes = {
        # Vísceras Vermelhas (já existentes)
        'condicao_geral': Bovino.CONDICAO_GERAL_CHOICES,
        'carcassa': Bovino.CARCASSA_CHOICES,
        'figado': Bovino.FIGADO_CHOICES,
        'coracao': Bovino.CORACAO_CHOICES,
        'pulmoes': Bovino.PULMOES_CHOICES,
        'rins': Bovino.RINS_CHOICES,
        'diafragma': Bovino.DIAFRAGMA_CHOICES,
        'lingua': Bovino.LINGUA_CHOICES,
        'cabeca': Bovino.CABECA_CHOICES,
        # Vísceras Brancas (novas)
        'utero': Bovino.UTERO_CHOICES,
        'baco_pancreas': Bovino.BAÇO_PANCREAS_CHOICES,
        'intestino_estomagos_bexiga': Bovino.INTESTINO_ESTOMAGOS_BEXIGA_CHOICES,
        'glandula_mamaria': Bovino.GLANDULA_MAMARIA_CHOICES,
    }
    
    if request.method == 'POST':
        # Salvar avaliação detalhada - Vísceras Vermelhas
        animal.condicao_geral = request.POST.get('condicao_geral')
        animal.carcassa = request.POST.get('carcassa')
        animal.figado = request.POST.get('figado')
        animal.coracao = request.POST.get('coracao')
        animal.pulmoes = request.POST.get('pulmoes')
        animal.rins = request.POST.get('rins')
        animal.diafragma = request.POST.get('diafragma')
        animal.lingua = request.POST.get('lingua')
        animal.cabeca = request.POST.get('cabeca')
        
        # Salvar avaliação detalhada - Vísceras Brancas
        animal.utero = request.POST.get('utero')
        animal.baco_pancreas = request.POST.get('baco_pancreas')
        animal.intestino_estomagos_bexiga = request.POST.get('intestino_estomagos_bexiga')
        animal.glandula_mamaria = request.POST.get('glandula_mamaria')
        
        animal.observacoes_avaliacao = request.POST.get('observacoes_avaliacao')
        
        # Determinar status da avaliação com base nas seleções
        # Se alguma parte tiver uma condição diferente de "Aprovado", o animal é inapto
        partes_vermelhas = [animal.condicao_geral, animal.carcassa, animal.figado, animal.coracao,
                            animal.pulmoes, animal.rins, animal.diafragma, animal.lingua, animal.cabeca]
        
        partes_brancas = [animal.utero, animal.baco_pancreas, animal.intestino_estomagos_bexiga, 
                          animal.glandula_mamaria]
        
        # Verificar se alguma parte (vermelha ou branca) foi condenada
        if any(parte and parte != "Aprovado" for parte in partes_vermelhas + partes_brancas):
            animal.status_avaliacao = 'inapto'
        else:
            animal.status_avaliacao = 'apto'
        
        animal.data_avaliacao = timezone.now()
        animal.save()
        
        messages.success(request, f'Avaliação do animal {animal.numero_brinco} registrada com sucesso!')
        return redirect('lista_animais_para_avaliacao')
    
    contexto = {
        'animal': animal,
        'opcoes': opcoes
    }
    
    return render(request, 'frigorifico_app/avaliar_animal.html', contexto)

def lista_animais_para_classificacao(request):
    # Mostrar apenas animais que foram avaliados como aptos
    animais = Bovino.objects.filter(status_avaliacao='apto', tipo_animal__isnull=True)
    
    contexto = {
        'animais': animais
    }
    
    return render(request, 'frigorifico_app/lista_animais_classificacao.html', contexto)

def classificar_animal(request, id):
    animal = get_object_or_404(Bovino, id=id)
    
    # Verificar se o animal foi aprovado na avaliação
    if animal.status_avaliacao != 'apto':
        messages.error(request, 'Apenas animais aprovados na avaliação podem ser classificados.')
        return redirect('lista_animais_para_classificacao')
    
    if request.method == 'POST':
        # Salvar dados de classificação
        animal.tipo_animal = request.POST.get('tipo_animal')
        animal.qualidade = request.POST.get('qualidade')
        peso_str = request.POST.get('peso')
        
        # Converter peso para decimal
        if peso_str:
            try:
                animal.peso = float(peso_str.replace(',', '.'))
            except ValueError:
                messages.error(request, 'Peso inválido. Use apenas números.')
                contexto = {
                    'animal': animal,
                    'tipo_animal_choices': Bovino.TIPO_ANIMAL_CHOICES,
                    'qualidade_choices': Bovino.QUALIDADE_CHOICES
                }
                return render(request, 'frigorifico_app/classificar_animal.html', contexto)
        
        animal.data_classificacao = timezone.now()
        animal.save()
        
        messages.success(request, f'Classificação do animal {animal.numero_brinco} registrada com sucesso!')
        return redirect('lista_animais_para_classificacao')
    
    contexto = {
        'animal': animal,
        'tipo_animal_choices': Bovino.TIPO_ANIMAL_CHOICES,
        'qualidade_choices': Bovino.QUALIDADE_CHOICES
    }
    
    return render(request, 'frigorifico_app/classificar_animal.html', contexto)

def lista_animais_para_estoque(request):
    # Mostrar apenas animais que foram classificados e ainda não estão no estoque
    animais = Bovino.objects.filter(
        status_avaliacao='apto',
        tipo_animal__isnull=False,
        meiacarcaça__isnull=True
    ).distinct()
    
    contexto = {
        'animais': animais
    }
    
    return render(request, 'frigorifico_app/lista_animais_estoque.html', contexto)

def enviar_para_estoque(request, id):
    animal = get_object_or_404(Bovino, id=id)
    
    # Verificar se o animal foi classificado
    if not animal.tipo_animal or not animal.qualidade:
        messages.error(request, 'Apenas animais classificados podem ser enviados para o estoque.')
        return redirect('lista_animais_para_estoque')
    
    if request.method == 'POST':
        # Obter dados do formulário
        trilho = request.POST.get('trilho')
        gancho_inicio = int(request.POST.get('gancho_inicio', 1))
        
        # Calcular peso de cada meia carcaça (50% do peso total do animal)
        peso_meia = None
        if animal.peso:
            peso_meia = animal.peso / 2
        
        # Criar meia carcaça esquerda
        MeiaCarcaça.objects.create(
            bovino=animal,
            lado='esquerda',
            posicao_trilho=trilho,
            posicao_gancho=gancho_inicio,
            peso=peso_meia,
            data_entrada_estoque=timezone.now()
        )
        
        # Criar meia carcaça direita
        MeiaCarcaça.objects.create(
            bovino=animal,
            lado='direita',
            posicao_trilho=trilho,
            posicao_gancho=gancho_inicio + 1,
            peso=peso_meia,
            data_entrada_estoque=timezone.now()
        )
        
        messages.success(request, f'Animal {animal.numero_brinco} enviado para o estoque com sucesso!')
        return redirect('lista_animais_para_estoque')
    
    contexto = {
        'animal': animal
    }
    
    return render(request, 'frigorifico_app/enviar_para_estoque.html', contexto)

def visualizar_estoque(request):
    # Obter todas as meias carcaças no estoque
    meias_carcaças = MeiaCarcaça.objects.select_related('bovino').all().order_by('posicao_trilho', 'posicao_gancho')
    
    contexto = {
        'meias_carcaças': meias_carcaças
    }
    
    return render(request, 'frigorifico_app/visualizar_estoque.html', contexto)

def pesquisar_estoque(request):
    # Inicializar variáveis
    meias_carcaças = MeiaCarcaça.objects.none()
    pesquisa_realizada = False
    
    if request.method == 'POST':
        # Obter parâmetros de pesquisa
        tipo = request.POST.get('tipo')
        qualidade = request.POST.get('qualidade')
        peso_min = request.POST.get('peso_min')
        peso_max = request.POST.get('peso_max')
        
        # Construir consulta
        meias_carcaças = MeiaCarcaça.objects.select_related('bovino').all()
        
        if tipo:
            meias_carcaças = meias_carcaças.filter(bovino__tipo_animal=tipo)
        
        if qualidade:
            meias_carcaças = meias_carcaças.filter(bovino__qualidade=qualidade)
        
        if peso_min:
            meias_carcaças = meias_carcaças.filter(peso__gte=peso_min)
        
        if peso_max:
            meias_carcaças = meias_carcaças.filter(peso__lte=peso_max)
        
        meias_carcaças = meias_carcaças.order_by('posicao_trilho', 'posicao_gancho')
        pesquisa_realizada = True
    
    contexto = {
        'meias_carcaças': meias_carcaças,
        'tipos': Bovino.TIPO_ANIMAL_CHOICES,
        'qualidades': Bovino.QUALIDADE_CHOICES,
        'pesquisa_realizada': pesquisa_realizada
    }
    
    return render(request, 'frigorifico_app/pesquisar_estoque.html', contexto)
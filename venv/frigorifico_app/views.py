from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, models
from django.utils import timezone
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import Bovino, MeiaCarcaça
from datetime import date
from decimal import Decimal
import json


@login_required
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


@login_required
def registro_inicial(request):
    return render(request, 'frigorifico_app/registro_inicial.html')


@login_required
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


@login_required
def registrar_animais(request):
    if request.method == 'POST':
        # Pegar dados do formulário
        quantidade = request.session.get('quantidade', 0)
        gta = request.session.get('gta', '')
        
        # Verificar se temos os dados necessários
        if not gta or quantidade <= 0:
            messages.error(request, 'Dados inválidos. Por favor, comece novamente.')
            return redirect('registro_inicial')
        
        # Lista para armazenar animais que deram erro
        animais_com_erro = []
        animais_registrados = 0
        data_abate_referencia = None
        
        # Processar cada animal
        for i in range(quantidade):
            numero_brinco = request.POST.get(f'numero_brinco_{i}')
            nome_produtor = request.POST.get(f'nome_produtor_{i}')
            sexo = request.POST.get(f'sexo_{i}')
            data_abate = request.POST.get(f'data_abate_{i}')
            
            # Guardar a data de abate do primeiro animal como referência
            if i == 0:
                data_abate_referencia = data_abate
            
            # Criar instância do modelo Bovino
            bovino = Bovino(
                numero_brinco=numero_brinco,
                nome_produtor=nome_produtor,
                sexo=sexo,
                data_abate=data_abate,
                gta=gta
            )
            
            try:
                bovino.save()
                animais_registrados += 1
            except IntegrityError:
                # Se houver erro de integridade (brinco duplicado), adicionar à lista de erros
                animais_com_erro.append({
                    'numero': i + 1,
                    'brinco': numero_brinco
                })
        
        # Definir ordem de abate para os animais registrados na mesma data
        if animais_registrados > 0 and data_abate_referencia:
            # Obter o maior valor de ordem_abate existente para essa data
            max_ordem = Bovino.objects.filter(data_abate=data_abate_referencia).aggregate(
                models.Max('ordem_abate')
            )['ordem_abate__max'] or 0
            
            # Definir a ordem de abate para os animais recém-registrados
            novos_animais = Bovino.objects.filter(
                data_abate=data_abate_referencia,
                ordem_abate__isnull=True
            ).order_by('id')
            
            for i, animal in enumerate(novos_animais):
                animal.ordem_abate = max_ordem + i + 1
                animal.save()
        
        # Limpar a sessão
        request.session.flush()
        
        # Mostrar mensagens apropriadas
        if animais_registrados > 0:
            messages.success(request, f'{animais_registrados} animal(is) registrado(s) com sucesso!')
        
        if animais_com_erro:
            mensagem_erro = "Os seguintes animais não foram registrados devido a número de brinco duplicado: "
            for erro in animais_com_erro:
                mensagem_erro += f"Animal {erro['numero']} (Brinco: {erro['brinco']}) "
            messages.error(request, mensagem_erro)
        
        # Preparar dados para a página de sucesso
        contexto = {
            'gta': gta,
            'quantidade': animais_registrados,
            'erros': animais_com_erro
        }
        
        # Renderizar a página de sucesso
        return render(request, 'frigorifico_app/sucesso.html', contexto)
    
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


@login_required
def lista_animais_para_avaliacao(request):
    # Mostrar apenas animais que ainda não foram avaliados, ordenados pela ordem de abate
    animais = Bovino.objects.filter(status_avaliacao='nao_avaliado').order_by('data_abate', 'ordem_abate')
    
    contexto = {
        'animais': animais
    }
    
    return render(request, 'frigorifico_app/lista_animais_avaliacao.html', contexto)


@login_required
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
        
        # Verificar se todas as partes foram avaliadas
        partes_vermelhas = [animal.condicao_geral, animal.carcassa, animal.figado, animal.coracao,
                            animal.pulmoes, animal.rins, animal.diafragma, animal.lingua, animal.cabeca]
        
        partes_brancas = [animal.utero, animal.baco_pancreas, animal.intestino_estomagos_bexiga, 
                          animal.glandula_mamaria]
        
        # Verificar se todas as partes foram preenchidas
        todas_partes_preenchidas = all(partes_vermelhas) and all(partes_brancas)
        
        if not todas_partes_preenchidas:
            messages.error(request, 'Por favor, avalie todas as partes do animal (vísceras vermelhas e brancas) antes de finalizar.')
            contexto = {
                'animal': animal,
                'opcoes': opcoes
            }
            return render(request, 'frigorifico_app/avaliar_animal.html', contexto)
        
        # Determinar status da avaliação com base nas seleções
        # Se alguma parte tiver uma condição diferente de "Aprovado", o animal é inapto
        condenado = False
        for parte in partes_vermelhas + partes_brancas:
            if parte and parte != 'Aprovado':
                condenado = True
                break
        
        # Definir status da avaliação
        if condenado:
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


@login_required
def lista_animais_para_classificacao(request):
    # Mostrar apenas animais que foram avaliados como aptos, ordenados pela ordem de abate
    animais = Bovino.objects.filter(status_avaliacao='apto', tipo_animal__isnull=True).order_by('data_abate', 'ordem_abate')
    
    contexto = {
        'animais': animais
    }
    
    return render(request, 'frigorifico_app/lista_animais_classificacao.html', contexto)


@login_required
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


@login_required
def lista_animais_para_estoque(request):
    # Mostrar apenas animais que foram classificados e ainda não estão no estoque, ordenados pela ordem de abate
    animais = Bovino.objects.filter(
        status_avaliacao='apto',
        tipo_animal__isnull=False,
        meiacarcaça__isnull=True
    ).distinct().order_by('data_abate', 'ordem_abate')
    
    contexto = {
        'animais': animais
    }
    
    return render(request, 'frigorifico_app/lista_animais_estoque.html', contexto)


@login_required
def enviar_para_estoque(request, id):
    animal = get_object_or_404(Bovino, id=id)
    
    # Verificar se o animal foi classificado
    if not animal.tipo_animal or not animal.qualidade:
        messages.error(request, 'Apenas animais classificados podem ser enviados para o estoque.')
        return redirect('lista_animais_para_estoque')
    
    if request.method == 'POST':
        # Obter dados do formulário
        trilho = request.POST.get('trilho')
        gancho_inicio_str = request.POST.get('gancho_inicio')
        peso_str = request.POST.get('peso')
        
        # Validar campos obrigatórios
        if not trilho or not gancho_inicio_str or not peso_str:
            messages.error(request, 'Todos os campos são obrigatórios.')
            contexto = {
                'animal': animal
            }
            return render(request, 'frigorifico_app/enviar_para_estoque.html', contexto)
        
        try:
            gancho_inicio = int(gancho_inicio_str)
            peso = float(peso_str.replace(',', '.'))
            
            # Validar peso positivo
            if peso <= 0:
                messages.error(request, 'O peso deve ser um valor positivo.')
                contexto = {
                    'animal': animal
                }
                return render(request, 'frigorifico_app/enviar_para_estoque.html', contexto)
            
            # Calcular peso de cada meia carcaça (50% do peso total do animal)
            peso_meia = peso / 2
            
            # Criar meia carcaça esquerda
            meia_esquerda = MeiaCarcaça(
                bovino=animal,
                lado='esquerda',
                posicao_trilho=trilho,
                posicao_gancho=gancho_inicio,
                peso=peso_meia,
                data_entrada_estoque=timezone.now()
            )
            meia_esquerda.full_clean()  # Isso chamará o método clean
            meia_esquerda.save()
            
            # Criar meia carcaça direita
            meia_direita = MeiaCarcaça(
                bovino=animal,
                lado='direita',
                posicao_trilho=trilho,
                posicao_gancho=gancho_inicio + 1,
                peso=peso_meia,
                data_entrada_estoque=timezone.now()
            )
            meia_direita.full_clean()  # Isso chamará o método clean
            meia_direita.save()
            
            messages.success(request, f'Animal {animal.numero_brinco} enviado para o estoque com sucesso!')
            return redirect('lista_animais_para_estoque')
            
        except ValueError:
            messages.error(request, 'Valores inválidos fornecidos. Verifique os campos e tente novamente.')
            contexto = {
                'animal': animal
            }
            return render(request, 'frigorifico_app/enviar_para_estoque.html', contexto)
        except ValidationError as e:
            messages.error(request, e.message)
            contexto = {
                'animal': animal
            }
            return render(request, 'frigorifico_app/enviar_para_estoque.html', contexto)
        except Exception as e:
            messages.error(request, f'Erro ao enviar para o estoque: {str(e)}')
            contexto = {
                'animal': animal
            }
            return render(request, 'frigorifico_app/enviar_para_estoque.html', contexto)
    
    contexto = {
        'animal': animal
    }
    
    return render(request, 'frigorifico_app/enviar_para_estoque.html', contexto)


@login_required
def visualizar_estoque(request):
    # Mostrar todas as meias carcaças em estoque, ordenadas por trilho e gancho
    meias_carcaças = MeiaCarcaça.objects.select_related('bovino').order_by('posicao_trilho', 'posicao_gancho')
    
    contexto = {
        'meias_carcaças': meias_carcaças
    }
    
    return render(request, 'frigorifico_app/visualizar_estoque.html', contexto)


@login_required
def pesquisar_estoque(request):
    # Inicializar variáveis
    meias_carcaças = MeiaCarcaça.objects.none()
    pesquisa_realizada = False
    resultados_encontrados = False
    
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
        
        meias_carcaças = meias_carcaças.order_by('bovino__tipo_animal', 'bovino__qualidade', 'peso')
        pesquisa_realizada = True
        resultados_encontrados = meias_carcaças.exists()
    
    contexto = {
        'meias_carcaças': meias_carcaças,
        'tipos': Bovino.TIPO_ANIMAL_CHOICES,
        'qualidades': Bovino.QUALIDADE_CHOICES,
        'pesquisa_realizada': pesquisa_realizada,
        'resultados_encontrados': resultados_encontrados
    }
    
    return render(request, 'frigorifico_app/pesquisar_estoque.html', contexto)


@login_required
def resumo_estoque(request):
    # Obter todas as meias carcaças com seus dados relacionados
    meias_carcaças = MeiaCarcaça.objects.select_related('bovino').all()
    
    # Calcular totais por tipo e qualidade
    from django.db.models import Sum, Count
    resumo = meias_carcaças.values(
        'bovino__tipo_animal', 
        'bovino__qualidade'
    ).annotate(
        total_peso=Sum('peso'),
        quantidade=Count('id')
    ).order_by('bovino__tipo_animal', 'bovino__qualidade')
    
    contexto = {
        'resumo': resumo,
        'tipos': Bovino.TIPO_ANIMAL_CHOICES,
        'qualidades': Bovino.QUALIDADE_CHOICES,
    }
    
    return render(request, 'frigorifico_app/resumo_estoque.html', contexto)


@login_required
def ordem_abate(request):
    # Obter a data selecionada ou usar a data de hoje
    if request.method == 'POST':
        data_selecionada_str = request.POST.get('data_selecionada')
        if data_selecionada_str:
            try:
                # Converter string para objeto date
                data_selecionada = date.fromisoformat(data_selecionada_str)
            except ValueError:
                # Se houver erro na conversão, usar a data de hoje
                data_selecionada = date.today()
        else:
            # Se não houver data selecionada, usar a data de hoje
            data_selecionada = date.today()
    else:
        # Por padrão, mostrar animais com data de hoje
        data_selecionada = date.today()
    
    # Filtrar animais pela data selecionada e ordenar por ordem de abate
    animais = Bovino.objects.filter(data_abate=data_selecionada).order_by('ordem_abate')
    
    # Se não houver ordem definida, definir uma ordem automática
    if animais and animais.first().ordem_abate is None:
        for i, animal in enumerate(animais):
            animal.ordem_abate = i + 1
            animal.save()
        animais = Bovino.objects.filter(data_abate=data_selecionada).order_by('ordem_abate')
    
    contexto = {
        'animais': animais,
        'data_selecionada': data_selecionada,
    }
    
    return render(request, 'frigorifico_app/ordem_abate.html', contexto)


@login_required
def atualizar_ordem_abate(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            # Obter dados do POST
            ordens = request.POST.get('ordens')
            data_abate_str = request.POST.get('data_abate')
            
            # Verificar se os dados estão presentes
            if not ordens or not data_abate_str:
                return JsonResponse({'status': 'error', 'message': 'Dados incompletos'})
            
            # Converter string JSON em lista
            ordens_lista = json.loads(ordens)
            
            # Converter string de data em objeto date
            try:
                data_abate = date.fromisoformat(data_abate_str)
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Formato de data inválido. Deve ser no formato YYYY-MM-DD.'})
            
            # Atualizar a ordem de abate de cada animal
            for i, animal_id in enumerate(ordens_lista):
                try:
                    animal = Bovino.objects.get(id=animal_id, data_abate=data_abate)
                    animal.ordem_abate = i + 1
                    animal.save()
                except Bovino.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': f'Animal com ID {animal_id} não encontrado para a data especificada.'})
            
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Erro ao decodificar os dados de ordem.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'})


@login_required
def relatorio_diario(request):
    # Obter a data selecionada ou usar a data de hoje
    if request.method == 'POST':
        data_selecionada_str = request.POST.get('data_selecionada')
        data_venda_str = request.POST.get('data_venda')
        
        # Filtros
        filtro_data_abate = None
        filtro_data_venda = None
        
        if data_selecionada_str:
            try:
                # Converter string para objeto date
                filtro_data_abate = date.fromisoformat(data_selecionada_str)
            except ValueError:
                # Se houver erro na conversão, usar a data de hoje
                filtro_data_abate = date.today()
        
        if data_venda_str:
            try:
                # Converter string para objeto date
                filtro_data_venda = date.fromisoformat(data_venda_str)
            except ValueError:
                pass
        
        # Definir qual data usar para exibição (padrão é hoje)
        data_exibicao = filtro_data_abate if filtro_data_abate else date.today()
    else:
        # Por padrão, mostrar animais com data de hoje
        filtro_data_abate = date.today()
        filtro_data_venda = None
        data_exibicao = date.today()
    
    # Filtrar animais
    animais = Bovino.objects.all().prefetch_related('meiacarcaça_set')
    
    # Aplicar filtro de data de abate se especificado
    if filtro_data_abate:
        animais = animais.filter(data_abate=filtro_data_abate)
    
    # Aplicar filtro de data de venda se especificado
    if filtro_data_venda:
        animais = animais.filter(meiacarcaça__data_venda__date=filtro_data_venda)
    
    # Remover duplicatas caso tenha filtrado por data de venda
    if filtro_data_venda:
        animais = animais.distinct()
    
    # Ordenar por ordem de abate
    animais = animais.order_by('ordem_abate')
    
    # Calcular totais
    total_animais = animais.count()
    
    contexto = {
        'animais': animais,
        'data_selecionada': data_exibicao,
        'filtro_data_venda': filtro_data_venda,
        'total_animais': total_animais,
    }
    
    return render(request, 'frigorifico_app/relatorio_diario.html', contexto)


@login_required
def detalhes_animal(request, id):
    animal = get_object_or_404(Bovino, id=id)
    
    contexto = {
        'animal': animal,
    }
    
    return render(request, 'frigorifico_app/detalhes_animal.html', contexto)


@login_required
def pesquisar_animais_venda(request):
    # Inicializar variáveis
    meias_carcaças = MeiaCarcaça.objects.none()
    pesquisa_realizada = False
    resultados_encontrados = False
    
    if request.method == 'POST':
        # Obter parâmetros de pesquisa
        tipo = request.POST.get('tipo')
        qualidade = request.POST.get('qualidade')
        peso_min = request.POST.get('peso_min')
        peso_max = request.POST.get('peso_max')
        
        # Construir consulta
        meias_carcaças = MeiaCarcaça.objects.select_related('bovino').filter(
            bovino__tipo_animal__isnull=False,
            bovino__qualidade__isnull=False,
            data_venda__isnull=True  # Apenas meias carcaças não vendidas
        )
        
        if tipo:
            meias_carcaças = meias_carcaças.filter(bovino__tipo_animal=tipo)
        
        if qualidade:
            meias_carcaças = meias_carcaças.filter(bovino__qualidade=qualidade)
        
        if peso_min:
            meias_carcaças = meias_carcaças.filter(peso__gte=peso_min)
        
        if peso_max:
            meias_carcaças = meias_carcaças.filter(peso__lte=peso_max)
        
        meias_carcaças = meias_carcaças.order_by('bovino__tipo_animal', 'bovino__qualidade', 'peso')
        pesquisa_realizada = True
        resultados_encontrados = meias_carcaças.exists()
    
    contexto = {
        'meias_carcaças': meias_carcaças,
        'tipos': Bovino.TIPO_ANIMAL_CHOICES,
        'qualidades': Bovino.QUALIDADE_CHOICES,
        'pesquisa_realizada': pesquisa_realizada,
        'resultados_encontrados': resultados_encontrados
    }
    
    return render(request, 'frigorifico_app/pesquisar_animais_venda.html', contexto)


@login_required
def registrar_venda(request, id):
    # Buscar a meia carcaça pelo ID e verificar se ainda não foi vendida
    try:
        meia_carcaça = MeiaCarcaça.objects.get(id=id, data_venda__isnull=True)
    except MeiaCarcaça.DoesNotExist:
        messages.error(request, 'Meia carcaça não encontrada ou já foi vendida.')
        return redirect('pesquisar_animais_venda')
    
    if request.method == 'POST':
        # Obter dados do formulário
        comprador = request.POST.get('comprador')
        preco_kg_str = request.POST.get('preco_kg')
        
        # Validar campos obrigatórios
        if not comprador or not preco_kg_str:
            messages.error(request, 'Todos os campos são obrigatórios.')
            contexto = {
                'meia_carcaça': meia_carcaça
            }
            return render(request, 'frigorifico_app/registrar_venda.html', contexto)
        
        try:
            preco_kg = float(preco_kg_str.replace(',', '.'))
            
            # Validar preço positivo
            if preco_kg <= 0:
                messages.error(request, 'O preço por kg deve ser um valor positivo.')
                contexto = {
                    'meia_carcaça': meia_carcaça
                }
                return render(request, 'frigorifico_app/registrar_venda.html', contexto)
            
            # Registrar a venda
            meia_carcaça.comprador = comprador
            meia_carcaça.preco_kg = preco_kg
            meia_carcaça.data_venda = timezone.now()
            meia_carcaça.save()
            
            valor_total = meia_carcaça.peso * Decimal(str(preco_kg))
            messages.success(request, f'Venda registrada com sucesso! Valor total: R$ {valor_total:.2f}')
            return redirect('pesquisar_animais_venda')
            
        except ValueError:
            messages.error(request, 'Valor inválido fornecido para o preço por kg.')
            contexto = {
                'meia_carcaça': meia_carcaça
            }
            return render(request, 'frigorifico_app/registrar_venda.html', contexto)
        except Exception as e:
            messages.error(request, f'Erro ao registrar a venda: {str(e)}')
            contexto = {
                'meia_carcaça': meia_carcaça
            }
            return render(request, 'frigorifico_app/registrar_venda.html', contexto)
    
    contexto = {
        'meia_carcaça': meia_carcaça
    }
    
    return render(request, 'frigorifico_app/registrar_venda.html', contexto)

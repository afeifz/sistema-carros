import requests
import pandas as pd
def forca_opcao(msg,conjunto_opcoes,msg_erro = 'Inválido'):
    opcoes = '\n'.join(conjunto_opcoes)
    opcao = input(f"{msg}\n{opcoes}\n->")
    while not opcao in conjunto_opcoes:
        print(msg_erro)
        opcao = input(f"{msg}\n{opcoes}\n->")
    return opcao

def checa_numero(msg,msg_erro = 'Inválido'):
    num = input(msg)
    while not num.isnumeric():
        print(msg_erro)
        num = input(msg)
    return int(num)

def comprar():
    while True:
        escolha = forca_opcao("Qual carro tu quer?",carros['modelo'])
        indice_escolha = indices[escolha]
        for key in carros.keys():
            print(f'{key} : {carros[key][indice_escolha]} ')

        comprar = forca_opcao(f'Vai comprar o {escolha}?',sim_ou_nao)
        if comprar == sim_ou_nao[0]:
            qtd = checa_numero(f'Quantas unidades de {escolha} vc vai levar? \n ->')
            if qtd > carros['estoque'][indice_escolha]:
                print(f'Não há {qtd} no nosso estoque. Voltando ao início')
                continue
            else:
                carros['estoque'][indice_escolha] -= qtd
                if escolha not in carrinho['Carros'].keys():
                    carrinho['Carros'][escolha] = qtd
                else:
                    carrinho['Carros'][escolha] += qtd
                carrinho['Valor Total'] += qtd*carros['preco'][indice_escolha]
        encerrar = forca_opcao("Você deseja encerrar a compra?",sim_ou_nao)
        if encerrar == sim_ou_nao[0]:
            if carrinho['Valor Total'] != 0:
                carrinho['endereco'] = endereco()
                return
            print('cuzao')


def endereco():
    while True:
        cep = input('diga seu cep')
        url = f'https://viacep.com.br/ws/{cep}/json/'
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            infos = ''
            for key in response.keys():
                infos += f'\n {key} : {response[key]}'
            validar_endereco = forca_opcao("As informações estão corretas?",sim_ou_nao)
            if validar_endereco == sim_ou_nao[0]:
                response['unidade'] = input("Diga o número: ")
                response['complemento'] = input("Diga o complemento")
                return response


def printa_dic(dic,level = 0):
    for key in dic.keys():
        if type(dic[key]) is not dict:
            print(f'{level*" "}{key} : {dic[key]}')
        else:
            level += 2
            print(f'{key}')
            printa_dic(dic[key],level)
            level -= 2
def remover():
    escolha = forca_opcao(f'Qual dos carros deseja remover?', carros['modelo'])
    indice_remover = indices[escolha]
    for key in carros.keys():
        carros[key].pop(indice_remover)

def cadastrar():
    for key in carros.keys():
        info = input(f'Diga o novo/a {key}')
        carros[key].append(info)

def atualizar():
    opcoes_atualizacao = list(carros.keys())
    opcoes_atualizacao.append("Total")
    escolha = forca_opcao(f'Qual dos carros deseja atualizar?', carros['modelo'])
    indice_escolha = indices[escolha]
    tipo_atualizacao = forca_opcao(f"Qual tipo de atualização?", opcoes_atualizacao)
    if tipo_atualizacao == opcoes_atualizacao[len(opcoes_atualizacao) - 1]:
        for key in carros.keys():
            carros[key][indice_escolha] = input(f'Diga o novo {key} do carro {escolha}')
    else:
        carros[tipo_atualizacao][indice_escolha] = input(f'Diga o novo {tipo_atualizacao} do carro {escolha}')



carros = {
    'modelo': ['opala', 'marea', 'kombi', 'celtinha brabio', 'uno', 'monza', 'corcel'],
    'potencia(cv)': [172, 130, 250, 140, 100, 120, 150],
    'consumo (km/l)': [1, 3, 8, 7, 15, 2, 1.6],
    'cor': ['laranja', 'verde', 'branca', 'preto', 'prata', 'preto', 'azul'],
    'ano': ['1972', '2004', '1985', '2014', '2001', '1980', '1975'],
    'estoque': [5, 6, 7, 8, 9, 10, 11],
    'preco': [50, 10, 2, 0, 100000, 100, 200]
    }
carrinho = {
    'Carros' : {},
    'Valor Total': 0,
    'endereco': {

        }
    }

# Método diferentes de operar os indíces(deixar comentado)
'''indices = {}
    for i in range(len(carros['modelo'])):
        if carros['modelo'][i] == escolha:
            indice_escolha = i
            break'''

operacoes = ['remover','cadastrar','atualizar']
indices = {carros['modelo'][i] : i for i in range(len(carros['modelo']))}
sim_ou_nao = ['sim','nao']
funcao = ['cliente','funcionario']
cliente_ou_funcionario = forca_opcao('Qual dos dois vc se encaixa?',funcao)
if cliente_ou_funcionario == funcao[0]:
    comprar()
    printa_dic(carrinho)
else:
    operacao = forca_opcao(f'Qual operação você realizará?',operacoes)
    if operacao == operacoes[0]:
        remover()
    elif operacao == operacoes[1]:
        cadastrar()
    else:
        atualizar()
    print(pd.DataFrame(carros))


# Método para puxar a api pra validar o cep(deixar comentado)
'''cep = input('diga seu cep')
url = f'https://viacep.com.br/ws/{cep}/json/'
response = requests.get(url)
print(response.json())'''



import os
from sys import platform
from random import randint

def sortearNumero(minimo, maximo):
    return randint(minimo, maximo)

# função responsável por identificar o sistema e com isso, utilizar o comando para limpar a tela do terminal
def limparTela(esperar=True):
    comando = "cls" if "win" in platform else "clear"
    if esperar:
        input("pressione enter para continuar: ")
    os.system(comando) 

def exibirLinha():
    print("-" * 45)

def exibirTitulo(titulo):
    posicao_inicial = int(45/2 - len(titulo) / 2) - 1
    exibirLinha()
    print(" " * posicao_inicial, titulo)
    exibirLinha()

def selecioneOpcao(lista_original, mensagem="selecione uma das opções:", escolha_obrigatoria=True):
    while True:
        for indice, opcao in enumerate(lista_original):
            print(f"{indice}){opcao}")
        
        try:
            escolha = int(input(mensagem))
            if escolha >= 0 and escolha < len(lista_original):
                return escolha
            else:
                print("Erro: Selecione uma opção válida!")

        except ValueError:
            print("Erro: Selecione uma opção válida!")
        
        if not(escolha_obrigatoria):
            return None
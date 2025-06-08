import os
from sys import platform
from random import randint
from classes import Personagem, Feitico, Movimento, Expansao 
from batalha import Batalha

def limparTela():
    comando = "cls" if "win" in platform else "clear"
    input("pressione enter para continuar: ")
    os.system(comando) 

class Main:
    def __init__(self):
        while True:
            print("bem vindo!")
            print("modos de jogo: ")
            print("a)jogador vs jogador     b)jogador vs computador")
            modo = input("selecione o modo de jogo: ")

            limparTela()
            if "a" in modo:
                self.jogadorVsJogador()
            elif "b" in modo:
                self.jogadorVsComputador()
    
    def escolhaPersonagem(self, modo="automatico"):
        # feiticos
        # gojo
        azul = Feitico("azul", 15, 100, 15, 100, "imobilizado", [1, 3])
        vermelho = Feitico("vermelho", 25, 100, 35, 0)
        vazio_roxo = Feitico("vazio roxo", 70, 100, 60, 0)
        # sukuna
        clivar = Feitico("clivar", 20, 100, 25, 50, "sangrando", [1, 3])
        desmantelar = Feitico("desmantelar", 75, 100, 80, 0)
        flecha_fogo = Feitico("flecha de fogo", 50, 100, 65, 60, "queimando", [2, 4])

        # golpes
        soco = Movimento("soco simples", 6, 100, 25, 100, "atordoado", [2, 4])
        chute = Movimento("Chute tranversal", 8, 100, 15, 0)

        # expansão
        muriokusho = Expansao("muriokusho", 35)
        santuario = Expansao("santuario", 40)

        # personagens disponíveis
        personagens = []
        # satoru Gojo
        personagens.append(Personagem("Satoru Gojo", 100, 10, 10, 100, [soco, chute], [azul, vermelho, vazio_roxo], muriokusho, True))
        # Ryomen Sukuna
        personagens.append(Personagem("Ryomen Sukuna", 100, 10, 10, 100, [soco, chute], [clivar, desmantelar, flecha_fogo], santuario, True))
        
        if modo == "automatico":
            ...
        else:
            while True:
                for n, personagem in enumerate(personagens):
                    print(f"{n}){personagem.nome}")

                escolha = input("escolha um dos personagens: ")
                

                if escolha.isnumeric(): 
                    if int(escolha) < len(personagens):
                        limparTela()
                        personagem = personagens[int(escolha)]
                        personagem.definirModo("manual")
                        return personagem
                    else:
                        print("Erro: opção inválida!")
                else:
                    print("Erro: por favor, insira um valor númerico válido!")
                limparTela()
            
    def jogadorVsJogador(self):
        jogador1 = self.escolhaPersonagem("manual")
        jogador2 = self.escolhaPersonagem("manual")

        batalha = Batalha([jogador1, jogador2])
        batalha.cicloBatalha()

    def jogadorVsComputador(self):
        ...

Main()

        

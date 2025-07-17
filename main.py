from utils import limparTela, selecioneOpcao, sortearNumero
from character import Personagens
from actions import ConjuntoAcoes
from battle import Batalha

# classe principal onde o jogo se passa.
class Main:
    def __init__(self):
        # looping principal, menu inicial.
        print("bem vindo!")
        print("modos de jogo: ")
        lista_modos_jogo = ["jogador vs jogador", "jogador vs computador", "sair"]

        modo_jogo =  selecioneOpcao(lista_exibicao=lista_modos_jogo, lista_original=["a", "B", "c"], mensagem="selecione o modo de jogo: ")

        if "a" in modo_jogo:
            self.jogadorVsJogador() # redireciona o jogador para o modo_jogo jogador VS jogador
        elif "b" in modo_jogo:
            self.jogadorVsComputador() # redireciona o jogador para o modo_jogo jogador VS computador
        else:
            exit() # fecha o programa

    def escolherPersonagem(self, modo="automatico"):
        """É responsável por permitir que o usuário escolha os movimentos e feitiços"""

        # personagens disponíveis
        personagens = Personagens().adicionarPersonagens()

        for personagem in personagens:
            ConjuntoAcoes().adicionarAcoesPersonagem(personagem)
    
        limparTela()
        if modo == "automatico":
            # sorteando um número aleatório para escolher o indíce da lista personagens. 
            indice_sorteado = sortearNumero(0, len(personagens) - 1)
            # escolhe o personagem no indice da lista personagens e armazena na variavel personagem 
            personagem = personagens[indice_sorteado]
            return personagem 
        else:
            lista_personagens = []
            # looping responsável por exibir todos os personagens
            for n, personagem in enumerate(personagens):
                lista_personagens.append(personagem.nome)

            personagem = selecioneOpcao(lista_exibicao=lista_personagens, lista_original=personagens, mensagem="selecione um personagem: ")
            personagem.definirModo("manual")
            return personagem
            
    def jogadorVsJogador(self):
        jogador1 = self.escolherPersonagem("manual")
        jogador2 = self.escolherPersonagem("manual")

        batalha = Batalha([jogador1, jogador2])
        batalha.looping()

    def jogadorVsComputador(self):
        ...

Main()
from utilidades import limparTela, selecioneOpcao, sortearNumero
from personagem import Personagens
from batalha import Batalha


# classe principal onde o jogo se passa.
class Main:
    def __init__(self):
        self.numero_jogadores = 2
        self.jogadores = []
        # looping principal, menu inicial.
        print("bem vindo!")
        modo_jogo =  selecioneOpcao(lista_original=["jogador vs jogador", "sair"], mensagem="selecione o modo de jogo: ")

        if modo_jogo == 0:
            self.jogadorVsJogador() # redireciona o jogador para o modo_jogo jogador VS jogador
        else:
            exit() # fecha o programa

    def escolherPersonagem(self, modo):
        """É responsável por permitir que o usuário escolha os movimentos e feitiços"""
        # personagens disponíveis
        personagens = Personagens().carregarPersonagens()

        limparTela()
        match modo:
            case "aleatoria":
                # sorteando um número aleatório para escolher o indíce da lista personagens. 
                indice_escolhido = sortearNumero(0, len(personagens) - 1)
            case "manual":
                # looping responsável por exibir todos os personagens
                lista_personagens = [personagem.nome for personagem in personagens]
                indice_escolhido = selecioneOpcao(lista_original=lista_personagens, mensagem="selecione um personagem: ") 

        return personagens[indice_escolhido]
                  
    def jogadorVsJogador(self):
        for n in range(1, self.numero_jogadores + 1):
            print(f"player {n} vai escolher o personagem: ")
            opcoes = ["manual", "aleatoria"]
            indice_escolhido = selecioneOpcao(lista_original=opcoes, mensagem="selecione o modo de escolha: ", escolha_obrigatoria=True)
            opcao = opcoes[indice_escolhido]

            self.jogadores.append(self.escolherPersonagem(opcao))

        batalha = Batalha(self.jogadores)
        batalha.looping()
        
Main()
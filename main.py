from utilidades import limparTela, selecioneOpcao, sortearNumero
from personagem import Personagens
from acoes import ConjuntoAcoes
from batalha import Batalha

# classe principal onde o jogo se passa.
class Main:
    def __init__(self):
        self.numero_jogadores = 2
        self.jogadores = []
        # looping principal, menu inicial.
        print("bem vindo!")
        
        lista_modos_jogo = ["jogador vs jogador", "sair"]
        modo_jogo =  selecioneOpcao(lista_exibicao=lista_modos_jogo, lista_original=["a", "b"], mensagem="selecione o modo de jogo: ")

        if "a" in modo_jogo:
            self.jogadorVsJogador() # redireciona o jogador para o modo_jogo jogador VS jogador
        else:
            exit() # fecha o programa

    def escolherPersonagem(self, modo):
        """É responsável por permitir que o usuário escolha os movimentos e feitiços"""
        # personagens disponíveis
        personagens = Personagens().adicionarPersonagens()
        for personagem in personagens:
            ConjuntoAcoes().adicionarAcoesPersonagem(personagem)
    
        limparTela()
        if modo == "aleatoria":
            # sorteando um número aleatório para escolher o indíce da lista personagens. 
            indice_sorteado = sortearNumero(0, len(personagens) - 1)
            # escolhe o personagem no indice da lista personagens e armazena na variavel personagem 
            personagem = personagens[indice_sorteado]

        elif modo == "manual":
            lista_personagens = []
            # looping responsável por exibir todos os personagens
            for personagem in personagens:
                lista_personagens.append(personagem.nome)
            personagem = selecioneOpcao(lista_exibicao=lista_personagens, lista_original=personagens, mensagem="selecione um personagem: ")
            
        return personagem
                  
    def jogadorVsJogador(self):
        for n in range(1, self.numero_jogadores + 1):
            print(f"player {n} vai escolher o personagem: ")
            opcoes = ["manual", "aleatoria"]
            modo = selecioneOpcao(lista_exibicao=opcoes, lista_original=opcoes, mensagem="selecione o modo de escolha: ", escolha_obrigatoria=True)
            self.jogadores.append(self.escolherPersonagem(modo))

        batalha = Batalha(self.jogadores)
        batalha.looping()
        
Main()
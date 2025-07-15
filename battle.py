from utils import limparTela, exibirLinha, exibirTitulo

# responsável por batalhas e funções relacionadas.
class Batalha:
    def __init__(self, personagens):
        self.personagens = personagens
        self.acoes = []
        self.efeitos = []
        self.expansoes = []

        for personagem in self.personagens:
            if personagem.expansao != None:
                self.expansoes.append(personagem.expansao)

    def looping(self):
        while True:
            self.escolherAcoes()
            self.executarAcoes()
            self.aplicarEfeitoExpansoes()
            self.exibirInformacoes()

            vencedor = self.verificarVencedor()
            if vencedor != None:
                print(f"{vencedor.nome} venceu!")
                break
            else:
                for personagem in self.personagens:
                    personagem.energia += 40
                    print(f"{personagem.nome} recuperou {40} de energia!")
        limparTela()

    def escolherAcoes(self):
        # organizando os personagens por velocidade, aqueles mais rapidos escolhem primeiro sua ação e as executam primeiro.
        self.personagens.sort(key=lambda p: p.agilidade, reverse=True)
        for personagem in self.personagens:
            self.acoes.append(personagem.escolherAcao(alvos=self.personagens))

    def executarAcoes(self):
        limparTela()
        exibirTitulo("executando ações")
        for acao in self.acoes:    
            acao.utilizar()
            exibirLinha()

        self.acoes.clear()

    def analisarStatus(self):
        limparTela()
        exibirTitulo("Aplicação de efeitos de status")
        for personagem in self.personagens:
            personagem.analisarStatus()
        exibirLinha()

    def exibirInformacoes(self):
        limparTela()
        exibirTitulo("fim de turno")
        for personagem in self.personagens:
            print(f"nome: {personagem.nome}    vida:  {personagem.vida}")
        exibirLinha()

    def aplicarEfeitoExpansoes(self):
        for expansao in self.expansoes:
            try:
                expansao.definirAlvos(self.personagens)
                expansao.podeConsumir()
                if expansao.ativa:
                    expansao.executar()
            except AttributeError: 
                pass

    def verificarVencedor(self):
        for personagem in self.personagens:
            if personagem.vida <= 0:
                self.personagens.remove(personagem)

        if len(self.personagens) == 1:
            return self.personagens[0]
        else:
            return None
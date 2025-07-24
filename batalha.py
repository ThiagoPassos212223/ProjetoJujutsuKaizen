from utilidades import limparTela, exibirLinha, exibirTitulo

# responsável por batalhas e funções relacionadas.
class Batalha:
    def __init__(self, personagens):
        self.personagens = personagens
        self.efeitos = []
        self.expansoes = []

    def looping(self):
        while True:
            self.escolherAcoes()
            self.executarAcoes()
            self.aplicarEfeitoExpansoes()
            self.exibirInformacoes()

            vencedor = self.verificarVencedor()
            if vencedor:
                print(f"{vencedor.nome} venceu!")
                break
        limparTela()

    def escolherAcoes(self):
        # organizando os personagens por velocidade, aqueles mais rapidos escolhem primeiro sua ação e as executam primeiro.
        self.personagens.sort(key=lambda p: p.agilidade, reverse=True)

        for personagem in self.personagens:
            personagem.escolherAcao(alvos=self.personagens)
    
    def fornecerEnergia(self):
        for personagem in self.personagens:
            personagem.energia += 40
            print(f"{personagem.nome} recuperou {40} de energia!")

    def executarAcoes(self):
        limparTela()
        exibirTitulo("executando ações")
        for personagem in self.personagens:
            personagem.executarAcao()

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
        for personagem in self.personagens:
            personagem.aplicarEfeitosExpansao(alvos_potencial=self.personagens)
                                        
    def verificarVencedor(self):
        for personagem in self.personagens:
            if personagem.vida <= 0:
                self.personagens.remove(personagem)

        if len(self.personagens) == 1:
            return self.personagens[0]
        else:
            return None
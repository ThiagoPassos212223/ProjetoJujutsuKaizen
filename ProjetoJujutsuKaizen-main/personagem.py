from utilidades import limparTela, exibirLinha, selecioneOpcao
from acoes import ConjuntoAcoes

class Personagem:
    def __init__(self, nome, vida, agilidade, energia):
        # atributos básicos
        self.nome = nome
        self.vida = vida
        self.agilidade = agilidade
        self.energia = energia

        self.precisao = 100
        self.status = []
        self.acao = None
    
    def adicionarMovimentos(self, feiticos, golpes, expansao=None, energia_reversa=False):
        self.feiticos = feiticos
        self.golpes = golpes
        self.expansao = expansao
        self.regeneracao = energia_reversa

    def analisarStatus(self):
        self.joga = True
        print(f"status: ({self.nome})")
        for status in self.status:
            efeito_status, duracao = status[0], status[1]
            match efeito_status:
                case "queimando":
                    print(f"{self.nome} está queimando! recebeu {5} de dano.")
                    self.vida -= 5
                case "sangrando":
                    print(f"{self.nome} está sangrando! recebeu {self.vida * 0.1} de dano.")
                    self.vida -= self.vida * 0.1
                case "imobilizado":
                    print(f"{self.nome} está imobilizado! Não é possível realizar sua ação.") 
                    self.joga = False
                case "atordoado":
                    print(f"{self.nome} está atordoado! Não poderá realizar sua ação.")
                    self.joga = False
                case "mugen ativado":
                    print(f"{self.nome} está com mugen ativado!")
                case "regeneração":
                    self.vida += 40
                    print(f"{self.nome} está se regenerando utilizando energia reversa! Recuperou 40 de vida")
                case "rika_manifestada":
                    self.energia += 50
                    print("rika está manifestada! Recebeu 50 de energia amaldiçoada")
                case _:
                    print(f"ERRO! Um status não cadastrado foi detectado! {efeito_status}")
            status[1] -= 1
            if duracao == 0:
                self.status.remove(status)
            
        exibirLinha()
        return self.joga
    
    def escolherAcao(self, alvos):
        while True:
            limparTela()
            print(f"seleção de movimentos: ({self.nome})")
            print(f"vida: {self.vida}   energia: {self.energia}")

            lista_opcoes = ["golpes", "feitiços"]

            if self.expansao:
                lista_opcoes.append("expansao")

            indice_escolhido = selecioneOpcao(lista_original=lista_opcoes, mensagem="selecione sua ação: ")
            acao = lista_opcoes[indice_escolhido]
            
            match acao:
                case "golpes":
                    acao = self.golpes
                case "feitiços":
                    acao = self.feiticos
                case "expansao":
                    acao = self.expansao
                case _:
                    acao = None

            if type(acao) == list:
                if len(acao) > 1:
                    lista_amostra = [acao.nome for acao in acao] 
                    indice_escolhido = selecioneOpcao(lista_original=lista_amostra, mensagem="selecione um movimento: ", escolha_obrigatoria=False)  
                else:
                    indice_escolhido = 0
                acao_escolhida = acao[indice_escolhido]

            else:
                acao_escolhida = acao

            if acao_escolhida:
                exibirLinha()
                print("informações adicionais")
                acao_escolhida.exibirInformacoes()
                indice_escolhido = selecioneOpcao(lista_original=["confirmar escolha", "cancelar"], mensagem="selecione uma das opções: ", escolha_obrigatoria=True)
                match indice_escolhido:
                    case 0:
                        acao_escolhida.definirUsuario(self)
                        if acao_escolhida.tipo == "acao":
                            acao_escolhida.definirAlvo(alvos) 
                    case _:
                        acao_escolhida = None 
                
                if acao_escolhida:
                    pode_utilizar = acao_escolhida.podeSerUtilizado()
                    if pode_utilizar:
                        self.acao = acao_escolhida
                        return None
            else:
                print("nenhuma opção foi selecionada!")
        
    def executarAcao(self):
        print(f"{self.nome} (Ação)")
        if self.acao:
            if self.analisarStatus() and self.vida > 0:
                if self.acao.tipo == "acao":
                    self.acao.utilizar()
                else:
                    self.acao.executar()
        else:
            print("nenhuma ação foi selecionada!")
        
    def aplicarEfeitosExpansao(self, alvos_potencial):
        if self.expansao and self.expansao.ativada:
            if self.vida > 20:
                self.expansao.definirAlvos(alvos_potencial)
                if self.expansao.podeSerUtilizado():
                    self.expansao.aplicarEfeitos()
                else:
                    self.expansao.ativada = False
                    print(f"{self.expansao.nome} está desativada! Energia insuficiente!")
            else:
                self.expansao.ativada = False
                print("expansão foi desativada! O usuário está gravemente ferido. Incapaz de manter sua expansão")

class Personagens:
    def __init__(self):
        self.personagens = [
            Personagem(nome="Satoru Gojo", vida=100, agilidade=100, energia=100),
            Personagem(nome="Ryomen Sukuna", vida=100, agilidade=90, energia=400),
            Personagem(nome="Yuta Okkotsu", vida=100, agilidade=50, energia=200)
        ]

        for personagem in self.personagens:
            ConjuntoAcoes().adicionarAcoesPersonagem(personagem)

    def carregarPersonagens(self):
        return self.personagens.copy()
    
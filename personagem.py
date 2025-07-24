from utilidades import limparTela, exibirLinha, selecioneOpcao

# classe responsável por modelar os feiticeiros e maldições
class Personagem:
    """classe responsável por modelar os personagens, definindo seus atributos e comportamentos como analisarStatus, escolherAcao. """
    def __init__(self, nome, vida, agilidade, energia):
        # atributos básicos
        self.nome = nome
        self.vida = vida
        self.agilidade = agilidade
        self.energia = energia
        # atributos padrão (todos os personagens possuem o mesmo valor)
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
        # self.status é uma lista que possuí todos os status que o jogador possuí, os status são analisados nesse looping 
        for status in self.status:
            # efeito_status: recebe um string contendo o efeito de status
            # duração: recebe um valor inteiro contendo a duração em turnos do efeito
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
            # verifica se a duração do efeito de status acabou, caso tenha, remove da lista de efeito de status
            status[1] -= 1
            if duracao == 0:
                self.status.remove(status)
            
        exibirLinha()
        return self.joga
    
    def escolherAcao(self, alvos):
        """responsável por permitir a escolha das ações do personagem"""
        while True:
            limparTela()
            print(f"seleção de movimentos: ({self.nome})")
            print(f"vida: {self.vida}   energia: {self.energia}")

            lista_opcoes = ["golpes", "feitiços"]
            # caso o personagem possua expansão, ela será exibida, caso contrário, não
            if self.expansao:
                lista_opcoes.append("expansao")

            # verifica a seleção do usuário e com isso, carrega a lista de opções correta. 
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
                # exibe informações sobre o movimento, feitiço ou expansão escolhida
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
    def adicionarPersonagens():
        personagens = []
        personagens.append(Personagem(nome="Satoru Gojo", vida=100, agilidade=100, energia=100))
        personagens.append(Personagem(nome="Ryomen Sukuna", vida=100, agilidade=90, energia=400))
        personagens.append(Personagem(nome="Yuta Okkotsu", vida=100, agilidade=50, energia=200))
        return personagens
    
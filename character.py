from utils import limparTela, exibirLinha, selecioneOpcao

# classe responsável por modelar os feiticeiros e maldições
class Personagem:
    """classe responsável por modelar os personagens, definindo seus atributos e comportamentos como analisarStatus, escolherAcao. """
    def __init__(self, nome, vida, agilidade, energia, energia_reversa=False):
        # atributos básicos
        self.nome = nome
        self.vida = vida
        self.agilidade = agilidade
        self.evasao = 10
        self.energia = energia
        self.energia_reversa = energia_reversa
        # atributos padrão (todos os personagens possuem o mesmo valor)
        self.precisao = 100
        self.status = []

        self.expansao_ativada = False
    
    def adicionarAcoes(self, feiticos, movimentos, expansao):
        self.feiticos = feiticos
        self.movimentos = movimentos
        self.expansao = expansao

    def analisarStatus(self):
        joga = True
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
                    joga = False
                case "atordoado":
                    print(f"{self.nome} está atordoado! Não poderá realizar sua ação.")
                    joga = False
                case "mugen ativado":
                    print(f"{self.nome} está com mugen ativado!")
                case "regeneração":
                    self.vida += 40
                    print(f"{self.nome} está se regenerando utilizando energia reversa! Recuperou 40 de vida")
                case _:
                    print(f"ERRO! Um status não cadastrado foi detectado! {efeito_status}")
            # verifica se a duração do efeito de status acabou, caso tenha, remove da lista de efeito de status
            if duracao - 1 == 0:
                self.status.remove(status)
            else: 
                status[1] -= 1
        exibirLinha()
        return joga

    def definirModo(self, modo="ia"):
        """define se o personagem sera controlado por uma IA ou um jogador"""
        self.modo = "ia" if modo == "ia" else "jogador"

    def escolherAcao(self, alvos):
        """responsável por permitir a escolha das ações do personagem"""
        limparTela()
        if self.modo == "ia":
            ...
        else:
            while True:
                print(f"seleção de movimentos: ({self.nome})")
                print(f"vida: {self.vida}   energia: {self.energia}")

                dicionario_opcoes = [self.movimentos, self.feiticos]            
                # caso o personagem possua expansão, ela será exibida, caso contrário, não
                if self.expansao != None:
                    dicionario_opcoes.append(self.expansao)

                # verifica a seleção do usuário e com isso, carrega a lista de opções correta. 
                acoes = selecioneOpcao(lista_exibicao=["movimentos", "feitiços", "expansao"], lista_original=dicionario_opcoes, mensagem="selecione sua ação: ")

                if type(acoes) == list:
                    if len(acoes) > 1:
                        lista_amostra = []
                        for acao in acoes:
                            lista_amostra.append(acao.nome) 
                        acao_escolhida = selecioneOpcao(lista_exibicao=lista_amostra, lista_original=acoes, mensagem="selecione um movimento: ", escolha_obrigatoria=False) 
                        if acao_escolhida == None:
                            return self.escolherAcao(alvos)
                    else:
                        acao_escolhida = acoes[0]

                else:
                    acao_escolhida = acoes

                # exibe informações sobre o movimento, feitiço ou expansão escolhida
                exibirLinha()
                print("informações adicionais")
                acao_escolhida.exibirInformacoes()

                escolha = selecioneOpcao(lista_exibicao=["confirmar escolha", "cancelar"], lista_original=[True, False], mensagem="selecione uma das opções: ", escolha_obrigatoria=True)
                if escolha:
                    if acao_escolhida.tipo == "acao":
                        if not(acao_escolhida.alvo_usuario):
                            acao_escolhida.definirUsuario(self)
                            acao_escolhida.definirAlvo(alvos)
                        else:
                            acao_escolhida.definirUsuario(self)
                            acao_escolhida.definirAlvo(alvos)
                    else:
                        acao_escolhida.definirUsuario(self)

                    pode_utilizar = acao_escolhida.podeSerUtilizado()

                    if pode_utilizar:
                        return acao_escolhida
                    else:
                        return self.escolherAcao(alvos)
                else:
                    return self.escolherAcao(alvos)

class Personagens:
    def __init__(self):
        ...
        
    def adicionarPersonagens(self):
        personagens = []
        personagens.append(Personagem(nome="Satoru Gojo", vida=100, agilidade=100, energia=100, energia_reversa=True))
        personagens.append(Personagem(nome="Ryomen Sukuna", vida=100, agilidade=90, energia=100, energia_reversa=True))

        return personagens
    
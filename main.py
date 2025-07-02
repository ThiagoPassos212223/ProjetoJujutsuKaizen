import os # responsável por interagir com o sistema
from sys import platform, exit # responsável por identificar o OS e fechar o programa quando necessário.
from random import randint # responsável por gerar números pseudoaleatórios

# função responsável por identificar o sistema e com isso, utilizar o comando para limpar a tela do terminal
def limparTela(esperar=True):
    comando = "cls" if "win" in platform else "clear"
    if esperar:
        input("pressione enter para continuar: ")
    os.system(comando) 

def exibirLinha():
    print("-" * 45)

def exibirTitulo(titulo):
    posicao_inicial = int(45/2)
    posicao_inicial = posicao_inicial - int(len(titulo) / 2)
    exibirLinha()
    print(" " * int(posicao_inicial - 1), titulo)
    exibirLinha()

def selecioneOpcao(lista_exibicao, lista_original, mensagem="selecione uma das opções:", escolha_obrigatoria=True):
    for indice, opcao in enumerate(lista_exibicao):
        print(f"{indice}){opcao}")    
    try:
        escolha = int(input(mensagem))
        return lista_original[escolha]
    except ValueError:
        print("Erro: o tipo esperado é um valor númerico inteiro positivo!")
    except IndexError:
        print("Erro: opção inválida, selecione uma das opções disponíveis!")

    if escolha_obrigatoria:
        return selecioneOpcao(lista_exibicao, lista_original, mensagem)    
    else:
        return None

# classe responsável por modelar os feiticeiros e maldições
class Personagem:
    """classe responsável por modelar os personagens, definindo seus atributos e comportamentos como analisarStatus, escolherAcao. """
    def __init__(self, nome, vida, defesa, ataque, agilidade, energia, movimentos, feiticos, expansao=None, energia_reversa=False):
        # atributos básicos
        self.nome = nome
        self.vida = vida
        self.defesa = defesa
        self.ataque = ataque
        self.agilidade = agilidade
        self.evasao = 10
        self.energia = energia
        self.feiticos = feiticos
        self.movimentos = movimentos
        self.expansao = expansao
        self.energia_reversa = energia_reversa
        self.regeneracao = Regeneracao("regeneração", "energia", 30, self)

        # atributos padrão (todos os personagens possuem o mesmo valor)
        self.precisao = 100
        self.status = []
        
    def analisarStatus(self):
        """aplica efeitos de status e define se o usuário pode realizar sua ação ou tem algum efeito de status que o impeça"""
        # verifica se a regeneração está ativada
        if self.regeneracao.ativa:
            # recupera a vida do usuário, caso ele tenha energia para fazer isso, caso não, desativa a regeneração
            self.regeneracao.executar()

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
                case _:
                    print(f"ERRO! Um status não cadastrado foi detectado! {efeito_status}")
            
            # verifica se a duração do efeito de status acabou, caso tenha, remove da lista de efeito de status
            if duracao - 1 == 0:
                self.status.remove(status)
            # reduz a duração do efeito de status
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
            print("oi")    
        else:
            while True:
                print(f"seleção de movimentos: ({self.nome})")
                print(f"vida: {self.vida}   energia: {self.energia}")

                dicionario_opcoes = [self.movimentos, self.feiticos]            
                # caso o personagem possua expansão, ela será exibida, caso contrário, não
                if self.expansao != None:
                    dicionario_opcoes.append(self.expansao)
                # caso o personagem possua regeneração, a escolha é exibida, caso contrário, não
                if self.energia_reversa:
                    dicionario_opcoes.append(self.regeneracao)

                # verifica a seleção do usuário e com isso, carrega a lista de opções correta. 
                acoes = selecioneOpcao(lista_exibicao=["movimentos", "feitiços", "expansao", "regeneração"], lista_original=dicionario_opcoes, mensagem="selecione sua ação: ")

                if type(acoes) == list:
                    if len(acoes) > 1:
                        lista_amostra = []
                        for indice, acao in enumerate(acoes):
                            lista_amostra.append(acao.nome) 

                        acao_escolhida = selecioneOpcao(lista_exibicao=lista_amostra, lista_original=acoes, mensagem="selecione um movimento: ", escolha_obrigatoria=False) 
                        if acao_escolhida == None:
                            return self.escolherAcao(alvos)
                    else:
                        acao_escolhida = acoes[0]

                elif type(acoes) == Regeneracao or type(acoes) == Expansao:
                    acao_escolhida = acoes

                # exibe informações sobre o movimento, feitiço ou expansão escolhida
                exibirLinha()
                print("informações adicionais")
                acao_escolhida.exibirInformacoes()

                escolha = selecioneOpcao(lista_exibicao=["confirmar escolha", "cancelar"], lista_original=[True, False], mensagem="selecione uma das opções: ", escolha_obrigatoria=True)

                if escolha:
                    if type(acao_escolhida) == Movimento:
                        acao_escolhida.definirUsuario(self)
                        acao_escolhida.definirAlvo(alvos)
                    else:
                        acao_escolhida.definirUsuario(self)

                    pode_utilizar = acao_escolhida.podeConsumir()

                    if pode_utilizar:
                        return acao_escolhida
                    else:
                        return self.escolherAcao(alvos)

                else:
                    return self.escolherAcao(alvos)

class Efeito:
    def __init__(self, nome, duracao, alvo):
        self.nome = nome
        self.duracao = duracao
        self.alvo = alvo

# Molda outras classes, facilitando a utilização de funções em comum. 
class Acao:
    def __init__(self, nome, fonte, consumo, alvo_usuario=False):
        self.nome = nome
        self.fonte = fonte
        self.consumo = consumo
        self.alvo_usuario = alvo_usuario
    
    def definirUsuario(self, usuario):
        self.usuario = usuario

    def definirAlvo(self, lista_alvos):
        # limpando a tela
        limparTela(esperar=False)
        
        alvos = lista_alvos.copy()
        # remove o usuário da lista de alvos possíveis
        if self.alvo_usuario:
            self.alvo = self.usuario
            return None
        else:
            alvos.remove(self.usuario)
            if len(alvos) == 1:
                self.alvo = alvos[0]
                return None
            else:
                for indice, alvo in enumerate(alvos):
                    print(f"{indice}){alvo.nome}")
                try:
                    indice_alvo = int(input("selecione o alvo da sua ação: "))
                    self.alvo = alvos[indice_alvo]
                    return None     
                except ValueError:
                    print(f"ERRO: o tipo esperado é um valor númerico inteiro positivo! Tente novamente!")
                except IndexError:
                    print("ERRO: opção inválida! Selecione uma das opções disponíveis!")

        # repete a função caso ocorra algum erro. A função só encerra o looping caso o usuário tenha selecionado um alvo válido.
        return self.definirAlvo(lista_alvos)

    def podeConsumir(self):
        if self.fonte == "energia":
            # reduz a energia do usuário do feitiço
            if self.usuario.energia - self.consumo > 0:
                return True
            else:
                print("energia insuficiente para utilizar movimento!")
                return False
        elif self.fonte == "pp":
            if self.consumo - 1 >= 0:
                return True
            else:
                print("pp insuficiente para realizar movimento")
                return False
        else:
            print(f"ocorreu um erro! Fonte inválida para o movimento {self.nome}")
            input("pressione enter para continuar: ")

    def consumir(self):
        if self.fonte == "energia":
            self.usuario.energia -= self.consumo
        elif self.fonte == "pp":
            self.consumo -= 1
        else:
            print(f"ocorreu um erro! Fonte inválida para o movimento {self.nome}")
            input("pressione enter para continuar: ")

    def exibirInformacoes(self):
        dicionario_atributos = self.__dict__.items()
        for chave, valor in dicionario_atributos:
            if chave == "alvo_usuario" or valor == None or valor == 0:
                pass
            else: 
                print(f"{chave}: {valor}")

class Movimento(Acao):
    def __init__(self, nome, dano, precisao, fonte, consumo, chanceAlterarStatus, statusAlterado=None, duracaoStatus=None, alvo_usuario=False):
        Acao.__init__(self, nome, fonte, consumo, alvo_usuario)
        self.dano = dano
        self.precisao = precisao
        self.fonte = fonte
        self.consumo = consumo
        self.chanceAlterarStatus = chanceAlterarStatus
        self.statusAlterado = statusAlterado
        self.duracaoStatus = duracaoStatus

    def executar(self):
        if self.usuario.analisarStatus() and self.usuario.vida > 0:
            self.consumir()
            print(f"{self.usuario.nome} utilizou {self.nome}")
            if (self.usuario.precisao + self.precisao) / 2 >= randint(1, 100):
                print(f"atingiu {self.alvo.nome}")
                dano = self.dano 
                defesa = self.alvo.defesa

                if dano > defesa:
                    print(f"causou {dano - defesa} de dano")
                    self.alvo.vida -= dano - defesa 
                else:
                    print("o movimento foi ineficaz. Causou apenas 1 de dano")
                    self.alvo.vida -= 1 

                if self.chanceAlterarStatus >= randint(1, 100):
                    print(f"alterou o status de {self.alvo.nome} para {self.statusAlterado}")
                    duracao_efeito = randint(self.duracaoStatus[0], self.duracaoStatus[1])
                    if self.statusAlterado not in self.alvo.status:
                        self.alvo.status.append([self.statusAlterado, duracao_efeito])
            else:
                print("Não conseguiu acertar o movimento!")

        exibirLinha()

        self.alvo = None
        self.usuario = None

class Expansao(Acao):
    def __init__(self, nome, fonte, consumo, alvo_usuario=False):
        Acao.__init__(self, nome, fonte, consumo, alvo_usuario)
        self.fonte = fonte
        self.consumo = consumo
        self.ativa = False

    def ativar(self):
        if self.ativa:
            self.ativa = False
            print(f"{self.usuario.nome} desativou a expansao de domínio {self.nome}!")
        else:
            print(f"{self.usuario.nome} ativou a expansão de domínio {self.nome}!")    
            self.ativa = True

    def definirAlvos(self, alvos):
        self.alvo = alvos.copy()
        self.alvo.remove(self.usuario)

    def executar(self):
        if self.ativa:
            self.consumir()
            print(f"{self.nome} está ativa")
            for alvo in self.alvo:
                if self.nome == "muriokusho":
                    if "imobilizado" not in alvo.status:
                        alvo.status.append(["imobilizado", 1])
                        print(f"{self.alvo.nome} está imobilizado!")

                elif self.nome == "santuario":
                    alvo.vida -= 25
                    print(f"{alvo.nome} foi atingido pelos cortes do santuário. Recebeu 25 de dano.")
        else:
            print(f"{self.nome} está desativada!")
            self.ativa = False

        exibirLinha()

class Regeneracao(Acao):
    def __init__(self, nome, fonte, consumo, alvo_usuario=True):
        Acao.__init__(self, nome, fonte, consumo, alvo_usuario)
        self.consumo = consumo
        self.fonte = fonte
        self.consumo = consumo
        self.ativa = False

    def ativar(self):
        if self.ativa:
            self.ativa = False
            print(f"{self.usuario.nome} desativou a regeneração!")
        else:
            print(f"{self.usuario.nome} ativou a regeneração!")    
            self.ativa = True

    def executar(self):
        if self.ativa:
            if self.consumir():
                print(f"{self.usuario.nome} utilizou energia reversa para se regenerar!")
                vida_recuperada = self.usuario.vida * 0.15
                self.usuario.vida += vida_recuperada
                print(f"recuperou {vida_recuperada}")
            else:
                print("energia insuficiente para se regenerar. regeneração está desativada!")
                self.ativa = False
        exibirLinha()

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
            for personagem in self.personagens:
                personagem.energia += 40
                print(f"{personagem.nome} recuperou {40} de energia!")

            self.escolherAcoes()
            self.executarAcoes()
            self.aplicarEfeitoExpansoes()
            self.exibirInformacoes()


            vencedor = self.verificarVencedor()
            if vencedor != None:
                print(f"{vencedor.nome} venceu!")
                break

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
            if type(acao) == Regeneracao or type(acao) == Expansao:
                acao.ativar()
            else:
                acao.executar()

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
        # gojo
        azul = Movimento(nome="azul", dano=15, precisao=100, fonte="energia", consumo=15, chanceAlterarStatus=100, statusAlterado="imobilizado", duracaoStatus=[1, 2])
        vermelho = Movimento(nome="vermelho", dano=25, precisao=100, fonte="energia", consumo=35, chanceAlterarStatus=0)
        vazio_roxo = Movimento(nome="vazio roxo", dano=70, precisao=100, fonte="energia", consumo=60, chanceAlterarStatus=0)
        # sukuna
        clivar = Movimento(nome="clivar", dano=20, precisao=100, fonte="energia", consumo=25, chanceAlterarStatus=50, statusAlterado="sangrando", duracaoStatus=[1, 3])
        desmantelar = Movimento(nome="desmantelar", dano=75, precisao=100, fonte="energia", consumo=80, chanceAlterarStatus=0)
        flecha_fogo = Movimento(nome="flecha de fogo", dano=50, precisao=100, fonte="energia", consumo=65, chanceAlterarStatus=60, statusAlterado="queimando", duracaoStatus=[2, 4])
        # yuta
        golpe_com_espada = Movimento(nome="golpe com espada", dano=12, precisao=100, fonte="pp", consumo=7, chanceAlterarStatus=50, statusAlterado="sangrando", duracaoStatus=[1, 3])
        # itadori
        kokussen = Movimento(nome="Kokussen", dano=15, precisao=100, fonte="energia", consumo=15, chanceAlterarStatus=35, statusAlterado="atordoado", duracaoStatus=[1, 2])

        # golpes gerais
        soco = Movimento(nome="soco simples", dano=6, precisao=100, fonte="pp", consumo=25, chanceAlterarStatus=0)
        chute = Movimento(nome="Chute tranversal", dano=8, precisao=100, fonte="pp", consumo=15, chanceAlterarStatus=100, statusAlterado="atordoado", duracaoStatus=[1, 2])

        # expansão
        muriokusho = Expansao(nome="muriokusho", fonte="energia", consumo=35)
        santuario = Expansao(nome="santuario", fonte="energia", consumo=40)

        # personagens disponíveis
        personagens = []
        personagens.append(Personagem(nome="Satoru Gojo", vida=100, defesa=0, ataque=10, agilidade=100, energia=100, movimentos=[soco, chute], feiticos=[azul, vermelho, vazio_roxo], expansao=muriokusho, energia_reversa=True))
        personagens.append(Personagem(nome="Ryomen Sukuna", vida=100, defesa=0, ataque=10, agilidade=90, energia=100, movimentos=[soco, chute], feiticos=[clivar, desmantelar, flecha_fogo], expansao=santuario, energia_reversa=True))
        

        limparTela()
        if modo == "automatico":
            ...
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
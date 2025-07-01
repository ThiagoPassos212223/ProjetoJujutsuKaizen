import os # responsável por interagir com o sistema
from sys import platform, exit # responsável por identificar o OS e fechar o programa quando necessário.
from random import randint # responsável por gerar números pseudoaleatórios

# função responsável por identificar o sistema e com isso, utilizar o comando para limpar a tela
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

class Personagem:
    def __init__(self, nome, vida, defesa, ataque, agilidade, energia, movimentos, feiticos, expansao=None, energia_reversa=False):
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
        self.regeneracao = Regeneracao(nome, 30, self)
        # condições da batalha
        self.precisao = 100
        self.status = []

    def analisarStatus(self):
        if self.regeneracao.ativa:
            self.regeneracao.executar()

        joga = True
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
                    joga = False
                case "atordoado":
                    print(f"{self.nome} está atordoado! Não poderá realizar sua ação.")
                    joga = False
                case _:
                    print(f"ERRO! Um status não cadastrado foi detectado! {efeito_status}")
            
            if duracao - 1 == 0:
                self.status.remove(status)
            else: 
                status[1] -= 1

        exibirLinha()
        return joga
    
    def definirModo(self, modo="ia"):
        self.modo = "ia" if modo == "ia" else "jogador"

    def escolherAcao(self, alvos):
        limparTela()
        if self.modo == "ia":
            print("oi")    
        else:
            print(f"seleção de movimentos: ({self.nome})")
            print(f"vida: {self.vida}   energia: {self.energia}")
            print("a)escolher movimento  b)escolher feitiço   c)expandir domínio", end="   ")
            
            if self.energia_reversa:
                print(f"d)usar energia reversa")
            else:
                print("")

            escolha = input("selecione uma das opções: ")


            # verifica a seleção do usuário e com isso, carrega a lista de opções correta. 
            dicionario_opcoes = {"a": self.movimentos, "b": self.feiticos, "c": self.expansao, "d": self.regeneracao}

            try:
                acoes = dicionario_opcoes[escolha]
            except KeyError:
                print("opção inválida! Selecione uma opção válida!")
                return self.escolherAcao(alvos)

            if type(acoes) == list:
                if len(acoes) > 1:
                    for indice, acao in enumerate(acoes):
                        print(f"{indice}){acao.nome}")    
                    try:
                        escolha = int(input("selecione uma das opções: "))
                        acao_escolhida = acoes[escolha]
                    except ValueError:
                        print("Erro: o tipo esperado é um valor númerico inteiro positivo! Tente novamente!")
                        return self.escolherAcao(alvos)
                    except IndexError:
                        print("Erro: opção inválida, selecione uma das opções disponíveis!")
                        return self.escolherAcao(alvos)    
                else:
                    acao_escolhida = acoes[0]
            elif type(acoes) == Regeneracao or type(acoes) == Expansao:
                acao_escolhida = acoes

            # exibe informações sobre o movimento, feitiço ou expansão escolhida
            exibirLinha()
            print("informações adicionais")
            acao_escolhida.exibirInformacoes()

            escolha = input("a)confirmar escolha    b)cancelar\n")
            if "b" in escolha:
                return self.escolherAcao(alvos)
            else:
                if type(acao_escolhida) == Movimento or type(acao_escolhida) == Feitico:
                    acao_escolhida.definirUsuario(self)
                    acao_escolhida.definirAlvo(alvos)
                else:
                    acao_escolhida.definirUsuario(self)
                return acao_escolhida

class Efeito:
    def __init__(self, nome, duracao, alvo):
        self.nome = nome
        self.duracao = duracao
        self.alvo = alvo

# Molda outras classes, facilitando a utilização de funções em comum. 
class Acao:
    def __init__(self, nome, alvo_usuario=False):
        self.nome = nome
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

    def exibirInformacoes(self):
        dicionario_atributos = self.__dict__.items()
        for chave, valor in dicionario_atributos:
            if chave == "alvo_usuario" or valor == None or valor == 0:
                pass
            else: 
                print(f"{chave}: {valor}")

class Feitico(Acao):
    def __init__(self, nome, dano, precisao, consumo, chanceAlterarStatus, statusAlterado=None, duracaoStatus=None, alvo_usuario=False):
        Acao.__init__(self, nome, alvo_usuario)
        self.dano = dano
        self.precisao = precisao
        self.consumo = consumo
        self.chanceAlterarStatus = chanceAlterarStatus
        self.statusAlterado = statusAlterado
        self.duracaoStatus = duracaoStatus

    def consumir(self):
        # reduz a energia do usuário do feitiço
        if self.usuario.energia - self.consumo > 0:
            self.usuario.energia -= self.consumo
            return True
        else:
            return False

    def executar(self):
        if self.usuario.analisarStatus() and self.usuario.vida > 0:
            if self.consumir():
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
                    print("Não conseguiu acertar o feitiço!")
            else:
                print("energia insuficiente para utilizar feitiço")
        exibirLinha()

        self.alvo = None
        self.usuario = None
    
class Movimento(Acao):
    def __init__(self, nome, dano, precisao, pp, chanceAlterarStatus, statusAlterado=None, duracaoStatus=None, alvo_usuario=False):
        Acao.__init__(self, nome, alvo_usuario)
        self.dano = dano
        self.precisao = precisao
        self.pp = pp
        self.chanceAlterarStatus = chanceAlterarStatus
        self.statusAlterado = statusAlterado
        self.duracaoStatus = duracaoStatus

    def consumir(self):
        # reduz a energia do usuário do feitiço
        if self.pp - 1 >= 0:
            self.pp -= 1
            return True
        else:
            return False

    def executar(self):
        if self.usuario.analisarStatus() and self.usuario.vida > 0:
            if self.consumir():
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
            else:
                print("pp insuficiente para utilizar o movimento")
        exibirLinha()

        self.alvo = None
        self.usuario = None

class Expansao(Acao):
    def __init__(self, nome, consumo, alvo_usuario=False):
        Acao.__init__(self, nome, alvo_usuario)
        self.consumo = consumo
        self.ativa = False

    def consumir(self):
        # reduz a energia do usuário do feitiço
        if self.usuario.energia - self.consumo > 0:
            print(f"{self.nome} está ativa! {self.usuario.nome} utilizou {self.consumo} para manter o domínio ativado!")
            self.usuario.energia -= self.consumo
            return True
        else:
            print(f"{self.nome} está desativada! {self.usuario.nome} não têm energia suficiente para manter o domínio ativado!")
            return False

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
            if self.consumir():
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
    def __init__(self, nome, consumo, alvo_usuario=True):
        Acao.__init__(self, nome, alvo_usuario)
        self.consumo = consumo
        self.ativa = False

    def consumir(self):
        # reduz a energia do usuário do feitiço
        if self.usuario.energia - self.consumo > 0:
            self.usuario.energia -= self.consumo
            return True
        else:
            return False

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
        print("a)jogador vs jogador     b)jogador vs computador   c)sair")
        modo = input("selecione o modo de jogo: ")

        if "a" in modo:
            self.jogadorVsJogador() # redireciona o jogador para o modo jogador VS jogador
        elif "b" in modo:
            self.jogadorVsComputador() # redireciona o jogador para o modo jogador VS computador
        else:
            exit() # fecha o programa

    def escolherPersonagem(self, modo="automatico"):
        """É responsável por permitir que o usuário escolha os movimentos e feitiços"""
        # gojo
        mugen = Feitico(nome="mugen", dano=0, precisao=100, consumo=8, chanceAlterarStatus=100, statusAlterado="mugen", duracaoStatus=[1, 1], alvo_usuario=True)
        azul = Feitico(nome="azul", dano=15, precisao=100, consumo=15, chanceAlterarStatus=100, statusAlterado="imobilizado", duracaoStatus=[1, 2])
        vermelho = Feitico(nome="vermelho", dano=25, precisao=100, consumo=35, chanceAlterarStatus=0)
        vazio_roxo = Feitico(nome="vazio roxo", dano=70, precisao=100, consumo=60, chanceAlterarStatus=0)
        # sukuna
        clivar = Feitico(nome="clivar", dano=20, precisao=100, consumo=25, chanceAlterarStatus=50, statusAlterado="sangrando", duracaoStatus=[1, 3])
        desmantelar = Feitico(nome="desmantelar", dano=75, precisao=100, consumo=80, chanceAlterarStatus=0)
        flecha_fogo = Feitico(nome="flecha de fogo", dano=50, precisao=100, consumo=65, chanceAlterarStatus=60, statusAlterado="queimando", duracaoStatus=[2, 4])
        # yuta
        golpe_com_espada = Movimento(nome="golpe com espada", dano=12, precisao=100, pp=7, chanceAlterarStatus=50, statusAlterado="sangrando", duracaoStatus=[1, 3])
        # golpes
        soco = Movimento(nome="soco simples", dano=6, precisao=100, pp=25, chanceAlterarStatus=0)
        chute = Movimento(nome="Chute tranversal", dano=8, precisao=100, pp=15, chanceAlterarStatus=100, statusAlterado="atordoado", duracaoStatus=[1, 2])
        # expansão
        muriokusho = Expansao(nome="muriokusho", consumo=35)
        santuario = Expansao(nome="santuario", consumo=40)

        # personagens disponíveis
        personagens = []
        personagens.append(Personagem(nome="Satoru Gojo", vida=100, defesa=0, ataque=10, agilidade=100, energia=100, movimentos=[soco, chute], feiticos=[mugen, azul, vermelho, vazio_roxo], expansao=muriokusho, energia_reversa=True))
        personagens.append(Personagem(nome="Ryomen Sukuna", vida=100, defesa=0, ataque=10, agilidade=90, energia=100, movimentos=[soco, chute], feiticos=[clivar, desmantelar, flecha_fogo], expansao=santuario, energia_reversa=True))
        

        limparTela()
        if modo == "automatico":
            ...
        else:
            # looping responsável por exibir todos os personagens
            for n, personagem in enumerate(personagens):
                print(f"{n}){personagem.nome}")

            # validando escolha do usuário
            try:
                escolha = int(input("escolha um dos personagens: "))
                personagem = personagens[escolha]
                # os personagens são por padrão colocados como IA. 
                # Nesse caso, está definindo que o jogador é um humano.
                personagem.definirModo("manual")
                return personagem
            except ValueError:
                print("Erro: opção inválida!")
                return self.escolherPersonagem(modo)
            except IndexError:
                print("Erro: por favor, insira um valor númerico válido!")
                return self.escolherPersonagem(modo)

    def jogadorVsJogador(self):
        jogador1 = self.escolherPersonagem("manual")
        jogador2 = self.escolherPersonagem("manual")

        batalha = Batalha([jogador1, jogador2])
        batalha.looping()

    def jogadorVsComputador(self):
        ...

Main()
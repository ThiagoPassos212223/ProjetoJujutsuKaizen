import os # responsável por interagir com o sistema
from sys import platform, exit # responsável por identificar o OS e fechar o programa quando necessário.
from random import randint # responsável por gerar números pseudoaleatórios

class Personagem:
    def __init__(self, nome, vida, defesa, ataque, agilidade, energia, movimentos, feiticos, expansao):
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
        # condições da batalha
        self.precisao = 100
        self.status = []


    def analisarStatus(self):
        print(f"status: ({self.nome})")
        for status in self.status:
            match status:
                case "queimando":
                    print(f"{self.nome} está queimando! recebeu {5} de dano.")
                    status.alvo.vida -= 5
                case "sangrando":
                    print(f"{self.nome} está sangrando! recebeu {self.vida * 0.1} de dano.")
                    self.vida -= self.vida * 0.1
                case "imobilizado":
                    print(f"{self.nome} está imobilizado! Não é possível realizar sua ação.") 
                case "mugen":
                    print(f"está ativado!")
                case _:
                    print(f"ERRO! Um status não cadastrado foi detectado! {self.nome}")
        print("-" * 45)
        self.status.clear()

    def definirModo(self, modo="ia"):
        self.modo = "ia" if modo == "ia" else "jogador"

    def escolherAcao(self, alvos):
        if self.modo == "ia":
            print("oi")    
        else:
            print(f"seleção de movimentos: ({self.nome})")
            print(f"vida: {self.vida}   energia: {self.energia}")
            print("a)escolher movimento  b)escolher feitiço   c)expandir domínio")
            escolha = input("selecione uma das opções: ")

            match escolha:
                case "a":
                    tipo_acao = "movimento"
                case "b":
                    tipo_acao = "feitico"
                case "c":
                    tipo_acao = "expansao"
                case _:
                    tipo_acao = None

            if tipo_acao != None:
                match tipo_acao:
                    case "movimento":
                        acoes = self.movimentos
                    case "feitico":
                        acoes = self.feiticos
                    case "expansao":
                        acoes = self.expansao
                    case _:
                        acoes = None
                        print("erro!")

                for indice, acao in enumerate(acoes):
                    print(f"{indice}){acao.nome}")
                
                escolha = input("selecione uma das opções: ")
                if escolha.isnumeric():
                    escolha = int(escolha)
                    if escolha < len(acoes):
                        acao_escolhida = acoes[escolha]
                        
                        print(f"{acao_escolhida.nome}")
                        if type(acao_escolhida) == Expansao:
                            print(f"consumo: {acao_escolhida.consumo}")
                        else:
                            if acao_escolhida.dano > 0:
                                print(f"dano: {acao_escolhida.dano}")
                            print(f"precisão: {acao_escolhida.precisao}")
                            
                            if acao_escolhida.chanceAlterarStatus > 0:
                                print(f"chance de alterar status: {acao_escolhida.chanceAlterarStatus}")
                                print(f"status alterado: {acao_escolhida.statusAlterado}")
                                print(f"duracaoStatus: {acao_escolhida.duracaoStatus}")

                            if type(acao_escolhida) == Movimento:
                                print(f"pp: {acao_escolhida.pp}")
                            elif type(acao_escolhida) == Feitico:
                                print(f"consumo: {acao_escolhida.consumo}")      
                        escolha = input("a)confirmar escolha    b)cancelar\n")
                        if "b" in escolha:
                            pass
                        else:
                            if type(acao_escolhida) == Movimento or type(acao_escolhida) == Feitico:
                                acao_escolhida.definirUsuario(self)
                                acao_escolhida.definirAlvo(alvos)
                            else:
                                acao_escolhida.definirUsuario(self)
                            
                            print("-" * 45)
                            return acao_escolhida
                    else:
                        print("ERRO: escolha inválida!")
                else:
                    print("ERRO: O valor inserido não é inteiro!")
                        
            limparTela()
            return self.escolherAcao(alvos)

class Efeito:
    def __init__(self, nome, duracao, alvo, ativo=False):
        self.nome = nome
        self.duracao = duracao
        self.alvo = alvo
        self.ativo = ativo

# Molda outras classes, facilitando a utilização de funções em comum. 
class Acao:
    def __init__(self, nome, alvo_usuario=False):
        self.nome = nome
        self.alvo_usuario = alvo_usuario
    
    def definirUsuario(self, usuario):
        self.usuario = usuario

    def definirAlvo(self, lista_alvos):
        alvos = lista_alvos.copy()

        # remove o usuário da lista de alvos possíveis
        if self.alvo_usuario:
            self.alvo = self.usuario
        else: 
            alvos.remove(self.usuario)
        
        if len(alvos) == 1:
            self.alvo = alvos[0]
            return None
        else:
            for indice, alvo in enumerate(alvos):
                print(f"{indice}){alvo.nome}")
            
            indice_alvo = input("selecione o alvo da sua ação: ")
            if indice_alvo.isnumeric():
                if indice_alvo < len(alvos):
                    self.alvo = alvos[indice_alvo]
                    return None
                else:
                    print("ERRO: opção inválida!")
            else:
                print("ERRO: opção inválida! O valor inserido necessita ser um número!")

            # repete a função caso ocorra algum erro. A função só encerra o looping caso o usuário tenha selecionado um alvo válido.
            limparTela()
            return self.definirAlvo(lista_alvos)

class Feitico(Acao):
    def __init__(self, nome, dano, precisao, consumo, chanceAlterarStatus, statusAlterado=None, duracaoStatus=None, alvo_usuario=False):
        Acao.__init__(self, nome, alvo_usuario)
        self.dano = dano
        self.precisao = precisao
        self.consumo = consumo
        self.chanceAlterarStatus = chanceAlterarStatus
        self.statusAlterado = statusAlterado
        self.duracaoStatus = duracaoStatus
    
class Movimento(Acao):
    def __init__(self, nome, dano, precisao, pp, chanceAlterarStatus, statusAlterado=None, duracaoStatus=None, alvo_usuario=False):
        Acao.__init__(self, nome, alvo_usuario)
        self.dano = dano
        self.precisao = precisao
        self.pp = pp
        self.chanceAlterarStatus = chanceAlterarStatus
        self.statusAlterado = statusAlterado
        self.duracaoStatus = duracaoStatus

class Expansao(Acao):
    def __init__(self, nome, consumo, alvo_usuario=False):
        Acao.__init__(self, nome, alvo_usuario)
        self.nome = nome
        self.consumo = consumo


# função responsável por identificar o sistema e com isso, utilizar o comando para limpar a tela
def limparTela():
    comando = "cls" if "win" in platform else "clear"
    input("pressione enter para continuar: ")
    os.system(comando) 

# responsável por batalhas e funções relacionadas.
class Batalha:
    def __init__(self, personagens):
        self.personagens = personagens
        self.acoes = []
        self.efeitos = []
        self.expansoes = []

    def looping(self):
        while True:
            self.escolherAcoes()
            self.executarAcoes()
            self.aplicarEfeitos()
            self.analisarStatus()
            self.exibirInformacoes()


            vencedor = self.verificarVencedor()
            if vencedor != None:
                print(f"{vencedor.nome} venceu!")
                break

            limparTela()
        limparTela()

    def escolherAcoes(self):
        # organizando os personagens por velocidade, aqueles mais rapidos escolhem primeiro sua ação e as executam primeiro.
        self.personagens.sort(key=lambda p: p.agilidade, reverse=True)

        for personagem in self.personagens:
            self.acoes.append(personagem.escolherAcao(alvos=self.personagens))
            limparTela()

    def executarAcoes(self):
        for acao in self.acoes:
            if acao.nome == "nenhuma":
                print(acao.usuario.nome)
                print("-" * 45)
            else:
                print(f"{acao.usuario.nome}")
                print("-" * 45)
                if acao.usuario.vida > 0:
                    if not "imobilizado" in acao.usuario.status:
                        if acao.alvo.vida > 0:
                            if not "mugen" in acao.alvo.status or acao.alvo.statusAlterado == "quebrar mugen":
                                if type(acao) == Expansao: 
                                    if not acao in self.expansoes:
                                        if acao.usuario.energia - acao.consumo >= 0:
                                            acao.usuario.energia -= acao.consumo
                                        else:
                                            print("energia insuficiente para expandir domínio")
                                    else:
                                        print("expansão de domínio desativada!")
                                        self.expansoes.remove(acao)

                                
                                elif type(acao) == Feitico:
                                    if acao.usuario.energia - acao.consumo >= 0:
                                        acao.usuario.energia -= acao.consumo

                                        print(f"{acao.usuario.nome} utilizou {acao.nome}")
                                        if (acao.precisao + acao.usuario.precisao)/2 >= randint(1, 100):
                                            print(f"atingiu {acao.alvo.nome}")
                                            dano = acao.dano 
                                            defesa = acao.alvo.defesa

                                            if dano > defesa:
                                                print(f"causou {dano - defesa} de dano")
                                                acao.alvo.vida -= dano - defesa 
                                            else:
                                                print("o movimento foi ineficaz. Causou apenas 1 de dano")
                                                acao.alvo.vida -= 1 

                                            if acao.chanceAlterarStatus >= randint(1, 100):
                                                print(f"alterou o status de {acao.alvo.nome} para {acao.statusAlterado}")
                                                duracao_efeito = randint(acao.duracaoStatus[0], acao.duracaoStatus[1])
                                                efeito = Efeito(nome=acao.statusAlterado, duracao=duracao_efeito, alvo=acao.alvo)
                                                self.efeitos.append(efeito)
                                        else:
                                            print("Não conseguiu acertar o feitiço!")
                                    else:
                                        print("energia insuficiente para utilizar feitiço")
                                    
                                elif type(acao) == Movimento:
                                    if acao.pp  > 0:
                                        acao.pp -= 1
                                        print(f"{acao.usuario.nome} utilizou {acao.nome}")
                                        if (acao.precisao + acao.usuario.precisao)/2 >= randint(1, 100):
                                            print(f"atingiu {acao.alvo.nome}")
                                            dano = acao.dano 
                                            defesa = acao.alvo.defesa

                                            if dano > defesa:
                                                print(f"causou {dano - defesa} de dano")
                                                acao.alvo.vida -= dano - defesa 
                                            else:
                                                print("o movimento foi ineficaz. Causou apenas 1 de dano")
                                                acao.alvo.vida -= 1 
                                        else:
                                            print("Não conseguiu acertar o movimento!")
                                    else:
                                        print("pp insuficiente para utilizar o movimento")
                                self.aplicarEfeitos()
                            else:
                                print(f"não foi possível atingir {acao.alvo.nome} pois o mugen está ativado!")
                    else:
                        print(f"{acao.usuario.nome} está imobilizado!")

                        print("-" * 45)
        self.acoes.clear()
    
    def aplicarEfeitos(self):
        print("Aplicação de efeitos")
        for efeito in self.efeitos:
            match efeito.nome:
                case "queimando":
                    efeito.alvo.status.append("queimando")
                case "sangrando":
                    efeito.alvo.status.append("sangrando")
                case "imobilizado":
                    efeito.alvo.status.append("imobilizado")
                case _:
                    print(f"ERRO! Um efeito não cadastrado foi detectado! {efeito.nome}")

            efeito.duracao -= 1 
            if efeito.duracao == 0:
                self.efeitos.remove(efeito)
        print("-" * 45)

    def analisarStatus(self):
        for personagem in self.personagens:
            personagem.analisarStatus()

    def exibirInformacoes(self):
        print("fim de turno")
        for personagem in self.personagens:
            print(f"nome: {personagem.nome}    vida:  {personagem.vida}")

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
        while True:
            print("bem vindo!")
            print("modos de jogo: ")
            print("a)jogador vs jogador     b)jogador vs computador   c)sair")
            modo = input("selecione o modo de jogo: ")

            limparTela()
            if "a" in modo:
                self.jogadorVsJogador() # redireciona o jogador para o modo jogador VS jogador
            elif "b" in modo:
                self.jogadorVsComputador() # redireciona o jogador para o modo jogador VS computador
            else:
                exit() # fecha o programa

    def escolhaPersonagem(self, modo="automatico"):
        """É responsável por permitir que o usuário escolha os movimentos e feitiços"""
        # gojo
        azul = Feitico(nome="azul", dano=15, precisao=100, consumo=15, chanceAlterarStatus=100, statusAlterado="imobilizado", duracaoStatus=[1, 3])
        vermelho = Feitico(nome="vermelho", dano=25, precisao=100, consumo=35, chanceAlterarStatus=0)
        vazio_roxo = Feitico(nome="vazio roxo", dano=70, precisao=100, consumo=60, chanceAlterarStatus=0)
        # sukuna
        clivar = Feitico(nome="clivar", dano=20, precisao=100, consumo=25, chanceAlterarStatus=50, statusAlterado="sangrando", duracaoStatus=[1, 3])
        desmantelar = Feitico(nome="desmantelar", dano=75, precisao=100, consumo=80, chanceAlterarStatus=0)
        flecha_fogo = Feitico(nome="flecha de fogo", dano=50, precisao=100, consumo=65, chanceAlterarStatus=60, statusAlterado="queimando", duracaoStatus=[2, 4])
        # golpes
        soco = Movimento(nome="soco simples", dano=6, precisao=100, pp=25, chanceAlterarStatus=100, statusAlterado="atordoado", duracaoStatus=[2, 4])
        chute = Movimento(nome="Chute tranversal", dano=8, precisao=100, pp=15, chanceAlterarStatus=0)
        # expansão
        muriokusho = Expansao(nome="muriokusho", consumo=35)
        santuario = Expansao(nome="santuario", consumo=40)

        # personagens disponíveis
        personagens = []
        personagens.append(Personagem(nome="Satoru Gojo", vida=100, defesa=0, ataque=10, agilidade=100, energia=100, movimentos=[soco, chute], feiticos=[azul, vermelho, vazio_roxo], expansao=muriokusho))
        personagens.append(Personagem(nome="Ryomen Sukuna", vida=100, defesa=0, ataque=10, agilidade=90, energia=100, movimentos=[soco, chute], feiticos=[clivar, desmantelar, flecha_fogo], expansao=santuario))
        
        if modo == "automatico":
            ...
        else:
            while True:
                # looping responsável por exibir todos os personagens
                for n, personagem in enumerate(personagens):
                    print(f"{n}){personagem.nome}")

                escolha = input("escolha um dos personagens: ")
                # validando escolha do usuário
                if escolha.isnumeric(): 
                    if int(escolha) < len(personagens):
                        limparTela()
                        personagem = personagens[int(escolha)]
                        # os personagens são por padrão colocados como IA. 
                        # Nesse caso, está definindo que o jogador é um humano.
                        personagem.definirModo("manual")
                        return personagem
                    else:
                        print("Erro: opção inválida!")
                else:
                    print("Erro: por favor, insira um valor númerico válido!")
                limparTela()
            
    def jogadorVsJogador(self):
        jogador1 = self.escolhaPersonagem("manual")
        jogador2 = self.escolhaPersonagem("manual")

        batalha = Batalha([jogador1, jogador2])
        batalha.looping()

    def jogadorVsComputador(self):
        ...

Main()

        

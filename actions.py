from utils import limparTela, exibirLinha, sortearNumero

# Molda outras classes, facilitando a utilização de funções em comum. 
class Acao:
    def __init__(self, nome, tipo, consumo, precisao, alvo_usuario=False):
        self.nome = nome
        self.tipo = tipo
        self.consumo = consumo
        self.precisao = precisao
        self.alvo_usuario = alvo_usuario
        self.funcoes = None
    
    def adicionarFuncoes(self, funcoes):
        self.funcoes = funcoes

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
            elif chave == "funcoes":
                pass
            else: 
                print(f"{chave}: {valor}")

    def podeSerUtilizado(self):
        if self.tipo == "energia":
            # reduz a energia do usuário do feitiço
            if self.usuario.energia - self.consumo > 0:
                return True
            else:
                return False
        elif self.tipo == "pp":
            if self.consumo - 1 >= 0:
                return True
            else:
                return False
        else:
            print(f"ocorreu um erro! Fonte inválida para o movimento {self.nome}")
            input("pressione enter para continuar: ")

    def consumir(self):
        if self.tipo == "energia":
            self.usuario.energia -= self.consumo
        elif self.tipo == "pp":
            self.consumo -= 1
        else:
            print(f"ocorreu um erro! Fonte inválida para o movimento {self.nome}")
        
    def utilizar(self):
        if self.usuario.analisarStatus() and self.usuario.vida > 0:
            self.consumir()
            print(f"{self.usuario.nome} utilizou {self.nome}")
            if (self.usuario.precisao + self.precisao) / 2 >= sortearNumero(1, 100):
                print(f"atingiu {self.alvo.nome}")
                for funcao in self.funcoes:
                    funcao.executar(self.alvo)
            else:
                print("Não conseguiu acertar o movimento!")

        exibirLinha()
        self.alvo = None
        self.usuario = None
    
class Dano:
    def __init__(self, dano, precisao=100, acerto_garantido=False):
        self.dano = dano
        self.precisao = precisao
        self.acerto_garantido = acerto_garantido

    def executar(self, alvo):
        if self.acerto_garantido or self.precisao >= sortearNumero(1, 100):
            print(f"causou {self.dano} de dano")
            alvo.vida -= self.dano
        else:
            print("não conseguiu atingir o alvo.")

class Efeito:
    def __init__(self, status, duracao, precisao=100, acerto_garantido=False):
        self.status = status
        self.duracao = duracao
        self.precisao = precisao
        self.acerto_garantido = acerto_garantido
    
    def executar(self, alvo):
        if self.acerto_garantido or self.precisao >= sortearNumero(1, 100):
            print(f"alterou o status de {alvo.nome} para {self.status}")

            if len(self.duracao) > 1:
                duracao_efeito = sortearNumero(self.duracao[0], self.duracao[1])
            else:
                duracao_efeito = self.duracao

            if self.status not in alvo.status:
                alvo.status.append([self.status, duracao_efeito])
        

class Expansao:
    def __init__(self, efeito, duracao):
        self.efeito = efeito
        self.duracao = duracao

    def executar(self, alvo):
        print(f"{self.nome} está ativa")
        for alvo in self.alvo:    
            alvo.status.append(["imobilizado", 1])
            print(f"{self.alvo.nome} está imobilizado!")

        exibirLinha()

class ConjuntoAcoes:
    def __init__(self):
        ...

    def adicionarFeiticos(self, nome_personagem):
        # gojo
        mugen = Acao(nome="mugen", precisao=100, tipo="energia", consumo=20)
        mugen.adicionarFuncoes([Efeito(status="mugen ativado", duracao=[3, 4], precisao=100, acerto_garantido=True)])

        azul = Acao(nome="azul", precisao=100, tipo="energia", consumo=15)
        azul.adicionarFuncoes([Efeito(status="imobilizado", duracao=[1, 3], precisao=100, acerto_garantido=True)])
        
        vermelho = Acao(nome="vermelho", precisao=100, tipo="energia", consumo=35)
        vermelho.adicionarFuncoes([Dano(dano=35, precisao=100, acerto_garantido=True), Efeito("atordoado", [1, 2], precisao=30, acerto_garantido=False)])
        
        vazio_roxo = Acao(nome="vazio roxo", precisao=100, tipo="energia", consumo=60)
        vazio_roxo.adicionarFuncoes([Dano(70, precisao=100, acerto_garantido=True)])
        # sukuna
        clivar = Acao(nome="clivar", precisao=100, tipo="energia", consumo=25)
        clivar.adicionarFuncoes([Dano(15, precisao=100, acerto_garantido=True), Efeito("sangrando", [1, 3], precisao=45, acerto_garantido=False)])

        desmantelar = Acao(nome="desmantelar", precisao=100, tipo="energia", consumo=80)
        desmantelar.adicionarFuncoes([Dano(50, precisao=100, acerto_garantido=True), Efeito("sangrando", [1, 3], precisao=100, acerto_garantido=False)])

        flecha_fogo = Acao(nome="flecha de fogo", precisao=100, tipo="energia", consumo=65)
        flecha_fogo.adicionarFuncoes([Dano(65, precisao=100, acerto_garantido=True), Efeito("queimando", [2, 4], precisao=55, acerto_garantido=False)])

        self.feiticos = {
            "Satoru Gojo": [mugen, azul, vermelho, vazio_roxo],
            "Ryomen Sukuna": [clivar, desmantelar, flecha_fogo] 
        }
        return self.feiticos[nome_personagem]

    def adicionarMovimentos(self, nome_personagem):
        # golpes gerais
        soco = Acao(nome="soco simples", precisao=100, tipo="pp", consumo=25)
        soco.adicionarFuncoes([Dano(8, precisao=100, acerto_garantido=True)])
        chute = Acao(nome="Chute tranversal", precisao=100, tipo="pp", consumo=15)
        chute.adicionarFuncoes([Dano(12, precisao=100, acerto_garantido=True), Efeito("atordoado", [1, 3], precisao=100, acerto_garantido=False)])
        
        self.golpes = {
            "Satoru Gojo": [soco, chute],
            "Ryomen Sukuna": [soco, chute]
        }
        return self.golpes[nome_personagem]

    def adicionarExpansoes(self, nome_personagem):
        # expansão
        muriokusho = Acao(nome="muriokusho", tipo="energia", consumo=35, precisao=200)
        muriokusho.adicionarFuncoes([Expansao("imobilizado", [1, 4])])
        santuario = Acao(nome="santuario", tipo="energia", consumo=40, precisao=200)
        santuario.adicionarFuncoes([Expansao("santuario", [2, 5])])

        self.expansoes = {
            "Satoru Gojo": muriokusho,
            "Ryomen Sukuna": santuario
        }

        return self.expansoes[nome_personagem]

    def adicionarAcoesPersonagem(self, personagem):
        personagem.feiticos = self.adicionarFeiticos(personagem.nome)
        personagem.movimentos = self.adicionarMovimentos(personagem.nome)
        personagem.expansao = self.adicionarExpansoes(personagem.nome)

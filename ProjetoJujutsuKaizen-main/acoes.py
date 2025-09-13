from utilidades import limparTela, exibirLinha, sortearNumero, selecioneOpcao

# Responsável por moldar uma ação. 
class Acao:
    def __init__(self, nome, fonte, consumo, acerto_garantido=False, precisao=100, alvo_usuario=False):
        self.nome = nome
        self.tipo = "acao"
        self.fonte = fonte
        self.consumo = consumo
        self.acerto_garantido = acerto_garantido
        self.precisao = precisao
        self.alvo_usuario = alvo_usuario

    def adicionarFuncoes(self, funcoes):
        self.funcoes = funcoes

    def definirUsuario(self, usuario):
        self.usuario = usuario

    def definirAlvo(self, lista_alvos):
        limparTela(esperar=False)
        
        alvos = lista_alvos.copy() 
        if self.alvo_usuario:
            self.alvo = self.usuario
        else:
            alvos.remove(self.usuario)
            if len(alvos) == 1:
                self.alvo = alvos[0]
            else:
                nome_alvos = [alvo.nome for alvo in alvos]
                indice_escolhido = selecioneOpcao(lista_original=nome_alvos, mensagem="selecione um alvo:")
                self.alvo = alvos[indice_escolhido]
    
    def exibirInformacoes(self):
        dicionario_atributos = self.__dict__.items()
        for chave, valor in dicionario_atributos:
            if not(chave == "alvo_usuario" or valor == None or valor == 0 or chave == "funcoes"):
                print(f"{chave}: {valor}")

    def podeSerUtilizado(self):
        if self.fonte == "energia":
            return self.usuario.energia - self.consumo > 0
        elif self.fonte == "pp":
            return self.consumo - 1 >= 0
        else:
            print(f"ocorreu um erro! Fonte inválida para o movimento {self.nome}")

    def consumir(self):
        if self.fonte == "energia":
            self.usuario.energia -= self.consumo
        elif self.fonte == "pp":
            self.consumo -= 1
        else:
            print(f"ocorreu um erro! Fonte inválida para o movimento {self.nome}")
        
    def utilizar(self):
        self.consumir()
        print(f"{self.usuario.nome} utilizou {self.nome}")
        
        for funcao in self.funcoes:
            if not(type(funcao) == Expansao):
                funcao.executar(self.alvo)
            else:
                funcao.executar()
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
            for status_alvo in alvo.status:
                if "mugen ativado" in status_alvo:
                    mugen_ativado = True
                    break
            else:
                mugen_ativado = False

            if not(mugen_ativado):
                print(f"atingiu {alvo.nome}")
                print(f"causou {self.dano} de dano")
                alvo.vida -= self.dano
            else:
                print(f"não conseguiu atingir {alvo.nome}, pois mugen está ativado!")
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
            for status_alvo in alvo.status:
                if "mugen ativado" in status_alvo:
                    mugen_ativado = True
                    break
            else:
                mugen_ativado = False

            if not(mugen_ativado):
                print(f"alterou o status de {alvo.nome} para {self.status}")
                if type(self.duracao) == list:
                    duracao_efeito = sortearNumero(self.duracao[0], self.duracao[1])
                else:
                    duracao_efeito = self.duracao
                if self.status not in alvo.status:
                    alvo.status.append([self.status, duracao_efeito])
            else:
                print("não é possível aplicar efeito, pois o mugen está ativado!")

class Expansao:
    def __init__(self, nome, consumo):
        self.tipo = "expansao"
        self.nome = nome
        self.consumo = consumo
        self.ativada = False
    
    def definirUsuario(self, usuario):
        self.usuario = usuario

    def definirAlvos(self, personagens):
        self.alvos = personagens.copy()
        self.alvos.remove(self.usuario)

    def podeSerUtilizado(self):
        return self.usuario.energia - self.consumo >= 0
    
    def utilizar(self):
        self.usuario.energia -= self.consumo

    def executar(self):
        print(f"{self.usuario.nome} está invocando sua expansão de domínio")
        if self.podeSerUtilizado():
            print(f"{self.nome} está ativa")
            self.ativada = True
        else:
            print(f"{self.nome} não é possível ser ativada. Energia insuficiente.")
            
        return self.ativada
    
    def aplicarEfeitos(self):
        if self.podeSerUtilizado():
            self.utilizar()
            for alvo in self.alvos:
                match self.nome:
                    case "santuario":
                        dano = 25
                        alvo.vida -= dano
                        print(f"{alvo.nome} foi atingido pelos cortes do santuario! recebeu {dano} de dano!")
                    case "muriokusho":
                        if "imobilizado" not in alvo.status:
                            alvo.status.append(["imobilizado", 1])
                            print(f"{alvo.nome} foi atingido pelos efeitos do Muriokusho! Está imobilizado!")
                    case _:
                        print("essa expansão ainda não foi cadastrada, consulte o desenvolvedor para mais informações!")
        else:
            print("expansão não pode ser utilizada! Energia insuficiente!")

    def exibirInformacoes(self):
        dicionario_atributos = self.__dict__.items()
        for chave, valor in dicionario_atributos:
            if chave == "usuario" or valor == None or valor == 0:
                pass
            elif chave == "ativada":
                if valor: 
                    print("expansão está ativada")
                else:
                    print("expansão está desativada")
            else: 
                print(f"{chave}: {valor}")

class ConjuntoAcoes:
    def __init__(self):
        ...

    def adicionarFeiticos(self, nome_personagem):
        # gojo
        mugen = Acao(nome="mugen", precisao=100, fonte="energia", consumo=35, alvo_usuario=True)
        mugen.adicionarFuncoes([Efeito(status="mugen ativado", duracao=[1, 3], precisao=200, acerto_garantido=True)])
        azul = Acao(nome="azul", precisao=100, fonte="energia", consumo=15)
        azul.adicionarFuncoes([Efeito(status="imobilizado", duracao=[1, 3], precisao=100, acerto_garantido=True)])
        vermelho = Acao(nome="vermelho", precisao=100, fonte="energia", consumo=35)
        vermelho.adicionarFuncoes([Dano(dano=35, precisao=100, acerto_garantido=True), Efeito("atordoado", [1, 2], precisao=30, acerto_garantido=False)])
        vazio_roxo = Acao(nome="vazio roxo", precisao=100, fonte="energia", consumo=60)
        vazio_roxo.adicionarFuncoes([Dano(70, precisao=100, acerto_garantido=True)])
        # sukuna
        clivar = Acao(nome="clivar", precisao=100, fonte="energia", consumo=25)
        clivar.adicionarFuncoes([Dano(15, precisao=100, acerto_garantido=True), Efeito("sangrando", [1, 3], precisao=45, acerto_garantido=False)])
        desmantelar = Acao(nome="desmantelar", precisao=100, fonte="energia", consumo=80)
        desmantelar.adicionarFuncoes([Dano(50, precisao=100, acerto_garantido=True), Efeito("sangrando", [1, 3], precisao=100, acerto_garantido=False)])
        flecha_fogo = Acao(nome="flecha de fogo", precisao=100, fonte="energia", consumo=65)
        flecha_fogo.adicionarFuncoes([Dano(65, precisao=100, acerto_garantido=True), Efeito("queimando", [2, 4], precisao=55, acerto_garantido=False)])
        # yuta
        fala_amaldicoada1 = Acao(nome="fala amaldiçoada: não se mova!", fonte="energia", consumo=20, precisao=100, alvo_usuario=False)
        fala_amaldicoada1.adicionarFuncoes([Efeito("imobilizado", duracao=[1, 4], precisao=100, acerto_garantido=False)])
        fala_amaldicoada2 = Acao(nome="fala amaldiçoada: morra!", fonte="energia", consumo=50, precisao=100, alvo_usuario=False)
        fala_amaldicoada2.adicionarFuncoes([Dano(50, precisao=100, acerto_garantido=False)])
        manifestar_rika = Acao(nome="manifestar rika", fonte="pp", consumo=1, precisao=200, alvo_usuario=True)
        manifestar_rika.adicionarFuncoes([Efeito("rika_manifestada", duracao=[2, 5], precisao=100, acerto_garantido=False)]) 

        # golpes comuns com energia reversa
        regeneracao = Acao(nome="regeneração", fonte="energia", consumo=40, precisao=200, alvo_usuario=True)
        regeneracao.adicionarFuncoes([Efeito("regeneração", 1, precisao=100, acerto_garantido=True)])

        self.feiticos = {
            "Satoru Gojo": [mugen, azul, vermelho, vazio_roxo, regeneracao],
            "Ryomen Sukuna": [clivar, desmantelar, flecha_fogo, regeneracao],
            "Yuta Okkotsu": [fala_amaldicoada1, fala_amaldicoada2, manifestar_rika, regeneracao]
        }
        return self.feiticos[nome_personagem]

    def adicionarGolpes(self, nome_personagem):
        # golpes gerais
        soco = Acao(nome="soco simples", precisao=100, fonte="pp", consumo=25)
        soco.adicionarFuncoes([Dano(8, precisao=100, acerto_garantido=True)])
        chute = Acao(nome="Chute tranversal", precisao=100, fonte="pp", consumo=15)
        chute.adicionarFuncoes([Dano(12, precisao=100, acerto_garantido=True), Efeito("atordoado", [1, 3], precisao=100, acerto_garantido=False)])
        
        self.golpes = {
            "Satoru Gojo": [soco, chute],
            "Ryomen Sukuna": [soco, chute],
            "Yuta Okkotsu": [soco, chute]
        }
        return self.golpes[nome_personagem]

    def adicionarExpansoes(self, nome_personagem):
        # expansão
        muriokusho = Expansao(nome="muriokusho", consumo=35)
        santuario = Expansao(nome="santuario", consumo=40)
        amorMutuo = Expansao(nome="amor mutuo", consumo=0)

        self.expansoes = {
            "Satoru Gojo": muriokusho,
            "Ryomen Sukuna": santuario,
            "Yuta Okkotsu": amorMutuo
        }
        return self.expansoes[nome_personagem]

    def adicionarAcoesPersonagem(self, personagem):
        self.feiticos = self.adicionarFeiticos(personagem.nome)
        self.golpes = self.adicionarGolpes(personagem.nome)
        self.expansao = self.adicionarExpansoes(personagem.nome)
        personagem.adicionarMovimentos(feiticos=self.feiticos, golpes=self.golpes, expansao=self.expansao)
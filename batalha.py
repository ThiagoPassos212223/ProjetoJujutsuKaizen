import os
from sys import platform
from random import randint

def limparTela():
    comando = "cls" if "win" in platform else "clear"
    input("pressione enter para continuar: ")
    os.system(comando) 

class Batalha:
    def __init__(self, personagens):
        self.personagens = personagens
        self.eventos = []
        self.expansoes = []

    def cicloBatalha(self):
        while True:
            # os usuários recebem 20 de energia a cada turno
            for personagem in self.personagens:
                personagem.energia += 15

            self.escolhaAcoes()
            self.execucaoAcoes()
            self.executarExpansoes()

            vencedor = self.verificarVencedor()
            if vencedor != None:
                print(f"{vencedor.nome} venceu a batalha!")
                limparTela()
                break
    
    def escolhaAcoes(self):
        for personagem in self.personagens:
            if personagem.modo == "ia":
                print("oi")    
            else:
                looping = True
                while looping:
                    print(f"seleção de movimentos: ({personagem.nome})")
                    print(f"vida: {personagem.vida}   energia: {personagem.energia}")
                    print("a)escolher movimento  b)escolher feitiço   c)expandir domínio    d)utilizar energia reversa ")
                    escolha = input("selecione uma das opções: ")
                    match escolha:
                        case "a":
                            for n, movimento in enumerate(personagem.movimentos):
                                print(f"{n}){movimento.nome}")

                            escolha = input("selecione um movimento: ")
                            if escolha.isnumeric():
                                if int(escolha) < len(personagem.movimentos):
                                    limparTela()
                                    movimento = personagem.movimentos[int(escolha)]
                                    self.eventos.append(["movimento", personagem, movimento])
                                    looping = False
                                    break
                            print("opção invalida! ")
                        case "b":
                            for n, feitico in enumerate(personagem.feiticos):
                                print(f"{n}){feitico.nome}")

                            escolha = input("selecione um feitico: ")
                            if escolha.isnumeric():
                                if int(escolha) < len(personagem.feiticos):
                                    limparTela()
                                    feitico = personagem.feiticos[int(escolha)]
                                    self.eventos.append(["feitico", personagem, feitico])
                                    looping = False
                                    break
                            
                            print("opção invalida!")
                        case "c":
                            personagem.expansao.definirUsuario(personagem)
                            self.eventos.append(["expansao", personagem.expansao])
                            looping = False
                        case "d":
                            self.eventos.append(["energia reversa", personagem])
                            looping=False
                        case _:
                            print("Erro: selecione uma opção válida")
                    limparTela()
    
    def execucaoAcoes(self):
        print("Executando ações!")
        print("-" * 45)
        for evento in self.eventos:
            if evento[0] == "feitico":
                usuario = evento[1]
                feitico = evento[2]

                alvos = self.personagens.copy()
                alvos.remove(usuario)
                alvo = alvos[0]

                print(f"turno do(a) {usuario.nome}:")                
                if alvo.vida > 0:
                    if self.analiseStatus(usuario):
                        if usuario.energia - feitico.gastoEnergia >= 0:
                            usuario.energia -= feitico.gastoEnergia
                            if usuario.precisao + feitico.precisao >= randint(1, alvo.evasao):
                                print(f"{usuario.nome} utilizou o feitiço {feitico.nome}")
                                if feitico.dano > 0:
                                    dano = usuario.ataque + feitico.dano
                                    defesa = alvo.defesa

                                    dano_real = (defesa - dano) * -1
                                    if dano_real <= 0:
                                        print("o feitiço não causou danos consideráveis, causou apenas 1 de dano!")
                                        alvo.vida -= 1
                                    else:
                                        print(f"Causou {dano_real} de dano!")
                                        alvo.vida -= dano_real

                                if feitico.chanceAlterarStatus > 0:
                                    if feitico.chanceAlterarStatus >= randint(1, 100):
                                        alvo.status.append([feitico.statusAlterado, feitico.duracaoStatus])
                                        print(f"{alvo.nome} está {feitico.statusAlterado}!")
                        else:
                            print("O usuário não tem energia suficiente para utilizar o feitiço!")

            elif evento[0] == "movimento":
                usuario = evento[1]
                movimento = evento[2]

                alvos = self.personagens.copy()
                alvos.remove(usuario)
                alvo = alvos[0]
                
                print(f"turno do(a) {usuario.nome}:")                

                if alvo.vida > 0:
                    if self.analiseStatus(usuario):
                        if movimento.pp - 1 >= 0:
                            movimento.pp -= 1
                            if usuario.precisao + movimento.precisao >= randint(1, alvo.evasao):
                                print(f"{usuario.nome} utilizou o movimento {movimento.nome}")
                                if movimento.dano > 0:
                                    dano = usuario.ataque + movimento.dano
                                    defesa = alvo.defesa

                                    if randint(1, 100) == 100:
                                        print("acertou um black flash! Causará o dobro de dano!")
                                        print(f"dano base: {dano}  dano atual: {dano * 2}")
                                        dano *= 2

                                    dano_real = (defesa - dano) * -1
                                    if dano_real <= 0:
                                        print("o movimento não causou danos consideráveis, causou apenas 1 de dano!")
                                        alvo.vida -= 1
                                    else:
                                        print(f"o movimento causou {dano_real} de dano!")
                                        alvo.vida -= dano_real
                                if movimento.chanceAlterarStatus > 0:
                                    if movimento.chanceAlterarStatus >= randint(1, 100):
                                        alvo.status.append([movimento.statusAlterado, movimento.duracaoStatus])
                                        print(f"{alvo.nome} está {movimento.statusAlterado}!")
                                
                        else:
                            print("PP esgotado, não é possível utilizar esse movimento!")
            
            elif evento[0] == "expansao":
                expansao = evento[1]
                usuario = evento[1].usuario
                if usuario.vida > 0:
                    if usuario.energia - expansao.gastoEnergia >= 0:
                        usuario.energia -= expansao.gastoEnergia 
                        self.expansoes.append(expansao)
                        self.expansaoDominio(expansao)

                    else:
                        print(f"{expansao.nome} não pode ser conjurado por causa da baixa energia do usuário!")
                else:
                    print(f"{expansao.nome} foi quebrado, o usuário sofreu graves danos e não consegue manter o domínio!")
            elif evento[0] == "energia reversa":
                if evento[1].energia - 20 >= 0:
                    evento[1].vida += 35
                    print(f"{evento[1].nome} utilizou energia reversa para recuperar 35 de vida!")
                else:
                    print(f"{evento[1].nome} não conseguiu utilizar energia reversa para se recuperar, pois não tem energia suficiente!")


            print("-" * 45)
         
        limparTela()
        self.eventos.clear()
        
    def analiseStatus(self, personagem):
        for status in personagem.status:
            print(f"o jogador está {status[0]}")
            if status[0] == "queimando":
                personagem.vida -= 8
                print(f"{personagem.nome} está queimando, recebeu {8} de dano!")
                return True

            elif status[0] == "sangrando":
                personagem.vida -= personagem.vida * 0.15
                print(f"{personagem.nome} está sangrando, recebeu {personagem.vida * 0.15} de dano!")
                return True

            elif status[0] == "imobilizado":
                if status[1] > 0:
                    status[1] -= 1
                    print(f"{personagem.nome} está imobilizado! não é possível agir nesse turno!")
                    return False
                else:
                    personagem.status.remove(status)

            elif status[0] == "atordoado":
                print(f"{personagem.nome} está atordoado!")
                if randint(1, 3) == 1:
                    print(f"{personagem.nome} está desorientado, não consegue realizar sua ação")
                    return False
                else:
                    return True
        else:
            return True

    def executarExpansoes(self):
        if len(self.expansoes) > 0:
            print("expansões de domínio")
            for expansao in self.expansoes:
                self.expansaoDominio(expansao)
            print("-"* 45)


    def expansaoDominio(self, expansao):
        alvos = self.personagens.copy()
        alvos.remove(expansao.usuario)

        if expansao.usuario.vida > 0:
            if expansao.usuario.energia - expansao.gastoEnergia >= 0:
                expansao.usuario.energia -= expansao.gastoEnergia
                print(f"{expansao.nome} está ativado!")
                if expansao.nome == "muriokusho":
                    for alvo in alvos:
                        print(f"{alvo.nome} foi atingido pelos efeitos do muriokusho! está imóvel!")
                        alvo.status.append(["imobilizado", 1])


                elif expansao.nome == "santuario":
                    for alvo in alvos:
                        alvo.vida -= 8
                        print(f"{alvo.nome} foi atingido pelos cortes do santuário! Recebeu {8} de dano")
            else:
                print(f"{expansao.nome} foi desfeito por causa da baixa energia do usuário!")
                self.expansoes.remove(expansao)
        else:
            print("o domínio foi desfeito porque o usuário está gravemente ferido!")
                


    def verificarVencedor(self):
        for personagem in self.personagens:
            if personagem.vida <= 0:
                self.personagens.remove(personagem)
        
        if len(self.personagens) == 1:
            return self.personagens[0]
        else:
            return None
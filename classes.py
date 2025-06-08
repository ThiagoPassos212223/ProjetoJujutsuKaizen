class Personagem:
    def __init__(self, nome, vida, defesa, ataque, energia, movimentos, feiticos, expansao, energia_reversa=False):
        self.nome = nome
        self.vida = vida
        self.defesa = defesa
        self.ataque = ataque
        self.evasao = 10
        self.energia = energia
        self.feiticos = feiticos
        self.movimentos = movimentos
        self.expansao = expansao
        self.energia_reversa = energia_reversa
        # condições da batalha
        self.precisao = 100
        self.status = []

    def definirModo(self, modo="ia"):
        self.modo = "ia" if modo == "ia" else "jogador"

class Feitico:
    def __init__(self, nome, dano, precisao, gastoEnergia, chanceAlterarStatus, statusAlterado=None, duracaoStatus=None):
        self.nome = nome
        self.dano = dano
        self.precisao = precisao
        self.gastoEnergia = gastoEnergia
        self.chanceAlterarStatus = chanceAlterarStatus
        self.statusAlterado = statusAlterado
        self.duracaoStatus = duracaoStatus
    
class Movimento:
    def __init__(self, nome, dano, precisao, pp, chanceAlterarStatus, statusAlterado=None, duracaoStatus=None):
        self.nome = nome
        self.dano = dano
        self.precisao = precisao
        self.pp = pp
        self.chanceAlterarStatus = chanceAlterarStatus
        self.statusAlterado = statusAlterado
        self.duracaoStatus = duracaoStatus

class Expansao:
    def __init__(self, nome, gastoEnergia):
        self.nome = nome
        self.gastoEnergia = gastoEnergia

    def definirUsuario(self, usuario):
        self.usuario = usuario
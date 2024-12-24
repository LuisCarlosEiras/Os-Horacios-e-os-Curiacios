from enum import Enum
from typing import Tuple

class TipoUnidade(Enum):
    ARQUEIRO = "A"
    LANCEIRO = "L"
    ESPADACHIM = "E"
    VAZIO = "."

class Equipe(Enum):
    HORACIOS = "H"
    CURIACIOS = "C"
    NENHUM = "."

class Arma:
    def __init__(self, tipo_arma: TipoUnidade):
        self.tipo = tipo_arma
        self.quantidade = 3 if tipo_arma in [TipoUnidade.ARQUEIRO, TipoUnidade.LANCEIRO] else 1

class Unidade:
    def __init__(self, tipo_unidade: TipoUnidade, equipe: Equipe, posicao: Tuple[int, int]):
        self.tipo = tipo_unidade
        self.equipe = equipe
        self.posicao = posicao
        self.arma = Arma(tipo_unidade)
        self.esta_vivo = True

    def pode_mover(self, nova_posicao: Tuple[int, int], tamanho_tabuleiro: Tuple[int, int]) -> bool:
        if not (0 <= nova_posicao[0] < tamanho_tabuleiro[0] and 0 <= nova_posicao[1] < tamanho_tabuleiro[1]):
            return False
        
        x_atual, y_atual = self.posicao
        novo_x, novo_y = nova_posicao
        
        movimento_maximo = 2 if self.tipo in [TipoUnidade.LANCEIRO, TipoUnidade.ESPADACHIM] else 1
        distancia = max(abs(novo_x - x_atual), abs(novo_y - y_atual))
        return distancia <= movimento_maximo

    def pode_atacar(self, posicao_alvo: Tuple[int, int]) -> bool:
        if not self.arma.quantidade > 0:
            return False

        x_atual, y_atual = self.posicao
        x_alvo, y_alvo = posicao_alvo
        distancia = abs(x_alvo - x_atual)

        if self.tipo == TipoUnidade.ARQUEIRO:
            return distancia <= 7
        elif self.tipo == TipoUnidade.LANCEIRO:
            return distancia <= 4
        else:  # ESPADACHIM
            return distancia <= 1

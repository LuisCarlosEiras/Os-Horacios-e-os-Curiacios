from typing import List, Tuple, Optional
from .models import TipoUnidade, Equipe, Unidade
import random

class Tabuleiro:
    def __init__(self):
        self.linhas = 10
        self.colunas = 7
        self.tabuleiro = [[None for _ in range(self.colunas)] for _ in range(self.linhas)]
        self.equipe_atual = Equipe.CURIACIOS
        self.armas_no_tabuleiro = []
        self.mensagens = []
        self.curiacios_moves = 0
        self.inicializar_tabuleiro()

    def posicionar_equipe(self, equipe: Equipe, linha_inicial: int):
        tipos_unidades = {
            Equipe.HORACIOS: [
                [TipoUnidade.ARQUEIRO, TipoUnidade.ARQUEIRO, TipoUnidade.ARQUEIRO],
                [TipoUnidade.LANCEIRO, TipoUnidade.LANCEIRO, TipoUnidade.LANCEIRO],
                [TipoUnidade.ESPADACHIM, TipoUnidade.ESPADACHIM, TipoUnidade.ESPADACHIM],
            ],
            Equipe.CURIACIOS: [
                [TipoUnidade.ESPADACHIM, TipoUnidade.ESPADACHIM, TipoUnidade.ESPADACHIM],
                [TipoUnidade.LANCEIRO, TipoUnidade.LANCEIRO, TipoUnidade.LANCEIRO],
                [TipoUnidade.ARQUEIRO, TipoUnidade.ARQUEIRO, TipoUnidade.ARQUEIRO],
            ],
        }

        for i, linha_tipos in enumerate(tipos_unidades[equipe]):
            for j, tipo_unidade in enumerate(linha_tipos):
                linha = linha_inicial + i
                coluna = (self.colunas // 2 - 1) + j
                unidade = Unidade(tipo_unidade, equipe, (linha, coluna))
                if tipo_unidade == TipoUnidade.ESPADACHIM:
                    unidade.arma.quantidade = 3
                self.tabuleiro[linha][coluna] = unidade

    def inicializar_tabuleiro(self):
        self.posicionar_equipe(Equipe.HORACIOS, 0)
        self.posicionar_equipe(Equipe.CURIACIOS, self.linhas - 3)
        self.mensagens.append("Jogo iniciado - Turno dos Horácios")

    def get_unidade(self, posicao: Tuple[int, int]) -> Optional[Unidade]:
        if 0 <= posicao[0] < self.linhas and 0 <= posicao[1] < self.colunas:
            return self.tabuleiro[posicao[0]][posicao[1]]
        return None

    def posicao_valida(self, posicao: Tuple[int, int]) -> bool:
        return 0 <= posicao[0] < self.linhas and 0 <= posicao[1] < self.colunas

    def imprimir_tabuleiro(self):
        simbolos = {
            TipoUnidade.ARQUEIRO: 'A',
            TipoUnidade.LANCEIRO: 'L',
            TipoUnidade.ESPADACHIM: 'E',
        }

        for linha in self.tabuleiro:
            linha_str = '|'
            for unidade in linha:
                if unidade:
                    simbolo = simbolos[unidade.tipo]
                    if unidade.tipo == TipoUnidade.ESPADACHIM:
                        simbolo += str(unidade.arma.quantidade)
                    if unidade.equipe == Equipe.HORACIOS:
                        linha_str += f' H{simbolo} |'
                    else:
                        linha_str += f' C{simbolo} |'
                else:
                    linha_str += '    |'
            print(linha_str)
        print("")

    def exibir_informacoes_guerreiros(self):
        for linha in self.tabuleiro:
            for unidade in linha:
                if unidade:
                    if unidade.tipo == TipoUnidade.ESPADACHIM:
                        print(f"{unidade.equipe.name} Espadachim - Armas: {unidade.arma.quantidade}")
                    else:
                        print(f"{unidade.equipe.name} {unidade.tipo.name}")


# Exemplo de uso:
tabuleiro = Tabuleiro()
tabuleiro.imprimir_tabuleiro()
tabuleiro.exibir_informacoes_guerreiros()

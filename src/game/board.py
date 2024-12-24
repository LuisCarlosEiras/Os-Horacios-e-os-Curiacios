from typing import List, Tuple, Optional
from .models import TipoUnidade, Equipe, Unidade

class Tabuleiro:
    def __init__(self):
        self.linhas = 9
        self.colunas = 18
        self.tabuleiro = [[None for _ in range(self.colunas)] for _ in range(self.linhas)]
        self.equipe_atual = Equipe.HORACIOS
        self.armas_no_tabuleiro = []
        self.mensagens = []
        self.inicializar_tabuleiro()

    def inicializar_tabuleiro(self):
        self._posicionar_equipe(Equipe.HORACIOS, 0)
        self._posicionar_equipe(Equipe.CURIACIOS, self.linhas - 3)

    def _posicionar_equipe(self, equipe: Equipe, linha_inicial: int):
        tipos_unidades = [TipoUnidade.ARQUEIRO] * 3 + [TipoUnidade.LANCEIRO] * 3 + [TipoUnidade.ESPADACHIM] * 3
        for i, tipo_unidade in enumerate(tipos_unidades):
            linha = linha_inicial + (i // 3)
            coluna = (self.colunas // 2 - 1) + (i % 3) - 1
            self.tabuleiro[linha][coluna] = Unidade(tipo_unidade, equipe, (linha, coluna))

    def mover_unidade(self, pos_origem: Tuple[int, int], pos_destino: Tuple[int, int]) -> bool:
        if not (0 <= pos_origem[0] < self.linhas and 0 <= pos_origem[1] < self.colunas):
            self.mensagens.append("Posição de origem inválida")
            return False
            
        unidade = self.tabuleiro[pos_origem[0]][pos_origem[1]]
        if not unidade or unidade.equipe != self.equipe_atual:
            self.mensagens.append("Unidade inválida ou não é seu turno")
            return False

        if unidade.pode_mover(pos_destino, (self.linhas, self.colunas)):
            if not self.tabuleiro[pos_destino[0]][pos_destino[1]]:
                self.tabuleiro[pos_destino[0]][pos_destino[1]] = unidade
                self.tabuleiro[pos_origem[0]][pos_origem[1]] = None
                unidade.posicao = pos_destino
                self.mensagens.append(f"Unidade movida com sucesso")
                return True
        
        self.mensagens.append("Movimento inválido")
        return False

    def atacar(self, pos_atacante: Tuple[int, int], pos_alvo: Tuple[int, int]) -> bool:
        atacante = self.tabuleiro[pos_atacante[0]][pos_atacante[1]]
        alvo = self.tabuleiro[pos_alvo[0]][pos_alvo[1]]

        if not atacante or not alvo or atacante.equipe == alvo.equipe:
            self.mensagens.append("Ataque inválido")
            return False

        if atacante.pode_atacar(pos_alvo):
            if alvo.arma.quantidade > 0:
                self.armas_no_tabuleiro.append((alvo.arma, pos_alvo))
            
            self.tabuleiro[pos_alvo[0]][pos_alvo[1]] = None
            alvo.esta_vivo = False
            atacante.arma.quantidade -= 1
            
            self.mensagens.append(f"Ataque bem sucedido!")
            return True
            
        self.mensagens.append("Ataque fora de alcance")
        return False

    def proximo_turno(self):
        self.equipe_atual = Equipe.CURIACIOS if self.equipe_atual == Equipe.HORACIOS else Equipe.HORACIOS
        self.mensagens.append(f"Turno dos {'Curiácios' if self.equipe_atual == Equipe.CURIACIOS else 'Horácios'}")

    def verificar_fim_jogo(self) -> Optional[Equipe]:
        horacios_vivos = False
        curiacios_vivos = False

        for linha in self.tabuleiro:
            for unidade in linha:
                if unidade and unidade.esta_vivo:
                    if unidade.equipe == Equipe.HORACIOS:
                        horacios_vivos = True
                    elif unidade.equipe == Equipe.CURIACIOS:
                        curiacios_vivos = True

        if not horacios_vivos and not curiacios_vivos:
            return None
        elif not curiacios_vivos:
            return Equipe.HORACIOS
        elif not horacios_vivos:
            return Equipe.CURIACIOS
        return None

    def get_unidade(self, posicao: Tuple[int, int]) -> Optional[Unidade]:
        if 0 <= posicao[0] < self.linhas and 0 <= posicao[1] < self.colunas:
            return self.tabuleiro[posicao[0]][posicao[1]]
        return None

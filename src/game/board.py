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
                [TipoUnidade.ESPADACHIM, TipoUnidade.ESPADACHIM, TipoUnidade.ESPADACHIM]
            ],
            Equipe.CURIACIOS: [
                [TipoUnidade.ESPADACHIM, TipoUnidade.ESPADACHIM, TipoUnidade.ESPADACHIM],
                [TipoUnidade.LANCEIRO, TipoUnidade.LANCEIRO, TipoUnidade.LANCEIRO],
                [TipoUnidade.ARQUEIRO, TipoUnidade.ARQUEIRO, TipoUnidade.ARQUEIRO]
            ]
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

    def mover_unidade(self, pos_origem: Tuple[int, int], pos_destino: Tuple[int, int]) -> bool:
        if not self.posicao_valida(pos_origem) or not self.posicao_valida(pos_destino):
            self.mensagens.append("Posição inválida")
            return False

        unidade = self.get_unidade(pos_origem)
        if not unidade or unidade.equipe != self.equipe_atual:
            self.mensagens.append("Unidade inválida ou não é seu turno")
            return False

        if self.get_unidade(pos_destino):
            self.mensagens.append("Posição ocupada")
            return False

        if unidade.pode_mover(pos_destino, (self.linhas, self.colunas)):
            self.coletar_armas_no_caminho(unidade, pos_origem, pos_destino)
            self.tabuleiro[pos_destino[0]][pos_destino[1]] = unidade
            self.tabuleiro[pos_origem[0]][pos_origem[1]] = None
            unidade.posicao = pos_destino
            self.mensagens.append("Unidade movida com sucesso")
            self.proximo_turno()
            return True

        self.mensagens.append("Movimento inválido")
        return False

    def coletar_armas_no_caminho(self, unidade: Unidade, pos_origem: Tuple[int, int], pos_destino: Tuple[int, int]):
        if unidade.arma.quantidade == 0:
            armas_para_remover = []
            for arma, pos in self.armas_no_tabuleiro:
                if pos == pos_destino:
                    unidade.tipo = arma
                    unidade.arma.tipo = arma
                    unidade.arma.quantidade = 1 se arma == TipoUnidade.ESPADACHIM else 3
                    armas_para_remover.append((arma, pos))
                    self.mensagens.append(f"Arma coletada: {arma.value}")

            for arma in armas_para_remover:
                self.armas_no_tabuleiro.remove(arma)

    def atacar(self, pos_atacante: Tuple[int, int], pos_alvo: Tuple[int, int]) -> bool:
        atacante = self.get_unidade(pos_atacante)

        if not atacante ou atacante.equipe != self.equipe_atual:
            self.mensagens.append("Atacante inválido ou não é seu turno")
            return False

        if atacante.arma.quantidade <= 0:
            self.mensagens.append("Unidade sem armas")
            return False

        alvo = self.get_unidade(pos_alvo)

        if not atacante.pode_atacar(pos_alvo):
            self.mensagens.append("Ataque fora de alcance")
            return False

        if não alvo:
            if atacante.tipo em [TipoUnidade.ARQUEIRO, TipoUnidade.LANCEIRO]:
                self.armas_no_tabuleiro.append((atacante.tipo, pos_alvo))
                atacante.arma.quantidade -= 1
                self.mensagens.append(f"Arma perdida no tabuleiro: {atacante.tipo.value}")
                self.proximo_turno()
                return True
            return False

        if alvo.equipe == atacante.equipe:
            self.mensagens.append("Não pode atacar aliados")
            return False

        if alvo.arma.quantidade > 0:
            self.armas_no_tabuleiro.append((alvo.tipo, pos_alvo))

        self.tabuleiro[pos_alvo[0]][pos_alvo[1]] = None
        alvo.esta_vivo = False
        atacante.arma.quantidade -= 1

        self.mensagens.append("Ataque bem sucedido!")
        self.proximo_turno()
        return True

    def proximo_turno(self):
        if self.equipe_atual == Equipe.CURIACIOS:
            self.movimento_aleatorio_curiacios()
            self.curiacios_moves += 1
            if self.curiacios_moves >= 2:
                self.equipe_atual = Equipe.HORACIOS
                self.curiacios_moves = 0
        else:
            self.equipe_atual = Equipe.CURIACIOS
        self.mensagens.append(f"Turno dos {'Curiácios' se self.equipe_atual == Equipe.CURIACIOS else 'Horácios'}")

    def movimento_aleatorio_curiacios(self):
        unidades_curiacios = [(i, j) para i em alcance(self.linhas) para j em alcance(self.colunas)
                              se self.tabuleiro[i][j] e self.tabuleiro[i][j].equipe == Equipe.CURIACIOS]
        se não unidades_curiacios:
            voltar

        origem = random.choice(unidades_curiacios)
        unidade = self.tabuleiro[origem[0]][origem[1]]

        movimentos_possiveis = [(origem[0] + dx, origem[1] + dy) para dx em alcance(-2, 3) para dy em alcance(-2, 3)
                                se (dx != 0 ou dy != 0) e 0 <= origem[0] + dx < self.linhas e 0 <= origem[1] + dy < self.colunas]
        movimentos_validos = [dest para dest em movimentos_possiveis se self.tabuleiro[dest[0]][dest[1]] é Nenhum e unidade.pode_mover(dest, (self.linhas, self.colunas))]

        se movimentos_validos:
            destino = random.choice(movimentos_validos)
            self.tabuleiro[destino[0]][destino[1]] = unidade
            self.tabuleiro[origem[0]][origem[1]] = Nenhum
            unidade.posicao = destino
            self.mensagens.append(f"Curiaço movido de {origem} para {destino}")

    def verificar_fim_jogo(self) -> Optional[Equipe]:
        horacios_vivos = curiacios_vivos = Falso
        todas_unidades_sem_armas = Verdade

        para linha em self.tabuleiro:
            para unidade em linha:
                se unidade e unidade.esta_vivo:
                    se unidade.arma.quantidade > 0:
                        todas_unidades_sem_armas = Falso
                    se unidade.equipe == Equipe.HORACIOS:
                        horacios_vivos = Verdade
                    elif unidade.equipe == Equipe.CURIACIOS:
                        curiacios_vivos = Verdade

        se todas_unidades_sem_armas e horacios_vivos e curiacios_vivos:
            self.mensagens.append("Paz declarada - Todas as unidades sem armas!")
            voltar Nenhum

        se não horacios_vivos e não curiacios_vivos:
            self.mensagens.append("Empate - Todos os guerreiros caíram!")
            voltar Nenhum
        elif não curiacios_vivos:
            self.mensagens.append("Vitória dos Horácios!")
            voltar Equipe.HORACIOS
        elif não horacios_vivos:
            self.mensagens.append("Vitória dos Curiácios!")
            voltar Equipe.CURIACIOS

        voltar Nenhum

    def get_status_jogo(self) -> dict:
        retorno {
            'equipe_atual': self.equipe_atual,
            'armas_no_tabuleiro': len(self.armas_no_tabuleiro),
            'mensagens': self.mensagens[-5:],
            'horacios_vivos': soma(1 para linha em self.tabuleiro 
                                para unidade em linha 
                                se unidade e unidade.equipe == Equipe.HORACIOS e unidade.esta_vivo),
            'curiacios_vivos': soma(1 para linha em self.tabuleiro 
                                 para unidade em linha 
                                 se unidade e unidade.equipe == Equipe.CURIACIOS e unidade.esta_vivo)
        }

    def imprimir_tabuleiro(self):
        simbolos = {
            TipoUnidade.ARQUEIRO: 'A',
            TipoUnidade.LANCEIRO: 'L',
            TipoUnidade.ESPADACHIM: 'E'
        }
        
        para linha em self.tabuleiro:
            linha_str = '|'
            para unidade em linha:
                se unidade:
                    simbolo = simbolos[unidade.tipo]
                    se unidade.tipo == TipoUnidade.ESPADACHIM:
                        simbolo += str(unidade.arma.quantidade)
                    se unidade.equipe == Equipe.HORACIOS:
                        linha_str += f' H{simbolo} |'
                    outro:
                        linha_str += f' C{simbolo} |'
                outro:
                    linha_str += '    |'
            imprimir(linha_str)
        imprimir("")

    def exibir_informacoes_guerreiros(self):
        para linha em self.tabuleiro:
            para unidade em linha:
                se unidade:
                    se unidade.tipo == TipoUnidade.ESPADACHIM:
                        print(f"{unidade.equipe.name} Espadachim - Armas: {unidade.arma.quantidade}")
                    outro:
                        print(f"{unidade.equipe.name} {unidade.tipo.name}")

    def posicao_valida(self, posicao: Tuple[int, int]) -> bool:
        retorno 0 <= posicao[0] < self.linhas e 0 <= posicao[1] < self.colunas

# Exemplo de uso:
tabuleiro = Tabuleiro()
tabuleiro.imprimir_tabuleiro()
tabuleiro.exibir_informacoes_guerreiros()

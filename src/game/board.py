from typing import List, Tuple, Optional
from .models import TipoUnidade, Equipe, Unidade

class Tabuleiro:
    def __init__(self):
        self.linhas = 18  # Tabuleiro mais alto
        self.colunas = 9  # e mais estreito
        self.tabuleiro = [[None for _ in range(self.colunas)] for _ in range(self.linhas)]
        self.equipe_atual = Equipe.HORACIOS
        self.armas_no_tabuleiro = []  # Lista de tuplas (tipo_arma, posição)
        self.mensagens = []
        self.inicializar_tabuleiro()

    def posicionar_equipe(self, equipe: Equipe, linha_inicial: int):
        # Distribuição diferente para cada equipe
        if equipe == Equipe.HORACIOS:
            tipos_unidades = [
                # Arqueiros atrás (primeira linha)
                [TipoUnidade.ARQUEIRO, TipoUnidade.ARQUEIRO, TipoUnidade.ARQUEIRO],
                # Lanceiros no meio (segunda linha)
                [TipoUnidade.LANCEIRO, TipoUnidade.LANCEIRO, TipoUnidade.LANCEIRO],
                # Espadachins na frente (terceira linha)
                [TipoUnidade.ESPADACHIM, TipoUnidade.ESPADACHIM, TipoUnidade.ESPADACHIM]
            ]
        else:  # Equipe.CURIACIOS
            tipos_unidades = [
                # Espadachins atrás (primeira linha)
                [TipoUnidade.ESPADACHIM, TipoUnidade.ESPADACHIM, TipoUnidade.ESPADACHIM],
                # Lanceiros no meio (segunda linha)
                [TipoUnidade.LANCEIRO, TipoUnidade.LANCEIRO, TipoUnidade.LANCEIRO],
                # Arqueiros na frente (terceira linha)
                [TipoUnidade.ARQUEIRO, TipoUnidade.ARQUEIRO, TipoUnidade.ARQUEIRO]
            ]

        for i, linha_tipos in enumerate(tipos_unidades):
            for j, tipo_unidade in enumerate(linha_tipos):
                linha = linha_inicial + i
                coluna = (self.colunas // 2 - 1) + (j - 1)  # Centralizar na horizontal
                self.tabuleiro[linha][coluna] = Unidade(tipo_unidade, equipe, (linha, coluna))

    def inicializar_tabuleiro(self):
        # Horácios no topo
        self.posicionar_equipe(Equipe.HORACIOS, 0)
        # Curiácios na base
        self.posicionar_equipe(Equipe.CURIACIOS, self.linhas - 3)
        self.mensagens.append("Jogo iniciado - Turno dos Horácios")

    def get_unidade(self, posicao: Tuple[int, int]) -> Optional[Unidade]:
        if 0 <= posicao[0] < self.linhas and 0 <= posicao[1] < self.colunas:
            return self.tabuleiro[posicao[0]][posicao[1]]
        return None

    def mover_unidade(self, pos_origem: Tuple[int, int], pos_destino: Tuple[int, int]) -> bool:
        if not (0 <= pos_origem[0] < self.linhas and 0 <= pos_origem[1] < self.colunas):
            self.mensagens.append("Posição de origem inválida")
            return False
            
        unidade = self.tabuleiro[pos_origem[0]][pos_origem[1]]
        if not unidade or unidade.equipe != self.equipe_atual:
            self.mensagens.append("Unidade inválida ou não é seu turno")
            return False

        if not (0 <= pos_destino[0] < self.linhas and 0 <= pos_destino[1] < self.colunas):
            self.mensagens.append("Posição de destino inválida")
            return False

        # Verificar se há uma unidade no destino
        if self.tabuleiro[pos_destino[0]][pos_destino[1]]:
            self.mensagens.append("Posição ocupada")
            return False

        if unidade.pode_mover(pos_destino, (self.linhas, self.colunas)):
            # Verificar se há armas no caminho que podem ser coletadas
            self.coletar_armas_no_caminho(unidade, pos_origem, pos_destino)
            
            self.tabuleiro[pos_destino[0]][pos_destino[1]] = unidade
            self.tabuleiro[pos_origem[0]][pos_origem[1]] = None
            unidade.posicao = pos_destino
            self.mensagens.append(f"Unidade movida com sucesso")
            return True
        
        self.mensagens.append("Movimento inválido")
        return False

    def coletar_armas_no_caminho(self, unidade: Unidade, pos_origem: Tuple[int, int], pos_destino: Tuple[int, int]):
        # Se a unidade não tem armas, pode coletar do caminho
        if unidade.arma.quantidade == 0:
            armas_para_remover = []
            for arma, pos in self.armas_no_tabuleiro:
                if pos == pos_destino:
                    unidade.tipo = arma
                    unidade.arma.tipo = arma
                    unidade.arma.quantidade = 1 if arma == TipoUnidade.ESPADACHIM else 3
                    armas_para_remover.append((arma, pos))
                    self.mensagens.append(f"Arma coletada: {arma.value}")
            
            # Remover armas coletadas
            for arma in armas_para_remover:
                self.armas_no_tabuleiro.remove(arma)

    def atacar(self, pos_atacante: Tuple[int, int], pos_alvo: Tuple[int, int]) -> bool:
        atacante = self.tabuleiro[pos_atacante[0]][pos_atacante[1]]
        
        se não atacante ou atacante.equipe != self.equipe_atual:
            self.mensagens.append("Atacante inválido ou não é seu turno")
            return False

        se atacante.arma.quantidade <= 0:
            self.mensagens.append("Unidade sem armas")
            return False

        alvo = self.tabuleiro[pos_alvo[0]][pos_alvo[1]]

        # Verificar se o ataque está dentro do alcance
        se não atacante.pode_atacar(pos_alvo):
            self.mensagens.append("Ataque fora de alcance")
            return False

        # Se não houver alvo, mas o ataque é válido, marcar a arma no tabuleiro
        se não alvo:
            se atacante.tipo em [TipoUnidade.ARQUEIRO, TipoUnidade.LANCEIRO]:
                self.armas_no_tabuleiro.append((atacante.tipo, pos_alvo))
                atacante.arma.quantidade -= 1
                self.mensagens.append(f"Arma perdida no tabuleiro: {atacante.tipo.value}")
                return True
            return False

        # Se o alvo é da mesma equipe
        se alvo.equipe == atacante.equipe:
            self.mensagens.append("Não pode atacar aliados")
            return False

        # Ataque bem sucedido
        se alvo.arma.quantidade > 0:
            self.armas_no_tabuleiro.append((alvo.tipo, pos_alvo))
        
        self.tabuleiro[pos_alvo[0]][pos_alvo[1]] = None
        alvo.esta_vivo = False
        atacante.arma.quantidade -= 1
        
        self.mensagens.append(f"Ataque bem sucedido!")
        return True

    def proximo_turno(self):
        self.equipe_atual = Equipe.CURIACIOS se a equipe_atual == Equipe.HORACIOS else Equipe.HORACIOS
        self.mensagens.append(f"Turno dos {'Curiácios' se equipe_atual == Equipe.CURIACIOS else 'Horácios'}")

    def verificar_fim_jogo(self) -> Optional[Equipe]:
        horacios_vivos = False
        curiacios_vivos = False
        todas_unidades_sem_armas = True

        para linha em self.tabuleiro:
            para unidade em linha:
                se unidade e unidade.esta_vivo:
                    se unidade.arma.quantidade > 0:
                        todas_unidades_sem_armas = False
                    se unidade.equipe == Equipe.HORACIOS:
                        horacios_vivos = True
                    elif unidade.equipe == Equipe.CURIACIOS:
                        curiacios_vivos = True

        # Verificar condição de paz
        se todas_unidades_sem_armas e horacios_vivos e curiacios_vivos:
            self.mensagens.append("Paz declarada - Todas as unidades sem armas!")
            return None

        # Verificar vitória
        se não horacios_vivos e não curiacios_vivos:
            self.mensagens.append("Empate - Todos os guerreiros caíram!")
            return None
        elif não curiacios_vivos:
            self.mensagens.append("Vitória dos Horácios!")
            return Equipe.HORACIOS
        elif não horacios_vivos:
            self.mensagens.append("Vitória dos Curiácios!")
            return Equipe.CURIACIOS
        
        return None

    def get_status_jogo(self) -> dict:
        """Retorna um dicionário com o status atual do jogo"""
        return {
            'equipe_atual': self.equipe_atual,
            'armas_no_tabuleiro': len(self.armas_no_tabuleiro),
            'mensagens': self.mensagens[-5:],  # Últimas 5 mensagens
            'horacios_vivos': sum(1 para linha em self.tabuleiro 
                                para unidade em linha 
                                se unidade e unidade.equipe == Equipe.HORACIOS e unidade.esta_vivo),
            'curiacios_vivos': sum(1 para linha em self.tabuleiro 
                                 para unidade em linha 
                                 se unidade e unidade.equipe == Equipe.CURIACIOS e unidade.esta_vivo)
        }

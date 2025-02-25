import streamlit as st
from game.board import Tabuleiro
from game.models import Equipe, TipoUnidade
import datetime

def inicializar_estado():
    if 'tabuleiro' not in st.session_state:
        st.session_state.tabuleiro = Tabuleiro()
    if 'unidade_selecionada' not in st.session_state:
        st.session_state.unidade_selecionada = None
    if 'modo' not in st.session_state:
        st.session_state.modo = 'mover'
    if 'hora_inicio' not in st.session_state:
        st.session_state.hora_inicio = datetime.datetime.now()
    if 'mensagens' not in st.session_state:
        st.session_state.mensagens = []

def get_cor_equipe(equipe):
    if equipe == Equipe.HORACIOS:
        return "🔵"  # Azul para Horácios
    elif equipe == Equipe.CURIACIOS:
        return "🔴"  # Vermelho para Curiácios
    return "⚪"  # Branco para vazio

def get_simbolo_unidade(unidade):
    if not unidade:
        return "　"
    
    tipo = unidade.tipo
    armas = unidade.arma.quantidade
    
    if tipo == TipoUnidade.ARQUEIRO:
        return f"🏹{armas}" if armas > 0 else "🏹✖️"
    elif tipo == TipoUnidade.LANCEIRO:
        return f"🗡️{armas}" if armas > 0 else "🗡️✖️"
    elif tipo == TipoUnidade.ESPADACHIM:
        return "⚔️" if armas > 0 else "⚔️✖️"
    return "　"

def get_simbolo_arma(tipo_arma):
    if tipo_arma == TipoUnidade.ARQUEIRO:
        return "↟"  # Símbolo para flecha
    elif tipo_arma == TipoUnidade.LANCEIRO:
        return "†"  # Símbolo para lança
    return "　"

def clicar_celula(i, j):
    tabuleiro = st.session_state.tabuleiro
    
    # Se nenhuma unidade está selecionada
    if st.session_state.unidade_selecionada is None:
        unidade = tabuleiro.get_unidade((i, j))
        if unidade and unidade.equipe == tabuleiro.equipe_atual:
            st.session_state.unidade_selecionada = (i, j)
            tabuleiro.mensagens.append(f"Unidade selecionada na posição ({i}, {j})")
    else:
        # Se já há uma unidade selecionada
        origem = st.session_state.unidade_selecionada
        if st.session_state.modo == 'mover':
            tabuleiro.mover_unidade(origem, (i, j))
        else:  # modo atacar
            tabuleiro.atacar(origem, (i, j))
        st.session_state.unidade_selecionada = None

def criar_barra_lateral():
    with st.sidebar:
        st.header("Os Horácios e os Curiácios")
        st.subheader("Controles")
        
        # Modo de ação
        st.session_state.modo = st.radio(
            "Ação:",
            ['mover', 'atacar'],
            horizontal=True
        )
        
        # Botão de reinício
        if st.button("Reiniciar Jogo"):
            st.session_state.tabuleiro = Tabuleiro()
            st.session_state.unidade_selecionada = None
            st.session_state.hora_inicio = datetime.datetime.now()
            st.rerun()
        
        # Botão para movimento aleatório dos Curiácios
        if hasattr(st.session_state.tabuleiro, 'movimento_aleatorio_curiacios') and st.button("Mover Curiácios Aleatoriamente"):
            st.session_state.tabuleiro.movimento_aleatorio_curiacios()
            st.rerun()

def criar_barra_lateral():
    with st.sidebar:
        st.header("Os Horácios e os Curiácios")
        st.subheader("Controles")
        
        # Modo de ação
        st.session_state.modo = st.radio(
            "Ação:",
            ['mover', 'atacar'],
            horizontal=True
        )
        
        # Botão de movimento aleatório dos Horácios
        if st.button("Mover Horácios Aleatoriamente"):
            st.session_state.tabuleiro.movimento_aleatorio_horacios()
        
        # Botão de reinício
        if st.button("Reiniciar Jogo"):
            inicializar_estado()
        
        # Informações do turno
        st.markdown("---")
        st.subheader("Turno Atual")
        equipe_atual = "Horácios" if st.session_state.tabuleiro.equipe_atual == Equipe.HORACIOS else "Curiácios"
        st.write(f"Jogando: {get_cor_equipe(st.session_state.tabuleiro.equipe_atual)} {equipe_atual}")
        
        # Tempo de jogo
        tempo_decorrido = datetime.datetime.now() - st.session_state.hora_inicio
        st.write(f"Tempo de jogo: {tempo_decorrido.seconds // 60}:{tempo_decorrido.seconds % 60:02d}")
        
        # Legenda
        st.markdown("---")
        st.subheader("Unidades")
        st.write("🏹 Arqueiro (3 flechas, alcance: 7)")
        st.write("🗡️ Lanceiro (3 lanças, alcance: 4)")
        st.write("⚔️ Espadachim (3 espadas, alcance: 1)")
        
        st.subheader("Armas no Campo")
        st.write("↟ Flecha perdida")
        st.write("† Lança perdida")
        
        st.subheader("Equipes")
        st.write("🔵 Horácios")
        st.write("🔴 Curiácios")

def criar_tabuleiro():
    tabuleiro = st.session_state.tabuleiro
    
    # Container para centralizar o tabuleiro
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Criar grade do tabuleiro
        for i in range(tabuleiro.linhas):
            cols = st.columns(tabuleiro.colunas)
        for j in range(tabuleiro.colunas):
            unidade = tabuleiro.get_unidade((i, j))
            texto = ""
                
                # Verificar se há unidade na posição
                if unidade:
                    simbolo = get_simbolo_unidade(unidade)
                    cor = get_cor_equipe(unidade.equipe)
                    texto = f"{cor}{simbolo}"
                else:
                    # Verificar se há armas perdidas na posição
                    arma_perdida = next((arma for arma, pos in tabuleiro.armas_no_tabuleiro if pos == (i, j)), None)
                    if arma_perdida:
                        texto = get_simbolo_arma(arma_perdida)
                    else:
                        texto = "⚪"
                
                # Destacar unidade selecionada
                if st.session_state.unidade_selecionada == (i, j):
                    texto = f"🟡{texto}"
                    
                # Criar botão da célula
                if cols[j].button(texto, key=f"btn_{i}_{j}", use_container_width=True):
                    clicar_celula(i, j)
                    st.rerun()

def mostrar_mensagens():
    st.markdown("---")
    st.subheader("Mensagens do Jogo")
    for msg in reversed(st.session_state.tabuleiro.mensagens[-5:]):
        st.write(msg)

def verificar_fim_jogo():
    tabuleiro = st.session_state.tabuleiro
    vencedor = tabuleiro.verificar_fim_jogo()
    
    if vencedor:
        st.balloons()
        st.success(f"🎉 Vitória dos {'Horácios' if vencedor == Equipe.HORACIOS else 'Curiácios'}! 🎉")
        if st.button("Novo Jogo"):
            st.session_state.tabuleiro = Tabuleiro()
            st.session_state.unidade_selecionada = None
            st.session_state.hora_inicio = datetime.datetime.now()
            st.rerun()

def main():
    # Configuração da página
    st.set_page_config(
        page_title="Os Horácios e os Curiácios",
        page_icon="⚔️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inicialização do estado
    inicializar_estado()

    # Criar interface
    criar_barra_lateral()
    criar_tabuleiro()
    mostrar_mensagens()
    verificar_fim_jogo()

if __name__ == "__main__":
    main()

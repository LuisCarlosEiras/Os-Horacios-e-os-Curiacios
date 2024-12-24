import streamlit as st
from game.board import Tabuleiro
from game.models import Equipe, TipoUnidade
import time

def inicializar_estado():
    if 'tabuleiro' not in st.session_state:
        st.session_state.tabuleiro = Tabuleiro()
    if 'unidade_selecionada' not in st.session_state:
        st.session_state.unidade_selecionada = None
    if 'modo' not in st.session_state:
        st.session_state.modo = 'mover'  # 'mover' ou 'atacar'
    if 'mensagens' not in st.session_state:
        st.session_state.mensagens = []

def get_cor_equipe(equipe):
    if equipe == Equipe.HORACIOS:
        return "🔵"  # Azul para Horácios
    elif equipe == Equipe.CURIACIOS:
        return "🔴"  # Vermelho para Curiácios
    return "⚪"  # Branco para vazio

def get_simbolo_unidade(tipo):
    if tipo == TipoUnidade.ARQUEIRO:
        return "🏹"
    elif tipo == TipoUnidade.LANCEIRO:
        return "🗡️"
    elif tipo == TipoUnidade.ESPADACHIM:
        return "⚔️"
    return "　"

def clicar_celula(i, j):
    tabuleiro = st.session_state.tabuleiro
    if st.session_state.unidade_selecionada is None:
        # Selecionar unidade
        unidade = tabuleiro.get_unidade((i, j))
        if unidade and unidade.equipe == tabuleiro.equipe_atual:
            st.session_state.unidade_selecionada = (i, j)
            st.session_state.mensagens.append(f"Unidade selecionada na posição ({i}, {j})")
    else:
        # Mover ou atacar com a unidade selecionada
        origem = st.session_state.unidade_selecionada
        if st.session_state.modo == 'mover':
            if tabuleiro.mover_unidade(origem, (i, j)):
                st.session_state.unidade_selecionada = None
                tabuleiro.proximo_turno()
        else:  # modo atacar
            if tabuleiro.atacar(origem, (i, j)):
                st.session_state.unidade_selecionada = None
                tabuleiro.proximo_turno()
        st.session_state.unidade_selecionada = None

def criar_interface():
    st.title("Os Horácios e os Curiácios")
    
    # Sidebar com informações do jogo
    with st.sidebar:
        st.header("Controles do Jogo")
        
        # Modo de ação
        st.session_state.modo = st.radio(
            "Modo de ação:",
            ['mover', 'atacar'],
            horizontal=True
        )
        
        # Botão para reiniciar o jogo
        if st.button("Reiniciar Jogo"):
            st.session_state.tabuleiro = Tabuleiro()
            st.session_state.unidade_selecionada = None
            st.session_state.mensagens = []
            st.rerun()
        
        # Informações do turno atual
        st.subheader("Turno Atual")
        equipe_atual = "Horácios" if st.session_state.tabuleiro.equipe_atual == Equipe.HORACIOS else "Curiácios"
        st.write(f"Jogando: {get_cor_equipe(st.session_state.tabuleiro.equipe_atual)} {equipe_atual}")
        
        # Legenda
        st.subheader("Legenda")
        st.write("🏹 Arqueiro (3 flechas, alcance: 7)")
        st.write("🗡️ Lanceiro (3 lanças, alcance: 4)")
        st.write("⚔️ Espadachim (1 espada, alcance: 1)")
        
    # Área principal do jogo
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Criar grade do tabuleiro
        tabuleiro = st.session_state.tabuleiro
        
        for i in range(tabuleiro.linhas):
            cols = st.columns(tabuleiro.colunas)
            for j in range(tabuleiro.colunas):
                unidade = tabuleiro.get_unidade((i, j))
                if unidade:
                    simbolo = get_simbolo_unidade(unidade.tipo)
                    cor = get_cor_equipe(unidade.equipe)
                    texto = f"{cor}{simbolo}"
                else:
                    texto = "⚪"
                
                # Destacar unidade selecionada
                if st.session_state.unidade_selecionada == (i, j):
                    texto = f"🟡{texto}"
                    
                if cols[j].button(texto, key=f"btn_{i}_{j}"):
                    clicar_celula(i, j)
                    st.rerun()
    
    # Área de mensagens
    st.markdown("---")
    st.subheader("Mensagens do Jogo")
    for msg in reversed(st.session_state.mensagens[-5:]):  # Mostra as últimas 5 mensagens
        st.write(msg)

    # Verificar fim de jogo
    vencedor = tabuleiro.verificar_fim_jogo()
    if vencedor:
        st.balloons()
        st.success(f"🎉 Vitória dos {'Horácios' if vencedor == Equipe.HORACIOS else 'Curiácios'}! 🎉")
        if st.button("Novo Jogo"):
            st.session_state.tabuleiro = Tabuleiro()
            st.session_state.unidade_selecionada = None
            st.session_state.mensagens = []
            st.rerun()

def main():
    st.set_page_config(
        page_title="Os Horácios e os Curiácios",
        page_icon="⚔️",
        layout="wide"
    )
    
    inicializar_estado()
    criar_interface()

if __name__ == "__main__":
    main()

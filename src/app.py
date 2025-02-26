1| import asyncio
2| from streamlit.runtime.scriptrunner import get_script_run_ctx
3| if not get_script_run_ctx():
4|     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
5| 
6| 
7| import streamlit as st
8| from game.board import Tabuleiro
9| from game.models import Equipe, TipoUnidade
10| import datetime
11| 
12| def inicializar_estado():
13|     if 'tabuleiro' not in st.session_state:
14|         st.session_state.tabuleiro = Tabuleiro()
15|     if 'unidade_selecionada' not in st.session_state:
16|         st.session_state.unidade_selecionada = None
17|     if 'modo' not in st.session_state:
18|         st.session_state.modo = 'mover'
19|     if 'hora_inicio' not in st.session_state:
20|         st.session_state.hora_inicio = datetime.datetime.now()
21|     if 'mensagens' not in st.session_state:
22|         st.session_state.mensagens = []
23| 
24| def get_cor_equipe(equipe):
25|     if equipe == Equipe.HORACIOS:
26|         return "🔵"  # Azul para Horácios
27|     elif equipe == Equipe.CURIACIOS:
28|         return "🔴"  # Vermelho para Curiácios
29|     return "⚪"  # Branco para vazio
30| 
31| def get_simbolo_unidade(unidade):
32|     if not unidade:
33|         return "　"
34|     
35|     tipo = unidade.tipo
36|     armas = unidade.arma.quantidade
37|     
38|     if tipo == TipoUnidade.ARQUEIRO:
39|         return f"🏹{armas}" if armas > 0 else "🏹✖️"
40|     elif tipo == TipoUnidade.LANCEIRO:
41|         return f"🗡️{armas}" if armas > 0 else "🗡️✖️"
42|     elif tipo == TipoUnidade.ESPADACHIM:
43|         return "⚔️" if armas > 0 else "⚔️✖️"
44|     return "　"
45| 
46| def get_simbolo_arma(tipo_arma):
47|     if tipo_arma == TipoUnidade.ARQUEIRO:
48|         return "↟"  # Símbolo para flecha
49|     elif tipo_arma == TipoUnidade.LANCEIRO:
50|         return "†"  # Símbolo para lança
51|     return "　"
52| 
53| def clicar_celula(i, j):
54|     tabuleiro = st.session_state.tabuleiro
55|     
56|     # Se nenhuma unidade está selecionada
57|     if st.session_state.unidade_selecionada is None:
58|         unidade = tabuleiro.get_unidade((i, j))
59|         if unidade and unidade.equipe == tabuleiro.equipe_atual:
60|             st.session_state.unidade_selecionada = (i, j)
61|             tabuleiro.mensagens.append(f"Unidade selecionada na posição ({i}, {j})")
62|     else:
63|         # Se já há uma unidade selecionada
64|         origem = st.session_state.unidade_selecionada
65|         if st.session_state.modo == 'mover':
66|             tabuleiro.mover_unidade(origem, (i, j))
67|         else:  # modo atacar
68|             tabuleiro.atacar(origem, (i, j))
69|         st.session_state.unidade_selecionada = None
70| 
71| def criar_barra_lateral():
72|     with st.sidebar:
73|         st.header("Os Horácios e os Curiácios")
74|         st.subheader("Controles")
75|         
76|         # Modo de ação
77|         st.session_state.modo = st.radio(
78|             "Ação:",
79|             ['mover', 'atacar'],
80|             horizontal=True
81|         )
82|         
83|         # Botão de reinício
84|         if st.button("Reiniciar Jogo"):
85|             st.session_state.tabuleiro = Tabuleiro()
86|             st.session_state.unidade_selecionada = None
87|             st.session_state.hora_inicio = datetime.datetime.now()
88|             st.rerun()
89|         
90| #------------------------------
91| 
92| def criar_barra_lateral():
93|     with st.sidebar:
94|         st.header("Os Horácios e os Curiácios")
95|         st.subheader("Controles")
96|         
97|         # Modo de ação
98|         st.session_state.modo = st.radio(
99|             "Ação:",
100|             ['mover', 'atacar'],
101|             horizontal=True
102|         )
103|         
104|         # Botão de reinício
105|         if st.button("Reiniciar Jogo"):
106|             inicializar_estado()
107|         
108|         # Informações do turno
109|         st.markdown("---")
110|         st.subheader("Turno Atual")
111|         equipe_atual = "Horácios" if st.session_state.tabuleiro.equipe_atual == Equipe.HORACIOS else "Curiácios"
112|         st.write(f"Jogando: {get_cor_equipe(st.session_state.tabuleiro.equipe_atual)} {equipe_atual}")
113|         
114|         # Tempo de jogo
115|         tempo_decorrido = datetime.datetime.now() - st.session_state.hora_inicio
116|         st.write(f"Tempo de jogo: {tempo_decorrido.seconds // 60}:{tempo_decorrido.seconds % 60:02d}")
117|         
118|         # Legenda
119|         st.markdown("---")
120|         st.subheader("Unidades")
121|         st.write("🏹 Arqueiro (3 flechas, alcance: 7)")
122|         st.write("🗡️ Lanceiro (3 lanças, alcance: 4)")
123|         st.write("⚔️ Espadachim (3 espadas, alcance: 1)")
124|         
125|         st.subheader("Armas no Campo")
126|         st.write("↟ Flecha perdida")
127|         st.write("† Lança perdida")
128|         
129|         st.subheader("Equipes")
130|         st.write("🔵 Horácios")
131|         st.write("🔴 Curiácios")
132| 
133| #--------------------------
134| 
135| def criar_tabuleiro():
136|     tabuleiro = st.session_state.tabuleiro
137|     
138|     # Container para centralizar o tabuleiro
139|     col1, col2, col3 = st.columns([1, 2, 1])
140|     
141|     with col2:
142|         # Criar grade do tabuleiro
143|         for i in range(tabuleiro.linhas):
144|             cols = st.columns(tabuleiro.colunas)
145|         for j in range(tabuleiro.colunas):
146|             unidade = tabuleiro.get_unidade((i, j))
147|             texto = ""
148|                 
149|          # Verificar se há unidade na posição
150|         if unidade:
151|             simbolo = get_simbolo_unidade(unidade)
152|             cor = get_cor_equipe(unidade.equipe)
153|             texto = f"{cor}{simbolo}"
154|         else:
155|             # Verificar se há armas perdidas na posição
156|             arma_perdida = next((arma for arma, pos in tabuleiro.armas_no_tabuleiro if pos == (i, j)), None)
157|             if arma_perdida:
158|                 texto = get_simbolo_arma(arma_perdida)
159|             else:
160|                 texto = "⚪"
161|                 
162|         # Destacar unidade selecionada
163|         if st.session_state.unidade_selecionada == (i, j):
164|             texto = f"🟡{texto}"
165|                     
166|         # Criar botão da célula
167|         if cols[j].button(texto, key=f"btn_{i}_{j}", use_container_width=True):
168|             clicar_celula(i, j)
169|             st.rerun()
170| 
171| def mostrar_mensagens():
172|     st.markdown("---")
173|     st.subheader("Mensagens do Jogo")
174|     for msg in reversed(st.session_state.tabuleiro.mensagens[-5:]):
175|         st.write(msg)
176| 
177| def verificar_fim_jogo():
178|     tabuleiro = st.session_state.tabuleiro
179|     vencedor = tabuleiro.verificar_fim_jogo()
180|     
181|     if vencedor:
182|         st.balloons()
183|         st.success(f"🎉 Vitória dos {'Horácios' if vencedor == Equipe.HORACIOS else 'Curiácios'}! 🎉")
184|         if st.button("Novo Jogo"):
185|             st.session_state.tabuleiro = Tabuleiro()
186|             st.session_state.unidade_selecionada = None
187|             st.session_state.hora_inicio = datetime.datetime.now()
188|             st.rerun()
189| 
190| def main():
191|     # Configuração da página
192|     st.set_page_config(
193|         page_title="Os Horácios e os Curiácios",
194|         page_icon="⚔️",
195|         layout="wide",
196|         initial_sidebar_state="expanded"
197|     )
198| 
199|     # Inicialização do estado
200|     inicializar_estado()
201| 
202|     # Criar interface
203|     criar_barra_lateral()
204|     criar_tabuleiro()
205|     mostrar_mensagens()
206|     verificar_fim_jogo()
207| 
208| if __name__ == "__main__":
209|     main()
210| 

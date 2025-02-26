import asyncio
from streamlit.runtime.scriptrunner import get_script_run_ctx
if not get_script_run_ctx():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from game.board import Board
from game.models import Team, UnitType
import datetime

def initialize_state():
    if 'board' not in st.session_state:
        st.session_state.board = Board()
    if 'selected_unit' not in st.session_state:
        st.session_state.selected_unit = None
    if 'mode' not in st.session_state:
        st.session_state.mode = 'move'
    if 'start_time' not in st.session_state:
        st.session_state.start_time = datetime.datetime.now()
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def get_team_color(team):
    if team == Team.HORACIOS:
        return "🔵"  # Blue for Horacios
    elif team == Team.CURIACIOS:
        return "🔴"  # Red for Curiacios
    return "⚪"  # White for empty

def get_unit_symbol(unit):
    if not unit:
        return "　"
    
    unit_type = unit.type
    weapons = unit.weapon.quantity
    
    if unit_type == UnitType.ARCHER:
        return f"🏹{weapons}" if weapons > 0 else "🏹✖️"
    elif unit_type == UnitType.LANCER:
        return f"🗡️{weapons}" if weapons > 0 else "🗡️✖️"
    elif unit_type == UnitType.SWORDSMAN:
        return "⚔️" if weapons > 0 else "⚔️✖️"
    return "　"

def get_weapon_symbol(weapon_type):
    if weapon_type == UnitType.ARCHER:
        return "↟"  # Symbol for arrow
    elif weapon_type == UnitType.LANCER:
        return "†"  # Symbol for lance
    return "　"

def click_cell(i, j):
    board = st.session_state.board
    
    # If no unit is selected
    if st.session_state.selected_unit is None:
        unit = board.get_unit((i, j))
        if unit and unit.team == board.current_team:
            st.session_state.selected_unit = (i, j)
            board.messages.append(f"Unit selected at position ({i}, {j})")
    else:
        # If a unit is already selected
        origin = st.session_state.selected_unit
        if st.session_state.mode == 'move':
            board.move_unit(origin, (i, j))
        else:  # attack mode
            board.attack(origin, (i, j))
        st.session_state.selected_unit = None

def create_sidebar():
    with st.sidebar:
        st.header("Horacios and Curiacios")
        st.subheader("Controls")
        
        # Action mode
        st.session_state.mode = st.radio(
            "Action:",
            ['move', 'attack'],
            horizontal=True
        )
        
        # Reset button
        if st.button("Reset Game"):
            initialize_state()
        
        # Turn information
        st.markdown("---")
        st.subheader("Current Turn")
        current_team = "Horacios" if st.session_state.board.current_team == Team.HORACIOS else "Curiacios"
        st.write(f"Playing: {get_team_color(st.session_state.board.current_team)} {current_team}")
        
        # Game time
        elapsed_time = datetime.datetime.now() - st.session_state.start_time
        st.write(f"Game time: {elapsed_time.seconds // 60}:{elapsed_time.seconds % 60:02d}")
        
        # Legend
        st.markdown("---")
        st.subheader("Units")
        st.write("🏹 Archer (3 arrows, range: 7)")
        st.write("🗡️ Lancer (3 lances, range: 4)")
        st.write("⚔️ Swordsman (3 swords, range: 1)")
        
        st.subheader("Weapons on the Field")
        st.write("↟ Lost arrow")
        st.write("† Lost lance")
        
        st.subheader("Teams")
        st.write("🔵 Horacios")
        st.write("🔴 Curiacios")

def create_board():
    board = st.session_state.board
    
    # Container to center the board
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Create board grid
        for i in range(board.rows):
            cols = st.columns(board.columns)
            for j in range(board.columns):
                unit = board.get_unit((i, j))
                text = ""
                    
                # Check if there is a unit at the position
                if unit:
                    symbol = get_unit_symbol(unit)
                    color = get_team_color(unit.team)
                    text = f"{color}{symbol}"
                else:
                    # Check if there are lost weapons at the position
                    lost_weapon = next((weapon for weapon, pos in board.weapons_on_board if pos == (i, j)), None)
                    if lost_weapon:
                        text = get_weapon_symbol(lost_weapon)
                    else:
                        text = "⚪"
                    
                # Highlight selected unit
                if st.session_state.selected_unit == (i, j):
                    text = f"🟡{text}"
                            
                # Create cell button
                if cols[j].button(text, key=f"btn_{i}_{j}", use_container_width=True):
                    click_cell(i, j)
                    st.rerun()

def show_messages():
    st.markdown("---")
    st.subheader("Game Messages")
    for msg in reversed(st.session_state.board.messages[-5:]):
        st.write(msg)

def check_game_end():
    board = st.session_state.board
    winner = board.check_game_end()
    
    if winner:
        st.balloons()
        st.success(f"🎉 Victory for the {'Horacios' if winner == Team.HORACIOS else 'Curiacios'}! 🎉")
        if st.button("New Game"):
            st.session_state.board = Board()
            st.session_state.selected_unit = None
            st.session_state.start_time = datetime.datetime.now()
            st.rerun()

def main():
    # Page configuration
    st.set_page_config(
        page_title="Horacios and Curiacios",
        page_icon="⚔️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # State initialization
    initialize_state()

    # Create interface
    create_sidebar()
    create_board()
    show_messages()
    check_game_end()

if __name__ == "__main__":
    main()

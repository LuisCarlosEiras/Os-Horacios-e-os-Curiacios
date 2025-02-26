from typing import List, Tuple, Optional
from game.models import UnitType, Team, Unit

class Board:
    def __init__(self):
        self.rows = 10
        self.columns = 7
        self.board = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        self.current_team = Team.HORACIOS
        self.weapons_on_board = []
        self.messages = []
        self.curiacios_moves = 0
        self.initialize_board()

    def position_team(self, team: Team, start_row: int):
        unit_types = {
            Team.HORACIOS: [
                [UnitType.ARCHER, UnitType.ARCHER, UnitType.ARCHER],
                [UnitType.LANCER, UnitType.LANCER, UnitType.LANCER],
                [UnitType.SWORDSMAN, UnitType.SWORDSMAN, UnitType.SWORDSMAN]
            ],
            Team.CURIACIOS: [
                [UnitType.SWORDSMAN, UnitType.SWORDSMAN, UnitType.SWORDSMAN],
                [UnitType.LANCER, UnitType.LANCER, UnitType.LANCER],
                [UnitType.ARCHER, UnitType.ARCHER, UnitType.ARCHER]
            ]
        }

        for i, row_types in enumerate(unit_types[team]):
            for j, unit_type in enumerate(row_types):
                row = start_row + i
                column = (self.columns // 2 - 1) + j
                unit = Unit(unit_type, team, (row, column))
                if unit_type == UnitType.SWORDSMAN:
                    unit.weapon.quantity = 3
                self.board[row][column] = unit

    def initialize_board(self):
        self.position_team(Team.HORACIOS, 0)
        self.position_team(Team.CURIACIOS, self.rows - 3)
        self.messages.append("Game started - Horacios' turn")

    def get_unit(self, position: Tuple[int, int]) -> Optional[Unit]:
        if 0 <= position[0] < self.rows and 0 <= position[1] < self.columns:
            return self.board[position[0]][position[1]]
        return None

    def valid_position(self, position: Tuple[int, int]) -> bool:
        return 0 <= position[0] < self.rows and 0 <= position[1] < self.columns

    def move_unit(self, origin: Tuple[int, int], destination: Tuple[int, int]) -> bool:
        if not self.valid_position(origin) or not self.valid_position(destination):
            self.messages.append("Invalid position")
            return False

        unit = self.get_unit(origin)
        if not unit or unit.team != self.current_team:
            self.messages.append("Invalid unit or not your turn")
            return False

        if self.get_unit(destination):
            self.messages.append("Position occupied")
            return False

        if unit.can_move(destination, (self.rows, self.columns)):
            self.collect_weapons_on_path(unit, origin, destination)
            self.board[destination[0]][destination[1]] = unit
            self.board[origin[0]][origin[1]] = None
            unit.position = destination
            self.messages.append("Unit moved successfully")
            self.next_turn()
            return True

        self.messages.append("Invalid move")
        return False

    def collect_weapons_on_path(self, unit: Unit, origin: Tuple[int, int], destination: Tuple[int, int]):
        if unit.weapon.quantity == 0:
            weapons_to_remove = []
            for weapon, pos in self.weapons_on_board:
                if pos == destination:
                    unit.type = weapon
                    unit.weapon.type = weapon
                    unit.weapon.quantity = 1 if weapon == UnitType.SWORDSMAN else 3
                    weapons_to_remove.append((weapon, pos))
                    self.messages.append(f"Weapon collected: {weapon.value}")

            for weapon in weapons_to_remove:
                self.weapons_on_board.remove(weapon)

    def attack(self, attacker_pos: Tuple[int, int], target_pos: Tuple[int, int]) -> bool:
        attacker = self.get_unit(attacker_pos)

        if not attacker or attacker.team != self.current_team:
            self.messages.append("Invalid attacker or not your turn")
            return False

        if attacker.weapon.quantity <= 0:
            self.messages.append("Unit without weapons")
            return False

        target = self.get_unit(target_pos)

        if not attacker.can_attack(target_pos):
            self.messages.append("Attack out of range")
            return False

        if not target:
            if attacker.type in [UnitType.ARCHER, UnitType.LANCER]:
                self.weapons_on_board.append((attacker.type, target_pos))
                attacker.weapon.quantity -= 1
                self.messages.append(f"Weapon lost on board: {attacker.type.value}")
                self.next_turn()
                return True
            return False

        if target.team == attacker.team:
            self.messages.append("Cannot attack allies")
            return False

        if target.weapon.quantity > 0:
            self.weapons_on_board.append((target.type, target_pos))

        self.board[target_pos[0]][target_pos[1]] = None
        target.is_alive = False
        attacker.weapon.quantity -= 1

        self.messages.append("Successful attack!")
        self.next_turn()
        return True

    def next_turn(self):
        if self.current_team == Team.CURIACIOS:
            self.curiacios_moves += 1
            if self.curiacios_moves >= 2:
                self.current_team = Team.HORACIOS
                self.curiacios_moves = 0
        else:
            self.current_team = Team.CURIACIOS
        self.messages.append(f"Turn of the {'Curiacios' if self.current_team == Team.CURIACIOS else 'Horacios'}")

    def check_game_end(self) -> Optional[Team]:
        horacios_alive = curiacios_alive = False
        all_units_without_weapons = True

        for row in self.board:
            for unit in row:
                if unit and unit.is_alive:
                    if unit.weapon.quantity > 0:
                        all_units_without_weapons = False
                    if unit.team == Team.HORACIOS:
                        horacios_alive = True
                    elif unit.team == Team.CURIACIOS:
                        curiacios_alive = True

        if all_units_without_weapons and horacios_alive and curiacios_alive:
            self.messages.append("Peace declared - All units without weapons!")
            return None

        if not horacios_alive and not curiacios_alive:
            self.messages.append("Draw - All warriors have fallen!")
            return None
        elif not curiacios_alive:
            self.messages.append("Victory for the Horacios!")
            return Team.HORACIOS
        elif not horacios_alive:
            self.messages.append("Victory for the Curiacios!")
            return Team.CURIACIOS

        return None

    def get_game_status(self) -> dict:
        return {
            'current_team': self.current_team,
            'weapons_on_board': len(self.weapons_on_board),
            'messages': self.messages[-5:],
            'horacios_alive': sum(1 for row in self.board
                                  for unit in row
                                  if unit and unit.team == Team.HORACIOS and unit.is_alive),
            'curiacios_alive': sum(1 for row in self.board
                                   for unit in row
                                   if unit and unit.team == Team.CURIACIOS and unit.is_alive)
        }

    def print_board(self):
        symbols = {
            UnitType.ARCHER: 'A',
            UnitType.LANCER: 'L',
            UnitType.SWORDSMAN: 'E'
        }

        for row in self.board:
            row_str = '|'
            for unit in row:
                if unit:
                    symbol = symbols[unit.type]
                    if unit.type == UnitType.SWORDSMAN:
                        symbol += str(unit.weapon.quantity)
                    if unit.team == Team.HORACIOS:
                        row_str += f' H{symbol} |'
                    else:
                        row_str += f' C{symbol} |'
                else:
                    row_str += '    |'
            print(row_str)
        print("")

    def display_warrior_info(self):
        for row in self.board:
            for unit in row:
                if unit:
                    if unit.type == UnitType.SWORDSMAN:
                        print(f"{unit.team.name} Swordsman - Weapons: {unit.weapon.quantity}")
                    else:
                        print(f"{unit.team.name} {unit.type.name}")

# Example usage:
board = Board()
board.print_board()
board.display_warrior_info()

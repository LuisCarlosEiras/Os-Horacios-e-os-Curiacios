from enum import Enum
from typing import Tuple, List, Optional

class UnitType(Enum):
    ARCHER = "A"
    LANCER = "L"
    SWORDSMAN = "E"
    EMPTY = "."

class Team(Enum):
    HORACIOS = "H"
    CURIACIOS = "C"
    NONE = "."

class Weapon:
    def __init__(self, weapon_type: UnitType):
        self.type = weapon_type
        self.quantity = 3 if weapon_type in [UnitType.ARCHER, UnitType.LANCER, UnitType.SWORDSMAN] else 1

class Unit:
    def __init__(self, unit_type: UnitType, team: Team, position: Tuple[int, int]):
        self.type = unit_type
        self.team = team
        self.position = position
        self.weapon = Weapon(unit_type)
        self.is_alive = True

    def can_move(self, new_position: Tuple[int, int], board_size: Tuple[int, int]) -> bool:
        if not (0 <= new_position[0] < board_size[0] and 0 <= new_position[1] < board_size[1]):
            return False
        
        current_x, current_y = self.position
        new_x, new_y = new_position
        
        max_move = 2 if self.type in [UnitType.LANCER, UnitType.SWORDSMAN] else 1
        distance = max(abs(new_x - current_x), abs(new_y - current_y))
        return distance <= max_move

    def can_attack(self, target_position: Tuple[int, int]) -> bool:
        if not self.weapon.quantity > 0:
            return False

        current_x, current_y = self.position
        target_x, target_y = target_position
        distance = abs(target_x - current_x)

        if self.type == UnitType.ARCHER:
            return distance <= 7
        elif self.type == UnitType.LANCER:
            return distance <= 4
        else:  # SWORDSMAN
            return distance <= 1

from enum import Enum
import utils


class FieldState(Enum):  # stores what we know about an enemy field
    UNKNOWN = 0          # not yet known
    MISS = 1             # shot, and missed
    HIT = 2              # shot, and hit

    def __str__(self):
        if self.value == 1:
            return "O"
        elif self.value == 2:
            return "X"
        return " "


class ShipOrientation(Enum):  # used is the numeric id, but this is easier to use code-side
    HORIZONTAL = 0
    VERTICAL = 1


DEFAULT_FLEET = [0, 2, 2, 1, 1, 1]  # stores how many ships of each size are in the fleet
myFleet = utils.create_2d_list(10, 0)  # stores where the player's ships are stored
enemyField = utils.create_2d_list(10, FieldState.UNKNOWN)  # stores what is known about the enemy field


def place_ship(x, y, size, orientation):
    pass

from enum import Enum
import utils


class FieldState(Enum):  # stores what is known about a cell in the enemy field
    UNKNOWN = 0  # not yet known
    MISS = 1  # shot, and missed
    HIT = 2  # shot, and hit
    DESTROYED = 3  # shot, hit, and complete ship destroyed

    def __str__(self):
        if self.value == 1:
            return "○"
        elif self.value == 2:
            return "●"
        elif self.value == 3:
            return "■"
        return " "


class ShipOrientation(Enum):  # used is the numeric id, but this is easier to use code-side
    HORIZONTAL = 0
    VERTICAL = 1

    def __int__(self):
        return self.value


free_ship_ids = utils.create_and_fill_list(7, True)  # store the unused ids
ships_left = [0, 2, 2, 1, 1, 1]  # stores how many ships of each size are in the fleet (starting at 1x0)
my_fleet = utils.create_2d_list(10, 0)  # stores where the player's ships are stored
enemy_field = utils.create_2d_list(10, FieldState.UNKNOWN)  # stores what is known about the enemy field


def get_smallest_ship_id():
    for i in range(7):
        if free_ship_ids[i]:
            return i
    return -1


def place_ship(ship_positions):
    ship_id = get_smallest_ship_id()
    length = len(ship_positions)
    if ships_left[length] <= 0:
        return False, "no ship of that size left"
    for pos in ship_positions:
        if my_fleet[pos[0]][pos[1]] != 0:  # pos = [x, y], 0 means the space is still empty
            return False, "the ship does not fit there"
    # if this is reached, the ship does fit
    for pos in ship_positions:
        my_fleet[pos[0]][pos[1]] = ship_id
    ships_left[length] -= 1  # decrement the ships of the specific length we still have left
    free_ship_ids[ship_id] = False
    return True, "ship " + str(ship_id) + " placed"


def remove_ship(ship_id):
    for x in range(len(my_fleet)):
        for y in range(len(my_fleet[0])):
            if my_fleet[x][y] == ship_id:
                my_fleet[x][y] = 0
    free_ship_ids[ship_id] = True

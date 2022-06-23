from enum import Enum
import utils
from communication import GuessResponse


class FieldState(Enum):
    """stores what is known about a cell in the enemy field"""
    UNKNOWN = 0  # not yet known
    MISS = 1  # shot, and missed
    HIT = 2  # shot, and hit
    SUNK = 3  # shot, hit, and complete ship destroyed

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


class ShipPlacementResult(object):
    """returned by "place_ship" and gives various information about the call"""
    NO_MORE_OF_SIZE = 0, False, "no ship of that size left"
    DOES_NOT_FIT = 1, False, "the ship does not fit there"
    SUCCESS = 2, True, "ship {ship_id:d} placed successfully"

    def __init__(self, resultType, ship_id=-1):
        self.resultType = resultType
        self.ship_id = ship_id

    def status_code(self) -> int:
        return self.resultType[0]

    def succeeded(self) -> bool:
        return self.resultType[1]

    def failed(self) -> bool:
        return not self.resultType[1]

    def get_ship_id(self) -> int:
        return self.ship_id

    def get_message(self) -> str:
        return self.resultType[2].format(ship_id=self.ship_id)


free_ship_ids = utils.create_and_fill_list(7, True)  # store the unused ids
ships_left = [0, 2, 2, 1, 1, 1]  # stores how many ships of each size are in the fleet (starting at 1x0)
my_fleet = utils.create_2d_list(10, 0)  # stores where the player's ships are stored
enemy_field = utils.create_2d_list(10, FieldState.UNKNOWN)  # stores what is known about the enemy field


def is_out_of_ships() -> bool:
    return utils.add_all(ships_left)


def get_smallest_ship_id() -> int:
    """returns the smallest non-occupied ship id"""
    for i in range(7):
        if free_ship_ids[i]:
            return i + 1
    return -1


def place_ship(ship_positions: list) -> ShipPlacementResult:
    """Places a ship at the specified locations. """
    ship_id = get_smallest_ship_id()
    length = len(ship_positions)
    if ships_left[length] <= 0:
        return ShipPlacementResult(ShipPlacementResult.NO_MORE_OF_SIZE)
    for pos in ship_positions:
        if my_fleet[pos[0]][pos[1]] != 0:  # pos = [x, y], 0 means the space is still empty
            return ShipPlacementResult(ShipPlacementResult.DOES_NOT_FIT, my_fleet[pos[0]][pos[1]])
    # if this is reached, the ship does fit
    for pos in ship_positions:
        my_fleet[pos[0]][pos[1]] = ship_id
    ships_left[length] -= 1  # decrement the ships of the specific length we still have left
    free_ship_ids[ship_id] = False
    return ShipPlacementResult(ShipPlacementResult.SUCCESS, ship_id)


def remove_ship(ship_id) -> None:
    """Clears all fields that have a ship of the supplied id"""
    for x in range(len(my_fleet)):
        for y in range(len(my_fleet[0])):
            if my_fleet[x][y] == ship_id:
                my_fleet[x][y] = 0
    free_ship_ids[ship_id] = True


def process_guess(x: int, y: int) -> GuessResponse:
    field = my_fleet[x][y]
    if field == 0:
        return GuessResponse.MISS

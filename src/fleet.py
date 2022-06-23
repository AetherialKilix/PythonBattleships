# fleet.py manages the state of both fleets (player and enemy).

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
#ships_left = [0, 2, 2, 1, 1, 1]  # stores how many ships of each size are in the fleet (starting at 1x0)
ships_left = [0, 0, 1, 0, 0, 0]  # stores how many ships of each size are in the fleet (starting at 1x0)

my_fleet = utils.create_2d_list(10, 0)  # stores where the player's ships are stored
my_fleet_unhit = utils.create_2d_list(10, 0)  # stores where the enemy is yet to hit a ship (0 = water or hit, 1 = unhit)
enemy_field = utils.create_2d_list(10, FieldState.UNKNOWN)  # stores what is known about the enemy field


def is_out_of_ships() -> bool:
    return utils.add_all(ships_left) == 0


def get_smallest_ship_id() -> int:
    """returns the smallest non-occupied ship id"""
    for i in range(7):
        if free_ship_ids[i]:
            return i + 1
    return -1


def place_ship(ship_positions: list[tuple[int, int]]) -> ShipPlacementResult:
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
        my_fleet_unhit[pos[0]][pos[1]] = 1
    ships_left[length] -= 1  # decrement the ships of the specific length we still have left
    free_ship_ids[ship_id - 1] = False
    return ShipPlacementResult(ShipPlacementResult.SUCCESS, ship_id)


def remove_ship(ship_id) -> None:
    """Clears all fields that have a ship of the supplied id"""
    for x in range(len(my_fleet)):
        for y in range(len(my_fleet[0])):
            if my_fleet[x][y] == ship_id:
                my_fleet[x][y] = 0
                my_fleet_unhit[x][y] = 0
    free_ship_ids[ship_id] = True


def is_game_lost() -> bool:
    """returns true, if the game is lost"""
    return utils.add_all_2d(my_fleet_unhit) == 0


def __process_hit(x: int, y: int, ship_id: int) -> tuple[bool, list]:
    """processed a hit, and determines if a ship has sunk (if so, returns where exactly)"""
    # get a 2d-list of booleans. True = position occupied by the requested ship
    same_ship = utils.list_operator_2d(my_fleet, None, lambda a, none: a == ship_id)
    # store, that the ship at this posision was hit
    my_fleet_unhit[x][y] = 0
    # get a 2d-list of booleans. True = position occupied by the requested ship and the position is not yet hit
    same_ship_and_unhit = utils.list_operator_2d(same_ship, my_fleet_unhit, lambda a, b: 1 if (a and b == 1) else 0)

    if utils.add_all_2d(same_ship_and_unhit) == 0:  # means that all positions of this ship have been hit
        return True, utils.get_ends_of_list(utils.get_coords_from_2d_array(same_ship))
    return False, []


def process_opponent_guess(x: int, y: int) -> tuple[GuessResponse, list]:
    """processed an opponent's guess and returns the information needed to respond"""
    field = my_fleet[x][y]
    if field == 0:  # means, there is no ship -> MISS
        return GuessResponse.MISS, []

    if my_fleet_unhit[x][y] == 0:  # if not a miss, and not hit = 0 -> already guessed -> INVALID
        return GuessResponse.INVALID, []
    sunk, sunk_positions = __process_hit(x, y, field)
    if not sunk:
        return GuessResponse.HIT, []

    if is_game_lost():
        return GuessResponse.WIN, []

    return GuessResponse.SUNK, sunk_positions


def get_fleet_as_string() -> list[list[str]]:
    return utils.list_operator_2d(my_fleet, my_fleet_unhit, lambda a, b: a if a and b else ("X" if a and not b else " "))


def process_response(x: int, y: int, response: GuessResponse, sunk: list):
    if response == GuessResponse.MISS:
        enemy_field[x][y] = FieldState.MISS
    if response == GuessResponse.HIT:
        enemy_field[x][y] = FieldState.HIT
    if response == GuessResponse.SUNK:
        data = utils.get_cells_from_ends(sunk)
        for cell in data:
            enemy_field[cell[0]][cell[1]] = FieldState.SUNK

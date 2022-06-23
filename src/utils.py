from __future__ import annotations

import fleet


def add_all(values: list) -> int:
    out = 0
    for i in values:
        out += i
    return out


def add_all_2d(values: list) -> int:
    out = 0
    for row in values:
        for column in row:
            out += column
    return out


def create_2d_list(size: int, fill=None) -> list:
    out = []
    for i in range(size):
        this = []
        if fill is not None:
            for j in range(size):
                this.append(fill)
        out.append(this)
    return out


def to_string_list(data: list) -> list:
    out = []
    for entry in data:
        out.append(str(entry))
    return out


def list_operator(a: list, b: list | None, operator=lambda a, b: a + b) -> list:
    out = []
    if b is None:
        for i in range(len(a)):
            out = operator(a[i], None)
    else:
        for i in range(len(a)):
            out = operator(a[i], b[i])
    return out


def list_operator_2d(a: list[list], b: list[list] | None, operator=lambda a, b: a + b) -> list[list]:
    out = []
    if b is None:
        for row in range(len(a)):
            this_row = []
            for cell in range(len(a[row])):
                this_row.append(operator(a[row][cell], None))
            out.append(this_row)
    else:
        for row in range(len(a)):
            this_row = []
            for cell in range(len(a[row])):
                this_row.append(operator(a[row][cell], b[row][cell]))
            out.append(this_row)
    return out;


def create_and_fill_list(size: int, fill) -> list:
    out = []
    for i in range(size):
        out.append(fill)
    return out


def get_cells_from_ends(origin, end):
    # calculate delta
    delta = [0, 0]
    delta[0] = int(end[0]) - int(origin[0])
    delta[1] = int(end[1]) - int(origin[1])
    # check for rudimentary validity
    if delta[0] != 0 and delta[1] != 0:
        return None
    # if passes rudimentary validity test
    else:
        # calc ship-length
        ship_length = delta[0] + delta[1]
        is_ship_positive = 1 if ship_length >= 0 else 0
        ship_length = abs(ship_length)
        # check rotation
        if delta[0] > 0:
            direction = fleet.ShipOrientation.HORIZONTAL
        else:
            direction = fleet.ShipOrientation.VERTICAL
        # get all cells which are taken up by the ship
        cells = []
        for i in range(ship_length):
            if direction == fleet.ShipOrientation.HORIZONTAL:
                cells.append([origin[0] + i * is_ship_positive, origin[1]])
            else:
                cells.append([origin[0], origin[1] + i * is_ship_positive])
        # return ship cells
        return cells


def get_coords_from_2d_array(data):
    out = []
    # iterate over data and save the coords if the cell is true
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j]:
                out.append([j, i])
    # return output
    return out


def get_ends_of_list(list_in: list) -> list:
    return [list_in[0], list_in[len(list_in) - 1]]

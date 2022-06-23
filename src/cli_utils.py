import fleet

dummy_local_field = [[2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                     [2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                     [2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                     [2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                     [2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                     [2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                     [2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                     [2, 3, 3, 3, 3, 3, 3, 3, 3, 3]]
dummy_enemy_field = [["■", "○", " ", " ", " ", " ", " ", " ", " ", " "],
                     ["■", " ", " ", " ", "○", " ", " ", " ", " ", " "],
                     ["■", "●", " ", " ", " ", " ", " ", " ", "●", " "],
                     ["■", " ", " ", " ", "■", "■", " ", " ", " ", " "],
                     [" ", " ", "○", " ", " ", " ", " ", " ", " ", " "],
                     [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                     [" ", " ", " ", " ", " ", "○", " ", " ", " ", " "],
                     [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                     [" ", " ", " ", "●", " ", " ", " ", " ", " ", " "],
                     [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]

# ■○●

field_spacer = "         "
x_coords = "     A   B   C   D   E   F   G   H   I   J  "
horizontalLine = "   +---+---+---+---+---+---+---+---+---+---+"


def display_current_turn(my_data, en_data):
    # print initial lines
    print(x_coords + field_spacer + x_coords)
    print(horizontalLine + field_spacer + horizontalLine)
    # create display line by line
    for i in range(len(my_data)):
        # add row counter to my field
        line = str(i) + "  "
        # iterate over the row of my field
        for j in range(len(my_data[i])):
            # draw datapoint if it isn't 0 ; otherwise draw an empty cell
            if str(my_data[i][j]) != "0":
                line += "| " + str(my_data[i][j]) + " "
            else:
                line += "|   "

        # add spacer and row counter to enemy field
        line += "|" + field_spacer + " " + str(i) + " "

        # iterate over the row of my field
        for j in range(len(my_data[i])):
            # draw datapoint if it isn't 0 ; otherwise draw an empty cell
            if str(en_data[i][j]) != "0":
                line += "| " + str(en_data[i][j]) + " "
            else:
                line += "|   "
        # cap row
        line += "|"

        # draw constructed line
        print(line)
        # draw the lower border to the row
        print(horizontalLine + field_spacer + horizontalLine)


coord_dictionary = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 9,
}

default_text = ">>> Please enter your Target [Column,Row] :"


def get_coord_input(text):
    # get player input
    target = input(text)
    # declare output
    out = []
    # try interpreting the input
    try:
        print(target[0] + "|" + target[1])
        # lookup the value of a letter as an integer
        out.append(coord_dictionary[target[0]])
        # cast second value to int
        out.append(int(target[1]))
        return out
    # if interpreting wasn't successful try again
    except:
        # inform the player about their mistake
        print("--- input not valid, please try again:")
        # try again
        return get_coord_input(text)
    # return output


def get_place_input():
    # ask player for origin coords
    origin = get_coord_input(">>> Please enter the origin of the ship [Column,Row] :")
    # ask player for end coords
    destination = get_coord_input(">>> Please enter the end of the ship [Column,Row] :")
    # calculate delta
    delta = [0, 0]
    delta[0] = int(destination[0]) - int(origin[0])
    delta[1] = int(destination[1]) - int(origin[1])
    # check for rudimentary validity
    if (delta[0] != 0 and delta[1] != 0) or (delta[0] == 0 and delta[1] == 0):
        print("--- input has to be in one vertical or horizontal line, please try again:")
        # try again
        return get_place_input()
    # if passes rudimentary validity test
    else:
        # calc ship-length
        ship_length = delta[0] + delta[1]
        # check rotation
        if delta[0] > 0:
            direction = fleet.ShipOrientation.HORIZONTAL
        else:
            direction = fleet.ShipOrientation.VERTICAL
        # get all cells which are taken up by the ship
        cells = []
        for i in range(abs(ship_length)):
            if direction == fleet.ShipOrientation.HORIZONTAL:
                cells.append([origin[0] + i * (ship_length / abs(ship_length)), origin[1]])
            else:
                cells.append([origin[0], origin[1] + i * (ship_length / abs(ship_length))])

        print(ship_length)
        print(cells)

        # TODO: place

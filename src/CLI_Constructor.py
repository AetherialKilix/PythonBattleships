localField = [[2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
              [2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
              [2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
              [2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
              [2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
              [2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
              [2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
              [2, 3, 3, 3, 3, 3, 3, 3, 3, 3]]
enemyField = [[" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
              [" ", " ", " ", " ", "O", " ", " ", " ", " ", " "],
              [" ", "X", " ", " ", " ", " ", " ", " ", "X", " "],
              [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
              [" ", " ", "O", " ", " ", " ", " ", " ", " ", " "],
              [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
              [" ", " ", " ", " ", " ", "O", " ", " ", " ", " "],
              [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
              [" ", " ", " ", "X", " ", " ", " ", " ", " ", " "],
              [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]

fieldSpacer = "         "
x_coords = "     A   B   C   D   E   F   G   H   I   J  "
horizontalLine = "   +---+---+---+---+---+---+---+---+---+---+"


def display_current_turn(my_data, en_data):
    # print initial lines
    print(x_coords + fieldSpacer + x_coords)
    print(horizontalLine + fieldSpacer + horizontalLine)
    # create display line by line
    for i in range(len(my_data)):
        # add row counter to my field
        line = str(i ) + "  "
        # iterate over the row of my field
        for j in range(len(my_data[i])):
            # draw datapoint if it isn't 0 ; otherwise draw an empty cell
            if str(my_data[i][j]) != "0":
                line += "| " + str(my_data[i][j]) + " "
            else:
                line += "|   "

        # add spacer and row counter to enemy field
        line += "|" + fieldSpacer + " " + str(i) + " "

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
        print(horizontalLine + fieldSpacer + horizontalLine)


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


def getInput(text):

    target = input(text)
    out = []
    try:
        out = target.split(",")
        out[0] = coord_dictionary[out[0]]
        out[1] = int(out[1])
    except:
        print("--- input not valid, please try again:")
        return getInput()
    return out
import fleet
import communication as com
import main
import utils

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
        if out[1] < 10:
            return out
        else:
            # inform the player about their mistake
            print("--- input not valid, please try again:")
            # try again
            return get_coord_input(text)
    # if interpreting wasn't successful try again
    except ValueError or KeyError:
        # inform the player about their mistake
        print("--- input not valid, please try again:")
        # try again
        return get_coord_input(text)


def get_place_input():
    # ask player for origin coords
    origin = get_coord_input(">>> Please enter the origin of the ship [Column,Row] :")
    # ask player for end coords
    destination = get_coord_input(">>> Please enter the end of the ship [Column,Row] :")
    # calculate cells of ship
    cells = utils.get_cells_from_ends(origin, destination)
    if not cells:
        print("--- input has to be in one vertical or horizontal line, please try again:")
        # try again
        get_place_input()
    else:
        # try to place ship
        ans = fleet.place_ship(cells)
        # interpret answer of placement-call
        if ans.succeeded():
            # PARTEY
            # if out of ships
            if fleet.is_out_of_ships():
                print("--- Done placing, waiting for other player...")
                # TODO: Tell Networking that it should tell the other player he stinks
            # continue placing
            else:
                get_place_input()
        # if it was a failure
        else:
            # if it collided with another ship
            if ans.status_code() == 1:
                # print error message
                print("--- " + ans.get_message())
                # ask player if he wants to remove the ship that is in the way
                if get_binary_question_input(">>> Do you want to remove the colliding ship? (y/n):", "y", "n"):
                    # if yes, remove colliding ship & place new one
                    fleet.remove_ship(ans.get_ship_id())
                    fleet.place_ship(cells)
                else:
                    # try again
                    get_place_input()
            # if it failed for another reason
            else:
                # print error message
                print("--- " + ans.get_message())
                # continue placing
                get_place_input()


def ship_placement_dialogue():
    get_place_input()


def active_turn_dialogue(state):
    if state == "server":
        target = get_coord_input(">>> Please enter your Target [Column,Row] :")
        main.connection.send_guess(target)
        main.connection.await_response()
        x, y = main.connection.await_guess()
        action = fleet.process_opponent_guess(x, y)
        print_action(action)
        main.connection.await_guess()
        # TODO: implement guess interpretation
        main.connection.send_response()
        active_turn_dialogue("playing")
    elif state == "client":
        x, y = main.connection.await_guess()
        action = fleet.process_opponent_guess(x, y)
        print_action(action)
        main.connection.send_response()
        active_turn_dialogue("playing")
    elif state == "playing":
        target = get_coord_input(">>> Please enter your Target [Column,Row] :")
        main.connection.send_guess(target)
        main.connection.await_response()
        x, y = main.connection.await_guess()
        action = fleet.process_opponent_guess(x, y)
        print_action(action)
        main.connection.await_guess()
        # TODO: implement guess interpretation
        main.connection.send_response()
        active_turn_dialogue("playing")
    else:
        server_client_dialogue()


def print_action(action):
    if action == com.GuessResponse.SUNK:
        print("The opponent has sunk one of your ships!")
    if action == com.GuessResponse.HIt:
        print("The opponent has hit one of your ships!")
    if action == com.GuessResponse.MISS:
        print("The opponent has missed!")
    if action == com.GuessResponse.WIN:
        print("The opponent has won the game!")


def server_client_dialogue():
    # get player answer
    if get_binary_question_input(">>> Do you want to be the server or the client? (s/c):", "s", "c"):
        # provide feedback
        print("--- You are the server now.")
        # get player defined port
        port = input(">>> Please enter the Port you want to use: ")
        # if port exists try opening port
        if port:
            try:
                # cast port to integer
                port = int(port)
                # try to open port
                main.connection = com.Connection("server", port)
                return "server"
            except ValueError:
                print("--- Input was not valid, please try again. Default Port is being used.")
                # try to open default port
                main.connection = com.Connection("server")
                return "server"
        else:
            # try to open default port
            main.connection = com.Connection("server")
            return "server"
    else:
        # give feedback
        print("--- You are a client now.")
        # input for user defined IP
        ip = input(">>> Please enter the IP-Address you want to play with: ")
        # input for user defined port
        port = input(">>> Please enter the Port you want to use: ")
        # if port exists try opening connection via that port
        if port:
            try:
                # cast port to integer
                port = int(port)
                # try to open connection to ip via defined port
                main.connection = com.Connection("client", port, ip)
                return "client"
            except ValueError:
                print("--- Input was not valid, please try again. Default Port is being used.")
                # try to open connection to ip via default port
                main.connection = com.Connection("client", address=ip)
                return "client"
        else:
            # try to open connection to ip via default port
            main.connection = com.Connection("client", address=ip)
            return "client"


def get_binary_question_input(text, arg1, arg2):
    # get player input
    answer = input(text)
    # check player answer
    if answer[0].lower() == arg1:
        return True
    elif answer[0].lower() == arg2:
        return False
    else:
        print("--- input isn't valid (" + arg1 + "/" + arg2 + "), please try again")
        return get_binary_question_input(text, arg1, arg2)


import fleet
import communication as com
import utils


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
    target = input(text).upper()
    # declare output
    out = []
    # try interpreting the input
    try:
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


# TODO: while True & continue
def get_place_input():
    # display field
    display_current_turn(fleet.get_fleet_as_string(), fleet.enemy_field)
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
        # display fields
        display_current_turn(fleet.get_fleet_as_string(), fleet.enemy_field)
        # let player select target
        target = get_coord_input(">>> Please enter your Target [Column,Row] :")
        # send target coords
        com.INSTANCE.send_guess(target[0], target[1])
        # receive answer
        response, payload = com.INSTANCE.await_response()
        # interpret answer
        print_own_action(response)
        if response == fleet.GuessResponse.WIN:
            com.INSTANCE.close()
            quit()
        elif response == fleet.GuessResponse.INVALID:
            print("you hit the same tile a second time. Please just don't. You are smarter than this!")
        # TODO: implement guess interpretation
        # wait for enemy guess
        x, y = com.INSTANCE.await_guess()
        # display fields
        display_current_turn(fleet.get_fleet_as_string(), fleet.enemy_field)
        # interpret enemy guess
        action = fleet.process_opponent_guess(x, y)
        print_enemy_action(action)
        # send answer to enemy
        com.INSTANCE.send_response(action[0], action[1])
        # start over
        active_turn_dialogue("playing")
    elif state == "client":
        # wait for enemy guess
        x, y = com.INSTANCE.await_guess()
        # interpret enemy guess
        action = fleet.process_opponent_guess(x, y)
        print_enemy_action(action)
        # display fields
        display_current_turn(fleet.get_fleet_as_string(), fleet.enemy_field)
        # send answer to enemy
        com.INSTANCE.send_response(action[0], action[1])
        # start over
        active_turn_dialogue("playing")
    elif state == "playing":
        # display fields
        display_current_turn(fleet.get_fleet_as_string(), fleet.enemy_field)
        # let player select a target
        target = get_coord_input(">>> Please enter your Target [Column,Row] :")
        # send target coords
        com.INSTANCE.send_guess(target[0], target[1])
        # receive answer
        response, payload = com.INSTANCE.await_response()
        # interpret answer
        print_own_action(response)
        if response == fleet.GuessResponse.WIN:
            com.INSTANCE.close()
            quit()
        fleet.process_response(target[0], target[1], response, payload)
        # wait for enemy guess
        x, y = com.INSTANCE.await_guess()
        # interpret enemy guess
        action = fleet.process_opponent_guess(x, y)
        print_enemy_action(action)
        # display fields
        display_current_turn(fleet.get_fleet_as_string(), fleet.enemy_field)
        # send answer to enemy
        com.INSTANCE.send_response(action[0], action[1])
        # start  over
        active_turn_dialogue("playing")
    else:
        server_client_dialogue()


def print_enemy_action(action):
    if action == com.GuessResponse.SUNK:
        print("The opponent has sunk one of your ships!")
    if action == com.GuessResponse.HIT:
        print("The opponent has hit one of your ships!")
    if action == com.GuessResponse.MISS:
        print("The opponent has missed!")
    if action == com.GuessResponse.WIN:
        print("The opponent has won the game! Better luck next time!")
        quit()


def print_own_action(action):
    if action == com.GuessResponse.SUNK:
        print("You sunk one of the opponents ships!")
    if action == com.GuessResponse.HIT:
        print("You hit one of the opponents ships!")
    if action == com.GuessResponse.MISS:
        print("You have missed!")
    if action == com.GuessResponse.WIN:
        print("You have won the game! Congratulations!")


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
                com.INSTANCE = com.Connection("server", port)
                return "server"
            except ValueError:
                print("--- Input was not valid, please try again. Default Port is being used.")
                # try to open default port
                com.INSTANCE = com.Connection("server")
                return "server"
        else:
            # try to open default port
            com.INSTANCE = com.Connection("server")
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
                com.INSTANCE = com.Connection("client", port, ip)
                return "client"
            except ValueError:
                print("--- Input was not valid, please try again. Default Port is being used.")
                # try to open connection to ip via default port
                com.INSTANCE = com.Connection("client", address=ip)
                return "client"
        else:
            # try to open connection to ip via default port
            com.INSTANCE = com.Connection("client", address=ip)
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

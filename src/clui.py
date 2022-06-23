import time

import fleet
import communication as com
import utils


field_spacer    = "         "
x_coords        = "     A   B   C   D   E   F   G   H   I   J  "
horizontalLine  = "   +---+---+---+---+---+---+---+---+---+---+"


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
        # cast second value to int
        out.append(int(target[1]))
        # lookup the value of a letter as an integer
        out.append(coord_dictionary[target[0]])
        if out[1] < 10:
            return out
        else:
            # inform the player about their mistake
            print("--- input not valid, please try again: ")
            # try again
            return get_coord_input(text)
    # if interpreting wasn't successful try again
    except ValueError or KeyError:
        # inform the player about their mistake
        print("--- input not valid, please try again: ")
        # try again
        return get_coord_input(text)


def get_place_input():
    # display field
    display_current_turn(fleet.get_fleet_as_string(), fleet.enemy_field)
    # ask player for origin coords
    origin = get_coord_input(">>> Please enter the origin of the ship [Column,Row] : ")
    if not origin:
        get_place_input()
    # ask player for end coords
    destination = get_coord_input(">>> Please enter the end of the ship [Column,Row] : ")
    if not destination:
        get_place_input()
    # calculate cells of ship
    cells = utils.get_cells_from_ends(origin, destination)
    if not cells:
        print("--- input has to be in one vertical or horizontal line, please try again: ")
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
                # display fields
                display_current_turn(fleet.get_fleet_as_string(), fleet.enemy_field)
                print("--- Done placing, waiting for other player...")
                com.INSTANCE.await_both_done()
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
                if get_binary_question_input(">>> Do you want to remove the colliding ship? (y/n): ", "y", "n"):
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
        # let player select target
        target = get_coord_input(">>> Please enter your Target [Column,Row] : ")
        # send target coords
        com.INSTANCE.send_guess(target[0], target[1])
        # receive answer
        response, payload = com.INSTANCE.await_response()
        if response == fleet.GuessResponse.WIN:
            com.INSTANCE.close()
            print_own_action(response)
            quit()
        fleet.process_response(target[0], target[1], response, payload)
        # display fields
        display_current_turn(fleet.get_fleet_as_string(), fleet.enemy_field)
        # interpret answer
        print_own_action(response)
        # wait for enemy guess
        x, y = com.INSTANCE.await_guess()
        # interpret enemy guess
        action = fleet.process_opponent_guess(x, y)
        # display fields
        display_current_turn(fleet.get_fleet_as_string(), fleet.enemy_field)
        print_enemy_action(action[0])
        # send answer to enemy
        com.INSTANCE.send_response(action[0], action[1])
        if action[0] == com.GuessResponse.WIN:
            com.INSTANCE.close()
            quit()
        # start over
        active_turn_dialogue("playing")
    elif state == "client":
        # wait for enemy guess
        x, y = com.INSTANCE.await_guess()
        # interpret enemy guess
        action = fleet.process_opponent_guess(x, y)
        # display fields
        display_current_turn(fleet.get_fleet_as_string(), fleet.enemy_field)
        print_enemy_action(action[0])
        # send answer to enemy
        com.INSTANCE.send_response(action[0], action[1])
        if action[0] == com.GuessResponse.WIN:
            com.INSTANCE.close()
            quit()
        # start over
        active_turn_dialogue("playing")
    elif state == "playing":
        # let player select a target
        target = get_coord_input(">>> Please enter your Target [Column,Row] :")
        # send target coords
        com.INSTANCE.send_guess(target[0], target[1])
        # receive answer
        response, payload = com.INSTANCE.await_response()
        if response == fleet.GuessResponse.WIN:
            print_own_action(response)
            com.INSTANCE.close()
            quit()
        fleet.process_response(target[0], target[1], response, payload)
        # display fields
        display_current_turn(fleet.get_fleet_as_string(), fleet.enemy_field)
        # interpret answer
        print_own_action(response)
        # wait for enemy guess
        x, y = com.INSTANCE.await_guess()
        # interpret enemy guess
        action = fleet.process_opponent_guess(x, y)
        # display fields
        display_current_turn(fleet.get_fleet_as_string(), fleet.enemy_field)
        print_enemy_action(action[0])
        # send answer to enemy
        com.INSTANCE.send_response(action[0], action[1])
        if action[0] == com.GuessResponse.WIN:
            com.INSTANCE.close()
            quit()
        # start  over
        active_turn_dialogue("playing")
    else:
        server_client_dialogue()


def print_enemy_action(action):
    if action == com.GuessResponse.SUNK:
        print("The opponent has sunk one of your ships!")
    elif action == com.GuessResponse.HIT:
        print("The opponent has hit one of your ships!")
    elif action == com.GuessResponse.MISS:
        print("The opponent has missed!")
    elif action == com.GuessResponse.WIN:
        print("The opponent has won the game! Better luck next time!")
    else:
        print("The opponent has played an invalid turn!")


def print_own_action(action):
    if action == com.GuessResponse.SUNK:
        print("You sunk one of the opponents ships!")
    elif action == com.GuessResponse.HIT:
        print("You hit one of the opponents ships!")
    elif action == com.GuessResponse.MISS:
        print("You have missed!")
    elif action == com.GuessResponse.WIN:
        print("You have won the game! Congratulations!")
    elif action == com.GuessResponse.INVALID:
        print("You hit the same tile a second time. Please just don't. You are smarter than this!")


def server_client_dialogue():
    # get player answer
    if get_binary_question_input(">>> Do you want to be the server or the client? (s/c) : ", "s", "c"):
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

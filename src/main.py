from clui import server_client_dialogue, ship_placement_dialogue, active_turn_dialogue


def event_order():
    role = server_client_dialogue()
    ship_placement_dialogue()
    active_turn_dialogue(role)


# start game
event_order()
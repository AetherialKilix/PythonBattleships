import clui as cli

connection = None


def event_order():
    role = cli.server_client_dialogue()
    cli.ship_placement_dialogue()
    cli.active_turn_dialogue(role)


# start game
event_order()
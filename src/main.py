import cli_utils as cli


def event_order():
    cli.server_client_dialogue()
    cli.ship_placement_dialogue()
    cli.active_turn_dialogue()


# start game
event_order()

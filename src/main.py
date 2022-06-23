from clui import server_client_dialogue, ship_placement_dialogue, active_turn_dialogue


def event_order():
    role = server_client_dialogue()
    ship_placement_dialogue()
    active_turn_dialogue(role)


# start game
event_order()

"""
import clui
import fleet

print(fleet.place_ship([(0, 0), (0, 1), (0, 2), (0, 3)]).get_message())
print(fleet.__process_hit(0, 2, 1))

print(fleet.place_ship([(0, 1), (0, 2)]).get_message())
print(fleet.place_ship([(1, 0), (1, 1), (1, 2), (1, 3)]).get_message())


print(fleet.place_ship([(1, 1), (1, 2), (1, 3)]).get_message())
fleet.remove_ship(2)

print("lost? ", fleet.is_game_lost())

clui.display_current_turn(fleet.get_fleet_as_string(), fleet.enemy_field)

print(fleet.__process_hit(0, 0, 1))
print(fleet.__process_hit(0, 1, 1))
print(fleet.__process_hit(0, 3, 1))

print("lost? ", fleet.is_game_lost())
"""

from math import sqrt

def step(world):
	comand = {}
	# print(world["units"])
	unit = world["units"][world["self_id"]]
	# print(unit)

	if unit.hp >= 5:
		return {"key" : "split", "give" : 2}

	# comands[unit_id] = {"key" : "move", "x" : 5, "y" : 5}
	near_food = -1
	near_food_length = 0

	for food_id in world["food"]:
		food = world["food"][food_id]
		if near_food == -1 or sqrt((food.x - unit.x) ** 2 + (food.y - unit.y) ** 2) < near_food_length:
			near_food = food_id
			near_food_length = sqrt((food.x - unit.x) ** 2 + (food.y - unit.y) ** 2)

	if near_food == -1:
		# print("afk")
		return {"key" : "afk"}

	comand = {"key" : "move", "y" : 10, "x" : 0}

	food = world["food"][near_food]
	comand["x"] = food.x - unit.x
	comand["y"] = food.y - unit.y

	if sqrt((comand["x"]) ** 2 + (comand["y"]) ** 2) > unit.max_step:
		max_way = sqrt((comand["x"]) ** 2 + (comand["y"]) ** 2)
		# print(max_way, comand["x"], comand["y"])

		comand["x"] *= unit.max_step / max_way
		comand["y"] *= unit.max_step / max_way
		while sqrt((comand["x"]) ** 2 + (comand["y"]) ** 2) > unit.max_step:
			# print("HELP")
			# print("WAIT")
			comand["x"] *= 0.9999999999999
			comand["y"] *= 0.9999999999999

	# print(comand)
	return comand
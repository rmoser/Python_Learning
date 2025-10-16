def is_even(x):
	return x % 2 == 0

def is_odd(x):
	return bool(x % 2)

def can_plant(crop):
	if crop in (Entities.Grass, Entities.Bush, Entities.Tree, Entities.Cactus):
		return True

	if crop == Entities.Carrot:
		return num_items(Items.Hay) > 0 and num_items(Items.Wood) > 0
		
	if crop in (Entities.Pumpkin, Entities.Sunflower):
		return num_items(Items.Carrot) > 0

def move_drone(x, y):
	if get_pos_x() > x:
		dir_ew = West
	else:
		dir_ew = East
	while get_pos_x() != x:
		move(dir_ew)

	if get_pos_y() > y:
		dir_nw = South
	else:
		dir_nw = North			
	while get_pos_y() != y:
		move(dir_nw)


def harvest_all():
	move_drone(0, 0)
	
	func = _harvest_all
	drone_func(func)

	move_drone(0, 0)

def _harvest_all():
	for c in range(get_world_size() // max_drones()):
		for r in range(get_world_size()):
			harvest()
			move(North)
		move(East)
		
		
def bones(n):
	harvest_all()
	change_hat(Hats.Dinosaur_Hat)
	
	def move_snake():
		
		if get_pos_x() > 0 and get_pos_y() == 0:
			dir = West

		elif get_pos_x() == get_world_size()-1 and get_pos_y() > 0:
			dir = South

		elif is_even(get_pos_x()):
			if get_pos_y() < get_world_size()-1:
				dir = North
			else:
				dir = East
		else:
			if get_pos_y() > 1:
				dir = South
			else:
				dir = East
		return move(dir)
		

	while move_snake():
		pass
	change_hat(Hats.Gold_Hat)
			
		
	
def reset(ground_type):
	harvest_all(ground_type)


from vars import *
from funcs import *

quick_print(crop_loops)

def _farm_grass():
	crop = Entities.Grass
	if not can_plant(crop):
		continue

	if crop in crop_loops:
		loops = crop_loops[crop]
	else:
		loops = 1
	for _ in range(get_world_size() // max_drones() * loops):
		for _ in range(get_world_size()):
			harvest()
				
			if get_ground_type() != Grounds.Grassland:
				till()
#			plant(crop)
						
			move(North)
		move(East)


					
def _farm_tree():
	crop = Entities.Tree
	if not can_plant(crop):
		continue

	if crop in crop_loops:
		loops = crop_loops[crop]
	else:
		loops = 1
	for _ in range(get_world_size() // max_drones() * loops):
		for _ in range(get_world_size()):
			harvest()
			if get_ground_type() != Grounds.Soil:
				till()

			if is_even(get_pos_y() + get_pos_x()):
				_crop = Entities.Tree
			elif crop == Entities.Tree:
				_crop = Entities.Bush
			plant(_crop)
						
			move(North)
		move(East)



def _farm_crop(crop):
	if not can_plant(crop):
		continue

	if crop in crop_loops:
		loops = crop_loops[crop]
	else:
		loops = 1
	for c in range(get_world_size() // max_drones() * loops):
		quick_print("Farming ", str(crop), " loop: ", c // loops)
		for _ in range(get_world_size()):
			harvest()
			if get_ground_type() != Grounds.Soil:
				till()

			plant(crop)
						
			move(North)
		move(East)
		

def _farm_carrot():
	_farm_crop(Entities.Carrot)

def _farm_cactus():
	_farm_crop(Entities.Cactus)

def _farm_sunflower():
	_farm_crop(Entities.Sunflower)

def farm_apple():
	_farm_crop(Entities.Apple)

def _farm_bush():
	_farm_crop(Entities.Bush)

def _farm_apple():
	_farm_crop(Entities.Apple)

def _farm_pumpkin():
	# TODO: Rewrite for pumpkins
	#_farm_crop(Entities.Pumpkin)


	if not can_plant(crop):
		continue

	if crop in crop_loops:
		loops = crop_loops[crop]
	else:
		loops = 1

	for c in range(get_world_size() // max_drones() * loops):
		quick_print("Farming ", str(crop), " loop: ", c // loops)
		for _ in range(get_world_size()):
			if crop != Entities.Pumpkin or get_entity_type() not in (Entities.Pumpkin, Entities.Dead_Pumpkin):
				harvest()

			if get_ground_type() != Grounds.Soil:
				till()

			while can_plant(crop):
				if get_entity_type() != crop:
					plant(crop)
					if num_items(Items.Fertilizer) > 0:
						use_item(Items.Fertilizer)
				elif can_harvest():
					break
				else:
					if get_entity_type() != crop:
						plant(crop)
						
			move(North)
		move(East)
		

	for c in range(get_world_size()):
		for r in range(get_world_size()):
			if crop != Entities.Pumpkin or get_entity_type() not in (Entities.Pumpkin, Entities.Dead_Pumpkin):
				harvest()
			
			if crop in (Entities.Grass, Entities.Tree, Entities.Carrot, Entities.Bush, Entities.Cactus, Entities.Sunflower):
				farm_drones(crop, crop_loops[crop])
					

			elif crop == Entities.Pumpkin:
				if get_ground_type() != Grounds.Soil:
					till()

				if passes == 0:
					while can_plant(crop):
						if get_entity_type() != crop:
							plant(crop)
							if num_items(Items.Fertilizer) > 0:
								use_item(Items.Fertilizer)
						elif can_harvest():
							break
				else:
					if get_entity_type() != crop:
						plant(crop)
														

			else:
				if get_ground_type() != Grounds.Soil:
					till()
				plant(crop)
				
			quick_print("Planting: ", crop, " at: (", get_pos_x(), ", ", get_pos_y(), ") Passes: ", passes)

			if crop in (Entities.Tree, Entities.Pumpkin) and not can_harvest() and get_water() < 0.5 and num_items(Items.Water) > 0:
				use_item(Items.Water)
				
			move(North)
		move(East)

	if passes == 0 and crop == Entities.Pumpkin:
		harvest()

def _plant(crop):
	if not can_plant(crop):
		continue

	for c in range(get_world_size() // max_drones()):
		for _ in range(get_world_size()):
			harvest()
			if get_ground_type() != Grounds.Soil:
				till()

			plant(crop)
						
			move(North)
		move(East)
		


drone_funcs = {
	Entities.Apple: _farm_apple,
	Entities.Bush: _farm_bush,
	Entities.Cactus: _farm_cactus,
	Entities.Carrot: _farm_carrot,
	Entities.Grass: _farm_grass,
	Entities.Pumpkin: _farm_pumpkin,
	Entities.Sunflower: _farm_sunflower,
	Entities.Tree: _farm_tree   
}

def farm_drones(crop, passes):
	if crop in drone_funcs:
		func = drone_funcs[crop]
	else:
		return
	crop_loops[crop] = passes
	
	n = max_drones() - num_drones()
	quick_print("Spawn ", n, " drones.")
	for i in range(n+1):
		if spawn_drone(func):
			for c in range((get_world_size() // max_drones())):
				move(East)
		else:
			func()

def drone_func(func):
	n = max_drones() - num_drones()
	quick_print("Spawn ", n, " drones.")
	for i in range(n+1):
		if spawn_drone(func):
			for c in range((get_world_size() // max_drones())):
				move(East)
		else:
			func()
	

def harvest_all():
	move_drone(0, 0)
	
	func = _harvest
	drone_func(func)

	move_drone(0, 0)

def _harvest():
	for c in range(get_world_size() // max_drones()):
		for r in range(get_world_size()):
			harvest()
			move(North)
		move(East)
		
def plant_all(crop):
	if not can_plant(crop):
		return
		
	move_drone(0, 0)
	
	func = __plant(crop)
	drone_func(func)

	move_drone(0, 0)

def __plant(crop):
	def _plant():
		for c in range(get_world_size() // max_drones()):
			for r in range(get_world_size()):
				plant(crop)
				move(North)
			move(East)
	return _plant


dirs = [North, East, South, West]
on_left = [West, North, East, South]

def _directions():
	global dirs
	global on_left
	_dirs = []
	for i in range(4):
		if can_move(dirs[i]):
			_dirs.append(i)
	return _dirs

def __find_treasure(d):
	def _find_treasure():
		while True:
			if get_entity_type() == Entities.Treasure:
				harvest()
				break
#  I think the maze exits when the treasure is found
#            if not measure():
#                break

			direction = dirs[d]
			if can_move(on_left[d]):
				d = (d - 1) % 4
				move(direction)
			else:
				d = (d + 1) % 4

	return _find_treasure


def maze(n):
	while n > 0:
		if n > 0:
			n -= 1

		if num_items(Items.Weird_Substance) == 0:
			return
	
		s = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
		if s > num_items(Items.Weird_Substance):
			s = num_items(Items.Weird_Substance)
	
		plant(Entities.Bush)
		use_item(Items.Weird_Substance, s)

		_dirs = _directions()
		for i in range(1, len(_dirs)):
			spawn_drone(__find_treasure(_dirs[i]))
		__find_treasure(0)()
			
			  
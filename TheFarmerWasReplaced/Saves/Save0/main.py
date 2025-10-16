from funcs import *
from farming import *
from vars import *

def choose_crop():
	item_counts = {}
	for i in Items:
		item_counts[i] = num_items(i)
	
	if item_counts[Items.Power] < 1000:
		return Entities.Sunflower
	
	if item_counts[Items.Gold] < 32000:
		return Entities.Treasure
	
	if item_counts[Items.Pumpkin] < 1000:
		return Entities.Pumpkin
	
	if item_counts[Items.Wood] < 100000:
		return Entities.Tree
	
	if item_counts[Items.Hay] < 5000000:
		return Entities.Grass
	
	if item_counts[Items.Carrot] < 1000:
		return Entities.Carrot
	
	if item_counts[Items.Bone] < 1000:
		return Entities.Dinosaur
	
	i = Entities.Dead_Pumpkin
	e = list(Entities)
	while i == Entities.Dead_Pumpkin:
		i = e[len(e) * random() // 1]
	
	return i
		
	
if __name__ == "__main__":
	move_drone(0, 0)
	while True:
		crop = choose_crop()
#		for crop in crops:
		quick_print("Crop:", crop)

		if crop == Entities.Treasure:
			maze(crop_loops[crop])
			move_drone(0, 0)
			continue

		if crop == Entities.Dinosaur:
			bones(crop_loops[crop])
			move_drone(0, 0)
			continue
				
		if not can_plant(crop):
			continue

		if crop == Entities.Pumpkin:
			passes = 2
		else:
			passes = 1
		
		while passes > 0:
			passes -= 1

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

	#			if crop == Entities.Pumpkin and passes == 0:
	#				harvest_all()
			
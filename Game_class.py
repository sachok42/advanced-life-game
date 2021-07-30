from math import *
import pygame
import time
from random import randint
from Unit_class import Unit
from Food_class import Food
from time import sleep
# MAX_STEP = 10.x

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# font = pygame.font.SysFont("Consolas", 50)

def length(x, y):
	return sqrt(x * x + y * y)


def dist(a, b):
	return length(a.x - b.x, a.y - b.y)

class Game():
	def __init__(self, ais_len=0, width=1920, height=1080):
		self.units = {}
		self.food = {}
		self.AI_types = {}

		self.next_unit_id = 0
		self.next_food_id = 0

		self.food_spawn_cd = 5
		self.hunger_cd = 60

		self.borning_units = []

		self.width = width
		self.height = height
		for i in range(ais_len):
			filename = input()
			self.AI_types[i] = {}

			with open(filename) as fp:
				string = fp.read()
				exec(string, self.AI_types[i])

			self.add_unit(Unit(randint(0, self.width), randint(0, self.height), i, 10, 3))

	def add_food(self, food):
		self.food[self.next_food_id] = food
		self.next_food_id += 1

	def add_unit(self, unit):
		self.units[self.next_unit_id] = unit
		self.next_unit_id += 1

	def collsion_unit_food(self, unit_id, food_id):
		unit = self.units[unit_id]
		food = self.food[food_id]

		if sqrt((unit.x - food.x) ** 2 + (unit.y - food.y) ** 2) < unit.radius + food.radius:
			return True

		return False

	def unit_see_food(self, unit_id, food_id):
		unit = self.units[unit_id]
		food = self.food[food_id]
		# print(sqrt((unit.x - food.x) ** 2 + (unit.y - food.y) ** 2))

		if sqrt((unit.x - food.x) ** 2 + (unit.y - food.y) ** 2) < unit.radius + food.radius + unit.vision_radius:
			return True

		return False

	def unit_see_unit(self, unit_id, unit_id2):
		unit = self.units[unit_id]
		unit2 = self.units[unit_id2]
		# print(sqrt((unit.x - unit2.x) ** 2 + (unit.y - unit2.y) ** 2))

		if sqrt((unit.x - unit2.x) ** 2 + (unit.y - unit2.y) ** 2) < unit.radius + unit2.radius + unit.vision_radius:
			return True

		return False

	def move_unit(self, unit_id, x, y):
		# unit = self.units[unit_id]
		# print(sqrt(x ** 2 + y ** 2))
		if sqrt(x ** 2 + y ** 2) <= self.units[unit_id].max_step:
			self.units[unit_id].move(x, y)

		delete_list = []

		for food_id in self.food:
			if self.collsion_unit_food(unit_id, food_id):
				self.units[unit_id].hp += self.food[food_id].radius
				delete_list.append(food_id)

		for i in delete_list:
			self.food.pop(i)

		# print(sqrt(x ** 2 + y ** 2))

	def give_data(self, unit_id):
		# print("hey")
		world = {}
		world["self_id"] = unit_id
		world["world"] = {"width" : self.width, "height" : self.height}

		world["units"] = {}
		world["food"] = {}

		for unit_id_ in self.units:
			# print(unit_id_)
			if self.unit_see_unit(unit_id, unit_id_):
				# print(unit_id_)
				world["units"][unit_id_] = self.units[unit_id_]

		for food_id in self.food:
			if self.unit_see_food(unit_id, food_id):
				world["food"][food_id] = self.food[food_id]

		return world

	def split(self, unit_id, give):
		if self.units[unit_id].hp > give:
			self.units[unit_id].hp -= give
			unit = self.units[unit_id]
			self.borning_units.append(Unit(unit.x, unit.y + unit.radius * 2, unit.AI_num, unit.radius, give, unit.max_step, unit.vision_radius))
			# print(self.borning_units[-1].max_step)
			# print(unit.max_step)
			
	def take_comand(self, unit_id, comand):
		if comand["key"] == "afk":
			return

		elif comand["key"] == "move":
			self.move_unit(unit_id, comand["x"], comand["y"])

		elif comand["key"] == "split":
			self.split(unit_id, comand["give"])

	def render(self, screen):
		screen.fill(BLACK)
		units_len = font.render(str(len(self.units)), 1, WHITE, BLACK)
		screen.blit(units_len, 5, 5)

		for unit_id in self.units:
			self.units[unit_id].render_vision(screen)

		for unit_id in self.units:
			self.units[unit_id].render(screen)

		for food_id in self.food:
			self.food[food_id].render(screen)

		pygame.display.update()

	def tick(self, screen):
		for unit_id in self.units:
			comand = self.AI_types[self.units[unit_id].AI_num]['step'](self.give_data(unit_id))
			self.take_comand(unit_id, comand)

		for unit in self.borning_units:
			self.add_unit(unit)

		self.borning_units = []

	def play(self, screen):
		timer = 0
		food_spawn_timer = 0
		hunger_timer = 0
		running = True
		clock = pygame.time.Clock()

		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					continue

			if not self.units:
				print("they_survived", timer, "frames")
				running = False

			self.tick(screen)

			food_spawn_timer += 1
			hunger_timer += 1
			timer += 1
			delete_list = []

			if food_spawn_timer == self.food_spawn_cd:
				food_spawn_timer = 0
				self.add_food(Food(randint(0, self.width), randint(0, self.height)))

			if hunger_timer == self.hunger_cd:
				hunger_timer = 0

				for unit_id in self.units:
					self.units[unit_id].hp -= 1

					if self.units[unit_id].hp <= 0:
						delete_list.append(unit_id)

			for unit_id in delete_list:
				self.units.pop(unit_id)

			self.render(screen)
			clock.tick(30)

def main():
	game = Game(1, 1000, 1000)
	screen = pygame.display.set_mode((1000, 1000))

	game.play(screen)

if __name__ == '__main__':
	main()
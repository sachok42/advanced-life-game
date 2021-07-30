from random import randint
import pygame

class Unit(): 
	def __init__(self, x, y, AI_num, radius = 10, hp = 1, max_step = 10, vision_radius = 300, color = (0, 255, 0)):
		self.x = x
		self.y = y
		self.radius = radius
		self.vision_radius = vision_radius
		self.max_step = max_step
		self.AI_num = AI_num
		self.hp = hp
		self.color = color

	def move(self, x, y):
		self.x += x
		self.y += y
		# print("hey")
	
	# def Contact(self, object_): # Возвращает True если герой пересекается с объектом
	# 	if ((self.x - object_.x) ** 2 + (self.y - object_.y) ** 2) ** (1/2) <= self.radius + object_.radius:
	# 		return True
	# 	else:
	# 		return False

	def render(self, screen):
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

	def render_vision(self, screen):
		pygame.draw.circle(screen, (250, 167, 239), (self.x, self.y), self.vision_radius)

	def get_type(self):
		return "Unit"

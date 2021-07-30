import pygame

class Food():
	def __init__(self, x = 50, y = 50, radius = 5, color = (255, 0, 0)):
		self.radius = radius
		self.x = x
		self.y = y
		self.color = color

	def move(self, x, y):
		self.x = x
		self.y = y

	def get_type(self):
		return "Food"

	def render(self, screen):
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
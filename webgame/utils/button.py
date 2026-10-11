import pygame as pg

#button class
class Button():
	def __init__(self, image, button_rect: pg.Rect):
		self.image = image
		self.rect = button_rect
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pg.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			pg.draw.ellipse(surface, (255, 255, 100),self.rect, 4)
			
			if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pg.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action
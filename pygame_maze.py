import pygame
from random import choice


WIDTH, HEIGHT = 750, 750
TILE = 50

cols = (WIDTH // TILE + 1) // 2
rows = (HEIGHT // TILE + 1) // 2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze example")
clock = pygame.time.Clock()


class Cell:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
		self.visited = False

	def draw(self):
		x = 2 * self.x * TILE
		y = 2 * self.y * TILE

		if self.visited:
			pygame.draw.rect(screen, pygame.Color('red'), (x, y, TILE, TILE))

		if not self.walls['top']:
			pygame.draw.rect(screen, pygame.Color('red'), (x, y - TILE, TILE, TILE))
		if not self.walls['right']:
			pygame.draw.rect(screen, pygame.Color('red'), (x + TILE, y, TILE, TILE))
		if not self.walls['bottom']:
			pygame.draw.rect(screen, pygame.Color('red'), (x, y + TILE, TILE, TILE))
		if not self.walls['left']:
			pygame.draw.rect(screen, pygame.Color('red'), (x - TILE, y, TILE, TILE))

	def check_cell(self, x, y):
		if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
			return False
		return grid_cell[x + y * cols]

	def check_neighbours(self):
		neighbours = []

		top = self.check_cell(self.x, self.y - 1)
		right = self.check_cell(self.x + 1, self.y)
		bottom = self.check_cell(self.x, self.y + 1)
		left = self.check_cell(self.x - 1, self.y)

		if top and not top.visited:
			neighbours.append(top)
		if right and not right.visited:
			neighbours.append(right)
		if bottom and not bottom.visited:
			neighbours.append(bottom)
		if left and not left.visited:
			neighbours.append(left)

		return choice(neighbours) if neighbours else False


def remove_walls(current_cell, next_cell):
	dx = current_cell.x - next_cell.x
	dy = current_cell.y - next_cell.y

	if dx == 1:
		current_cell.walls['left'] = False
		next_cell.walls['right'] = False
	if dx == -1:
		current_cell.walls['right'] = False
		next_cell.walls['left'] = False
	if dy == 1:
		current_cell.walls['top'] = False
		next_cell.walls['bottom'] = False
	if dy == -1:
		current_cell.walls['bottom'] = False
		next_cell.walls['top'] = False

def check_wall(grid_cell, x, y):
	if x % 2 == 0 and y % 2 == 0:
		return False
	if x % 2 == 1 and y % 2 == 1:
		return True

	if x % 2 == 0:
		grid_x = x // 2
		grid_y = (y - 1) // 2
		return grid_cell[grid_x + grid_y * cols].walls['bottom']
	else:
		grid_x = (x - 1) // 2
		grid_y = y // 2
		return grid_cell[grid_x + grid_y * cols].walls['right']

grid_cell = [Cell(x, y) for y in range(rows) for x in range(cols)]
current_cell = grid_cell[0]
current_cell.visited = True
stack = []

while True:
	screen.fill(pygame.Color('black'))

	for cell in grid_cell:
		cell.draw()

	next_cell = current_cell.check_neighbours()
	if next_cell:
		next_cell.visited = True
		remove_walls(current_cell, next_cell)
		current_cell = next_cell
		stack.append(current_cell)
	elif stack:
		current_cell = stack.pop()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		if event.type == pygame.KEYDOWN:
			map_cell = [check_wall(grid_cell, x, y) for y in range(rows * 2 - 1) for x in range(cols * 2 - 1)]
			for y in range(rows * 2 - 1):
				for x in range(cols * 2 - 1):
					if map_cell[x + y * (cols * 2 - 1)]:
						print(" ", end="")
					else:
						print("#", end="")
				print()

	pygame.display.flip()
	clock.tick(30)
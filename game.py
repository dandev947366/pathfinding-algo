import pygame, sys
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

class Pathfinder:
    def __init__(self,matrix):
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        self.select_surf = pygame.image.load('selection.png').convert_alpha()
        # pathhfinding
        self.path = []
        self.roomba = pygame.sprite.GroupSingle(Roomba())
    def draw_active_cell(self):
        mouse_pos = pygame.mouse.get_pos()
        row = mouse_pos[1] // 32
        col = mouse_pos[0] // 32
        current_cell_value = self.matrix[row][col]
        if current_cell_value == 1:
            rect = pygame.Rect((col*32,row*32),(32,32))
            screen.blit(self.select_surf, rect)

        print(mouse_pos)

    def create_path(self):
        # start
        start_x, start_y = self.roomba.sprite.get_coord()
        start = self.grid.node(start_x, start_y)
        mouse_pos = pygame.mouse.get_pos()
        end_x, end_y = mouse_pos[0] // 32, mouse_pos[1] // 32
        end = self.grid.node(end_x, end_y)
        finder = AStarFinder(diagonal_movement=DiagonalMovement)
        self.path, _ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()
        self.roomba.sprite.set_path(self.path)

    def draw_path(self):
        if self.path:
            points = []
            for point in self.path:
                if isinstance(point, tuple):
                    x, y = point[0] * 32 + 16, point[1] * 32 + 16
                else:  # Handle GridNode objects
                    x, y = point.x * 32 + 16, point.y * 32 + 16
                points.append((x, y))
                pygame.draw.circle(screen, '#4a4a4a', (x,y), 2)
            pygame.draw.lines(screen, '#4a4a4a', False, points, 5)


    def update(self):
        self.draw_active_cell()
        self.draw_path()
        self.roomba.update()
        self.roomba.draw(screen)

class Roomba(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('roomba.png').convert_alpha()
        self.rect = self.image.get_rect(center=(60, 60))
        self.pos = pygame.math.Vector2(self.rect.center)  # Use Vector2 for position
        self.speed = 0.6
        self.direction = pygame.math.Vector2(0, 0)
        self.path = []

    def get_coord(self):
        col = self.rect.centerx // 32
        row = self.rect.centery // 32
        return (col, row)
    def set_path(self, path):
        self.path = path
        self.create_collision_rects()
        self.get_direction()
    def create_collision_rects(self):
        if not self.path:
            return  # Exit early if there's no path

        self.collision_rects = []
        for point in self.path:
            if isinstance(point, tuple):  # Handle tuples
                x = (point[0] * 32) + 16
                y = (point[1] * 32) + 16
            elif hasattr(point, 'x') and hasattr(point, 'y'):  # Handle GridNode or similar objects
                x = (point.x * 32) + 16
                y = (point.y * 32) + 16
            else:
                raise TypeError(f"Unsupported path point type: {type(point)}")

            rect = pygame.Rect(x - 2, y - 2, 4, 4)  # Creates a 4x4 rect centered on (x, y)
            self.collision_rects.append(rect)

    # def check_collisions(self):
	# 	if self.collision_rects:
	# 		for rect in self.collision_rects:
	# 			if rect.collidepoint(self.pos):
	# 				del self.collision_rects[0]
	# 				self.get_direction()
	# 	else:
			# self.empty_path()
    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            self.direction = (end -start).normalize()
        else:
            self.direction = pygame.math.Vector2(0,0)
            self.path = []

    def update(self):
        self.pos += self.direction * self.speed
       # self.check_collisions()
        self.rect.center = self.pos


pygame.init()
screen = pygame.display.set_mode((1280, 736))
clock = pygame.time.Clock()

bg_surf = pygame.image.load('map.png').convert()
matrix = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
	[0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,0,0,1,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
	[0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
	[0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,1,1,0,0,0],
	[0,1,1,1,1,1,0,0,1,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,1,1,0,0,0],
	[0,0,0,1,1,1,0,0,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,0],
	[0,0,0,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,0],
	[0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

pathfinder = Pathfinder(matrix)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pathfinder.create_path()
    screen.blit(bg_surf, (0,0))
    pathfinder.update()
    pygame.display.update()
    clock.tick(60)

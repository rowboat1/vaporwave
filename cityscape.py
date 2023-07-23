import pygame
import random
from curves import bezier_curve

SCREENWIDTH, SCREENHEIGHT = 1200, 900
main_s = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
vec = pygame.Vector2
HEIGHT_FACTOR_FOR_BUILDINGS = 2
MIN_BUILDING_HEIGHT = 60
SPACING_INTERVAL = 20
MIN_BUILDING_WIDTH = 30
MAX_BUILDING_WIDTH = 60
BUILDING_BOTTOMS = SCREENHEIGHT * 4/5
FOCAL_FACTOR = 0.4
FOCAL_POINT = FOCAL_FACTOR * SCREENWIDTH

MOON_1_X = 0.69 * SCREENWIDTH
MOON_1_Y = 0.08 * SCREENHEIGHT
MOON_1_SIZE = 0.04 * SCREENWIDTH

MOON_2_X = 0.32 * SCREENWIDTH
MOON_2_Y = 0.34 * SCREENHEIGHT
MOON_2_SIZE = 0.025 * SCREENWIDTH

SATURN_START = (0.14 * SCREENWIDTH, 0)
SATURN_END = (0.44 * SCREENWIDTH, 0)
SATURN_VERTEX = (0.9 * SCREENWIDTH, 0.6 * SCREENHEIGHT)

buildings = []

class Building:
    def __init__(self, x):
        h = SCREENWIDTH / 2
        k = SCREENHEIGHT / HEIGHT_FACTOR_FOR_BUILDINGS
        a  = -1 / ((SCREENWIDTH * 1.2) / 2)
        max_height = a * ((x - h) ** 2) + k
        start = BUILDING_BOTTOMS
        height = random.randrange(MIN_BUILDING_HEIGHT - 1, max(MIN_BUILDING_HEIGHT, int(max_height)))
        width = random.randrange(MIN_BUILDING_WIDTH, MAX_BUILDING_WIDTH)
        self.rect = pygame.Rect(x, start - height, width, height)
        self.offset = None

    def draw(self):
        pygame.draw.rect(main_s, "red", building.rect, 1)

class OffsetBuilding(Building):
    def __init__(self, x):
        super().__init__(x)
        while not self.offset:
            self.offset = random.randrange(-10, 10)
        self.second_rect = self.rect.copy()
        self.second_rect.topleft = self.second_rect.topleft + vec((self.offset, abs(self.offset)))

    def draw(self):
        pygame.draw.rect(main_s, "red", self.rect, 1)
        pygame.draw.rect(main_s, "red", self.second_rect, 1)
        pygame.draw.line(main_s, "red", self.rect.topleft, self.second_rect.topleft)
        pygame.draw.line(main_s, "red", self.rect.topright, self.second_rect.topright)

class AngularBuilding(Building):
    def __init__(self, x):
        super().__init__(x)
        self.angle = random.uniform(0, 1)
        print(self.rect.width)
        midpoint = self.rect.left + self.rect.width * self.angle
        self.left_polygon = (
            self.rect.bottomleft,
            self.rect.topleft + vec(0, 10),
            (midpoint, self.rect.top),
            (midpoint, self.rect.bottom)
        )
        self.right_polygon = (
            self.rect.bottomright,
            self.rect.topright + vec(0, 10),
            (midpoint, self.rect.top),
            (midpoint, self.rect.bottom)
        )
        print(self.left_polygon)

    def draw(self):
        pygame.draw.polygon(main_s, "red", self.left_polygon, 1)
        pygame.draw.polygon(main_s, "red", self.right_polygon, 1)

class Man:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        unit_size = self.rect.width / 3
        self.torso = pygame.Rect(
                self.rect.left + unit_size / 2, 
                self.rect.top + (unit_size * 2 / 3), 
                unit_size * 1.5,
                unit_size * 2.5,
        )
        arm_length = 0.75 * self.torso.height
        leg_length = 0.7 * self.torso.height
        leg_width = 0.15 * self.torso.width
        inner_leg_width = 0.5 * self.torso.width
        self.polygons = [
            [
                (self.torso.centerx - (unit_size / 3), self.rect.top),
                (self.torso.centerx + (unit_size / 3), self.rect.top),
                self.torso.midtop,
            ],
            [
                self.torso.topleft,
                (self.torso.left - unit_size * 3/4, self.torso.top + arm_length / 2),
                (self.torso.left, self.torso.top + arm_length),
                (self.torso.left, self.torso.top + arm_length - arm_length / 3),
                (self.torso.left - unit_size * 2/6, self.torso.top + arm_length / 2),
                (self.torso.left, self.torso.top + arm_length / 3)
            ],
            [
                self.torso.bottomleft,
                (self.torso.left - leg_width, self.torso.bottom + leg_length),
                (self.torso.centerx - inner_leg_width, self.torso.bottom + leg_length),
                (self.torso.centerx, self.torso.bottom)
            ],
            [
                self.torso.topright,
                (self.torso.right + unit_size * 3/4, self.torso.top + arm_length / 2),
                (self.torso.right, self.torso.top + arm_length),
                (self.torso.right, self.torso.top + arm_length - arm_length / 3),
                (self.torso.right + unit_size * 2/6, self.torso.top + arm_length / 2),
                (self.torso.right, self.torso.top + arm_length / 3)
            ],
            [
                self.torso.bottomright,
                (self.torso.right + leg_width, self.torso.bottom + leg_length),
                (self.torso.centerx + inner_leg_width, self.torso.bottom + leg_length),
                (self.torso.centerx, self.torso.bottom)
            ],
        ]

    def draw(self):
        for polygon in self.polygons:
            pygame.draw.polygon(main_s, "yellow", polygon)
        pygame.draw.rect(main_s, "yellow", self.torso)

def generate_buildings():
    generated_buildings = []
    for x in range(0, SCREENWIDTH, SPACING_INTERVAL):
        r = random.uniform(0, 1)
        if r < 0.2:
            generated_buildings.append(AngularBuilding(x))
        elif r < 0.4: 
            generated_buildings.append(OffsetBuilding(x))
        elif r < 0.6:
            pass
        else:
            generated_buildings.append(Building(x))
    return generated_buildings

buildings = generate_buildings()
persons = [
    Man(0.3 *SCREENWIDTH, 0.57 * SCREENHEIGHT, 0.14 * SCREENWIDTH, 0.2 * SCREENHEIGHT),
    Man(0.47 * SCREENWIDTH, 0.63 * SCREENHEIGHT, 0.1 * SCREENWIDTH, 0.2 * SCREENHEIGHT)
]

t = 0
while 1:
    # main_s.fill("black")
    for building in buildings:
        building.draw()
    y_start = BUILDING_BOTTOMS - 1
    pygame.draw.rect(main_s, "black", (0, y_start, SCREENWIDTH, SCREENHEIGHT - y_start))
    pygame.draw.line(main_s, "white", (0, y_start), (SCREENWIDTH, y_start), 2)
    for x in range(0, SCREENWIDTH, 50):
        front_x = FOCAL_POINT - ((FOCAL_POINT - x) * 8)
        pygame.draw.line(main_s, "blue", (x, BUILDING_BOTTOMS + 1), (front_x, SCREENHEIGHT), 2)
        
    y = y_start + 2
    i = 5
    while y < SCREENHEIGHT:
        pygame.draw.line(main_s, "blue", (0, y + i), (SCREENWIDTH, y + i), 1)
        y += i
        i *= 1.2

    if t < 10000:
        p = bezier_curve(SATURN_START, SATURN_VERTEX, SATURN_END, t / 10000)
        pygame.draw.line(main_s, "blue", vec(p), vec(p) + vec(5 + (t // 1000), 0), 1)
        t += 1

    # pygame.draw.circle(main_s, "red", SATURN_VERTEX, 5)

    for person in persons:
        person.draw()
    pygame.draw.circle(main_s, "grey", (MOON_1_X, MOON_1_Y), MOON_1_SIZE)
    pygame.draw.circle(main_s, "white", (MOON_2_X, MOON_2_Y), MOON_2_SIZE)


    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_r:
                main_s.fill("black")
                t = 0
                buildings = generate_buildings()

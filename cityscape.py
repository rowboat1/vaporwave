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

SHADOW_MATRIX_1 = [[1, -0.75], [0, -0.5]]
SHADOW_MATRIX_2 = [[1, -1.7], [0, -0.4]]

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

class Person:
    def __init__(self, x, y, unit_size, shadow_matrix):
        arm_length = 1.875 * unit_size
        leg_length = 1.75 * unit_size
        leg_width = 0.225 * unit_size
        inner_leg_width = 0.75 * unit_size
        origin = vec(x, y)
        self.rect = pygame.Rect(
            x - unit_size / 2 + leg_width, 
            y - unit_size * 3.1666 - leg_length, 
            unit_size * 3,
            unit_size * 6
        )
        self.torso = pygame.Rect(
            x + leg_width, 
            y - (leg_length + unit_size * 2.5), 
            unit_size * 1.5,
            unit_size * 2.5,
        )
        # This is the left side of the left leg.
        self.polygon = [
            # Left leg
                origin,
                (self.torso.centerx - inner_leg_width, self.torso.bottom + leg_length),
                (self.torso.centerx, self.torso.bottom),
            # Right leg
                (self.torso.centerx, self.torso.bottom),
                (self.torso.centerx + inner_leg_width, self.torso.bottom + leg_length),
                (self.torso.right + leg_width, self.torso.bottom + leg_length),
            # Right arm
                self.torso.bottomright,
                # Armpit
                (self.torso.right, self.torso.top + arm_length / 3),
                # Elbow inner
                (self.torso.right + unit_size * 2/6, self.torso.top + arm_length / 2),
                # hand inner
                (self.torso.right, self.torso.top + arm_length - arm_length / 3),
                # hand outer
                (self.torso.right, self.torso.top + arm_length),
                # Elbow outer
                (self.torso.right + unit_size * 3/4, self.torso.top + arm_length / 2),
                # Shoulder
                self.torso.topright,
                self.torso.midtop,
            # Head
                (self.torso.centerx - (unit_size / 3), self.rect.top),
                (self.torso.centerx + (unit_size / 3), self.rect.top),
                self.torso.midtop,
            # Left arm
                self.torso.topleft,
                # Elbow outer
                (self.torso.left - unit_size * 3/4, self.torso.top + arm_length / 2),
                # Hand outer
                (self.torso.left, self.torso.top + arm_length),
                # Hand inner
                (self.torso.left, self.torso.top + arm_length - arm_length / 3),
                # Elbow inner
                (self.torso.left - unit_size * 2/6, self.torso.top + arm_length / 2),
                # Armpit
                (self.torso.left, self.torso.top + arm_length / 3),
                self.torso.bottomleft,
        ]
        transformable_map = map(lambda point: vec(point) - origin, self.polygon)
        mapped = map(lambda p: vec(
            p[0] * shadow_matrix[0][0] + p[1] * shadow_matrix[0][1], 
            p[0] * shadow_matrix[1][0] + shadow_matrix[1][1] * p[1]
        ), transformable_map)
        self.shadow = list(map(lambda p: origin + p, mapped))

    def draw(self):
        pygame.draw.polygon(main_s, "yellow", self.polygon)
        pygame.draw.polygon(main_s, "yellow", self.shadow, width=1)
        # pygame.draw.rect(main_s, "yellow", self.torso)

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
    Person(0.3128 *SCREENWIDTH, 0.8759 * SCREENHEIGHT, 0.04667 * SCREENWIDTH, SHADOW_MATRIX_1),
    Person(0.47917 * SCREENWIDTH, 0.8485 * SCREENHEIGHT, 0.03333 * SCREENWIDTH, SHADOW_MATRIX_2)
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
    pygame.draw.circle(main_s, (255, 255, 180), (MOON_1_X, MOON_1_Y), MOON_1_SIZE)
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

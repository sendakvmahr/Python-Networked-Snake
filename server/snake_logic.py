# Width and height are set in client, just remember to change it here too if I change it
import random
import json # not sure if that should be done here atm

WIDTH = 750
HEIGHT = 500
STEP_SIZE = 10
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

def to_nearest_tile(x):
    base_tile = int(x/STEP_SIZE)
    remainder = x % STEP_SIZE
    return (base_tile * STEP_SIZE) + (STEP_SIZE if remainder >= STEP_SIZE/2 else 0)

class Snake():
    def __init__(self, player, headx, heady, direction):
        self.head = [headx, heady]
        self.tail = []
        self.player = player
        self.direction = ()
        self.ate = False
        self.update_direction(direction)
    def update(self):
        if (self.ate):
            # If it grew, add an extra tail piece. Doesn't matter where the tail is initialized,
            # It will move to the right place before collision checking is done
            self.tail.append([0,0])
            self.ate = False
        if (len(self.tail) > 0):
            # Take out the coordinate corresponding to the last tail bit, 
            # stick a new coordinate where the head is
            self.tail.pop()
            self.tail.insert(0, list(self.head))
        # Move the head 
        self.head = [self.head[0] + STEP_SIZE * self.direction[0], self.head[1] + STEP_SIZE * self.direction[1]]
    def update_direction(self, direction):
        if (direction == "r"):
            self.direction = RIGHT
        elif (direction == "l"):
            self.direction = LEFT
        elif (direction == "u"):
            self.direction = UP
        else:
            self.direction = DOWN
    def get_draw_tails(self):
        return list(tuple(t) for t in self.tail)
    def get_head(self):
        return list(self.head)
    
class Game_State():
    def __init__(self, players):
        self.finished = False
        self.num_players = len(players)
        self.players = {}
        if (self.num_players == 1):
            self.players[players[0]] = Snake(players[0], to_nearest_tile(WIDTH/2), to_nearest_tile(HEIGHT/2), "r")
        if (self.num_players >= 2):
            self.players[players[0]] = Snake(players[0], to_nearest_tile(WIDTH/4), to_nearest_tile(HEIGHT/2), "r")
            self.players[players[1]] = Snake(players[1], to_nearest_tile(WIDTH*3/4), to_nearest_tile(HEIGHT/2), "l")
        if (self.num_players >= 3):
            self.players[players[2]] = Snake(players[2], to_nearest_tile(WIDTH/2), to_nearest_tile(HEIGHT/4), "d")
        if (self.num_players == 4):
            self.players[players[3]] = Snake(players[2], to_nearest_tile(WIDTH/2), to_nearest_tile(HEIGHT*3/4), "d")
        self.food = []
        self.spawn_food()
    def update(self):
        dead_snakes = []
        tails = []
        # Move snakes
        for snake in self.players.values():
            snake.update()
            tails += snake.get_draw_tails()
        # Check to see if snake heads are in anything
        # Really lazy collision detection - everything is done in multiples of 10
        for snake in self.players.values():
            head = snake.get_head()
            if ((head in tails)) or (self.in_wall(head)):
                # Snake hit a tail or wall, is dead
                dead_snakes.append(snake.player)
            elif (head == self.food[0]):
                snake.ate = True
                self.food.pop()
        for snake in dead_snakes:
            # Delete dead players
            del self.players[snake]
        if (len(self.food) == 0):
            self.spawn_food()
        if (len(self.players) == 1):
            # Last one staying wins
            self.finished = True
            
    def in_wall(self, head):
        x_collide = head[0] == 0 or head[0] == WIDTH
        y_collide = head[1] == 0 or head[1] == HEIGHT
        return x_collide or y_collide

    def update_player_direction(self, player, direction):
        self.players[player].update_direction(direction)

    def spawn_food(self):
        # Extra calculations involving STEP_SIZE prevent food from spawning in borders
        food_x = to_nearest_tile(random.randint(STEP_SIZE, WIDTH - STEP_SIZE * 2))
        food_y = to_nearest_tile(random.randint(STEP_SIZE, HEIGHT - STEP_SIZE * 2))
        self.food.append([food_x, food_y])

    def to_JSON(self):
        # Should be in another module in the future
        drawSnakes = []
        snakeHeads = {}
        score = {}
        for snake in self.players.values():
            tails = snake.get_draw_tails(),
            drawSnakes += tails,
            snakeHeads[snake.player] = snake.get_head(),
            score[snake.player] = len(tails)
        
        return json.dumps({"drawSnakes" : drawSnakes,
                           "snakeHeads" : snakeHeads,
                           "score" : score,
                           "drawFood" : self.food[0]
                         })


if (__name__ == "__main__"):
    # Used pygame for visuals to make sure logic worked
    import pygame, sys
    #pygame.init()
    clock = pygame.time.Clock()
    #py_display = pygame.display.set_mode([WIDTH, HEIGHT])
    #gs = Game_State(["player1", "player2", "player3", "player4"])
    gs = Game_State(["player1", "player2"])
    #gs = Game_State(["player1"])
    def draw_rect(x, y, color):
        # assume size 10 cause increments of 10
        pygame.draw.rect(py_display, color ,(x, y, 10, 10))
    def display(state):
        py_display.fill((100, 33, 33))
        for s in gs.players.values():
            draw_rect(s.head[0], s.head[1], (100, 255, 100))
            for t in s.get_draw_tails():
                draw_rect(t[0], t[1], (255, 255, 255))
        for f in gs.food:
            draw_rect(f[0], f[1], (100, 100, 255))
        pygame.display.flip()
    gs.update()
    print(gs.to_JSON())
        
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                pressed = pressed = pygame.key.get_pressed()
                # Cruddy input but it's not that important, the game works
                if (pressed[pygame.K_UP]):
                    gs.update_player_direction("player1", "u")
                if (pressed[pygame.K_DOWN]):
                    gs.update_player_direction("player1", "d")
                if (pressed[pygame.K_RIGHT]):
                    gs.update_player_direction("player1", "r")
                if (pressed[pygame.K_LEFT]):
                    gs.update_player_direction("player1", "l")
                if (pressed[pygame.K_w]):
                    gs.update_player_direction("player2", "u")
                if (pressed[pygame.K_s]):
                    gs.update_player_direction("player2", "d")
                if (pressed[pygame.K_d]):
                    gs.update_player_direction("player2", "r")
                if (pressed[pygame.K_a]):
                    gs.update_player_direction("player2", "l")
        gs.update()
        display(gs)
        clock.tick(16)
        """




# Game_State.width and Game_State.height are set in client, just remember to change it here too if I change it
import random
import json # not sure if that should be done here atm

class Snake():
    left = (-1, 0)
    right = (1, 0)
    up = (0, -1)
    down = (0, 1)
    def __init__(self, player, headx, heady, direction):
        self.head = [headx, heady]
        self.tail = []
        self.player = player
        self.direction = ()
        self.ate = False
        self.update_direction(direction)
    def update(self, step_size):
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
        self.head = [self.head[0] + step_size * self.direction[0], self.head[1] + step_size * self.direction[1]]
    def update_direction(self, direction):
        if (direction == "r"):
            self.direction = Snake.right
        elif (direction == "l"):
            self.direction = Snake.left
        elif (direction == "u"):
            self.direction = Snake.up
        else:
            self.direction = Snake.down
    def get_draw_tails(self):
        result = list(tuple(t) for t in self.tail)
        result.append(tuple(self.get_head()))
        return result
    def get_head(self):
        return list(self.head)
    
class Game_State():
    width = 750
    height = 500
    step_size = 10
    def __init__(self, players):
        self.finished = False
        self.num_players = len(players)
        self.players = {}
        if (self.num_players == 1):
            self.players[players[0]] = Snake(players[0], self.to_nearest_tile(Game_State.width/2), self.to_nearest_tile(Game_State.height/2), "r")
        if (self.num_players >= 2):
            self.players[players[0]] = Snake(players[0], self.to_nearest_tile(Game_State.width/4), self.to_nearest_tile(Game_State.height/2), "r")
            self.players[players[1]] = Snake(players[1], self.to_nearest_tile(Game_State.width*3/4), self.to_nearest_tile(Game_State.height/2), "l")
        if (self.num_players >= 3):
            self.players[players[2]] = Snake(players[2], self.to_nearest_tile(Game_State.width/2), self.to_nearest_tile(Game_State.height/4), "d")
        if (self.num_players == 4):
            self.players[players[3]] = Snake(players[2], self.to_nearest_tile(Game_State.width/2), self.to_nearest_tile(Game_State.height*3/4), "d")
        self.food = []
        self.spawn_food()
    def update(self):
        if not (self.finished):
            dead_snakes = []
            tails = []
            # Move snakes
            for snake in self.players.values():
                snake.update(Game_State.step_size)
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
        x_collide = head[0] == 0 or head[0] == Game_State.width
        y_collide = head[1] == 0 or head[1] == Game_State.height
        return x_collide or y_collide

    def update_player_direction(self, player, direction):
        self.players[player].update_direction(direction)

    def spawn_food(self):
        # Extra calculations involving STEP_SIZE prevent food from spawning in borders
        food_x = self.to_nearest_tile(random.randint(Game_State.step_size, Game_State.width - Game_State.step_size * 2))
        food_y = self.to_nearest_tile(random.randint(Game_State.step_size, Game_State.height - Game_State.step_size * 2))
        self.food.append([food_x, food_y])

    def to_nearest_tile(self, x):
        base_tile = int(x/Game_State.step_size)
        remainder = x % Game_State.step_size
        return (base_tile * Game_State.step_size) + (Game_State.step_size if remainder >= Game_State.step_size/2 else 0)

    def to_JSON(self):
        # Should be in another module in the future
        drawSnakes = []
        snakeHeads = {}
        score = {}
        for snake in self.players.values():
            tails = snake.get_draw_tails()
            drawSnakes += tails
            snakeHeads[snake.player] = snake.get_head()
            score[snake.player] = len(tails)-1
            # tails -1 b/c snake counts as a drawHead
        
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
    #py_display = pygame.display.set_mode([Game_State.width, Game_State.height])
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




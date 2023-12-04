import turtle
import random
import math


class ScreenManager:
    def __init__(self, width, height, title, bgcolor):
        self.screen = turtle.Screen()
        self.screen.setup(width, height)
        self.screen.title(title)
        self.screen.bgcolor(bgcolor)
        self.screen.tracer(0)

    def update_screen(self):
        self.screen.update()

    def register_shape(self, shape):
        self.screen.register_shape(shape)

    def set_key_bindings(self, player_movement_manager):
        self.screen.listen()
        self.screen.onkey(lambda: player_movement_manager.move_player("left"), "Left")
        self.screen.onkey(lambda: player_movement_manager.move_player("right"), "Right")
        self.screen.onkey(lambda: player_movement_manager.move_player("up"), "Up")
        self.screen.onkey(lambda: player_movement_manager.move_player("down"), "Down")

    def end_game(self):
        self.screen.bye()


class Wall(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.original_color = "gray"  # Storing the original color
        self.color(self.original_color)
        self.penup()
        self.speed(0)

    def flash(self, flash_color="yellow", times=3, duration=200):
        self._flash(flash_color, times, True, duration)

    def _flash(self, flash_color, times, state, duration):
        if times > 0:
            if state:
                self.color(flash_color)
            else:
                self.color(self.original_color)
            turtle.ontimer(lambda: self._flash(flash_color, times - int(not state), not state, duration), duration)
        else:
            self.restore_original_state()  # Call the method to restore the original state

    def change_color(self, color):
        self.color(color)

    def is_touching(self, other_obj):
        # Basic distance check to determine if touching another object
        return self.distance(other_obj) < 24  # Assuming a grid size of 24

    def restore_original_state(self):
        self.color("gray")
        self.showturtle()
        self.shapesize(1, 1)  # Reset to original size


class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("jucator.gif")
        self.penup()
        self.speed(0)
        self.award = 0
        self.key = False
        self.life = 300

    # The player has 4 possible directions which are implemented below; the condition implemented
    # for each direction does not allow the player to go through the walls
    def go_up(self):
        # Calculate the spot to move to
        move_to_x = player.xcor()
        move_to_y = player.ycor() + 24

        # Check if the space has a wall or a door
        if (move_to_x, move_to_y) not in walls and (move_to_x, move_to_y) not in doors:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        # Calculate the spot to move to
        move_to_x = player.xcor()
        move_to_y = player.ycor() - 24

        # Check if the space has a wall or a door
        if (move_to_x, move_to_y) not in walls and (move_to_x, move_to_y) not in doors:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        # Calculate the spot to move to
        move_to_x = player.xcor() + 24
        move_to_y = player.ycor()

        # Check if the space has a wall or a door
        if (move_to_x, move_to_y) not in walls and (move_to_x, move_to_y) not in doors:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        # Calculate the spot to move to
        move_to_x = player.xcor() - 24
        move_to_y = player.ycor()

        # Check if the space has a wall or a door
        if (move_to_x, move_to_y) not in walls and (move_to_x, move_to_y) not in doors:
            self.goto(move_to_x, move_to_y)

    # Check if the player touches another object
    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 5:
            return True
        else:
            return False

    # Check if the player is next to another object
    def is_next(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 27:
            return True
        else:
            return False

    def update_status(self, score_increment=0, life_decrement=0):
        self.award += score_increment
        self.life -= life_decrement
        print(f"Player Status - Score: {self.award}, Life: {self.life}")


class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("comoara.gif")
        self.penup()
        self.speed(0)
        self.award = 1000
        self.goto(x, y)

    # The function which remove the treasure from the screen
    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

    def hide_temporarily(self):
        self.hideturtle()
        turtle.ontimer(self.show, 7000)  # Schedule the show method to be called after 10 seconds

    def show(self):
        self.showturtle()


class Key(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("cheie.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.door_bound_to = None  # Initially, the key is not bound to any door

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

    def is_picked_up(self, player_instance):
        return self.distance(player_instance) < 20

    @staticmethod
    def display_pickup_message():
        print("You have picked up a key!")


class Door(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("usa.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y)

    # The function which remove the door from the screen
    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

    def x(self):
        return self.xcor()

    def y(self):
        return self.ycor()


class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("monstru.gif")
        self.penup()
        self.speed(0)
        self.life = 20
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])  # The enemy is moving randomly

    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24

        elif self.direction == "down":
            dx = 0
            dy = -24

        elif self.direction == "left":
            dx = -24
            dy = 0

        elif self.direction == "right":
            dx = 24
            dy = 0

        else:
            dx = 0
            dy = 0

        # Calculate the spot to move to
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        # Check if the space has a wall, door or exit
        if ((move_to_x, move_to_y) not in walls and (move_to_x, move_to_y) not in doors
                and (move_to_x, move_to_y) not in exits):
            self.goto(move_to_x, move_to_y)
        else:
            # Choose a different direction
            self.direction = random.choice(["up", "down", "left", "right"])

        # Set timer to move next time
        turtle.ontimer(self.move, t=random.randint(100, 300))


class Exit(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("cyan")
        self.penup()
        self.speed(0)
        self.goto(x, y)

    # The function which remove the exit from the screen
    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


class PlayerMovementManager:
    def __init__(self, player_instance, walls_instance, doors_instance):
        self.player = player_instance
        self.walls = walls_instance
        self.doors = doors_instance

    def move_player(self, direction):
        move_functions = {
            'up': self._move_up,
            'down': self._move_down,
            'left': self._move_left,
            'right': self._move_right
        }
        move_func = move_functions.get(direction)
        if move_func:
            move_func()

    def _move_up(self):
        self._move(0, 24)

    def _move_down(self):
        self._move(0, -24)

    def _move_left(self):
        self._move(-24, 0)

    def _move_right(self):
        self._move(24, 0)

    def _move(self, dx, dy):
        new_x = self.player.xcor() + dx
        new_y = self.player.ycor() + dy
        if (new_x, new_y) not in self.walls and (new_x, new_y) not in self.doors:
            self.player.goto(new_x, new_y)


class CollisionManager:
    def __init__(self):
        self.collision_logging_enabled = False

    def is_collision(self, obj1, obj2):
        distance = self._calculate_distance(obj1, obj2)
        return distance < 5

    def is_next_to(self, obj1, obj2):
        distance = self._calculate_distance(obj1, obj2)
        return distance < 27

    @staticmethod
    def _calculate_distance(obj1, obj2):
        a = obj1.xcor() - obj2.xcor()
        b = obj1.ycor() - obj2.ycor()
        return math.sqrt((a ** 2) + (b ** 2))

    def detect_enemy_collision(self, player_instance, enemies_instance):
        for enemy_instance in enemies_instance:
            if self.is_collision(player_instance, enemy_instance):
                print("Collision with enemy detected.")
                return True
        return False

    def detect_treasure_collision(self, player_instance, treasures_instance):
        for treasure_instance in treasures_instance:
            if self.is_collision(player_instance, treasure_instance):
                print("Collision with treasure detected.")
                return True
        return False

    def detect_key_collision(self, player_instance, keys_instance):
        for key_instance in keys_instance:
            if self.is_collision(player_instance, key_instance):
                print("Collision with key detected.")
                return True
        return False


class MazeBuilder:
    def __init__(self, maze_layout):
        self.maze_layout = maze_layout
        self.walls = []
        self.doors = []
        self.enemies = []
        self.treasures = []
        self.keys = []
        self.closed_doors = []
        self.exits = []

    def build_maze(self):
        for y, row in enumerate(self.maze_layout):
            for x, char in enumerate(row):
                screen_x = -288 + (x * 24)
                screen_y = 288 - (y * 24)
                self.process_maze_element(char, screen_x, screen_y)

        return self.walls, self.doors

    def process_maze_element(self, char, x, y):
        if char == "X":
            self.create_wall(x, y)
        elif char == "D":
            self.create_door(x, y)
        elif char == "P":
            player.goto(x, y)
        elif char == "T":
            self.create_treasure(x, y)
        elif char == "E":
            self.create_enemy(x, y)
        elif char == "K":
            self.create_key(x, y)
        elif char == "O":
            self.create_exit(x, y)

    def create_wall(self, x, y):
        wall.goto(x, y)
        wall.stamp()
        self.walls.append((x, y))

    def create_door(self, x, y):
        door_instance = Door(x, y)
        self.closed_doors.append(door_instance)
        self.doors.append((x, y))

    def create_treasure(self, x, y):
        treasure_instance = Treasure(x, y)
        self.treasures.append(treasure_instance)

    def create_enemy(self, x, y):
        enemy_instance = Enemy(x, y)
        self.enemies.append(enemy_instance)

    def create_key(self, x, y):
        key_instance = Key(x, y)
        self.keys.append(key_instance)

    def create_exit(self, x, y):
        exit_instance = Exit(x, y)
        self.exits.append(exit_instance)


# Initialize the screen manager
screen_manager = ScreenManager(700, 700, "MAZE", "black")

# Register shapes (images)
screen_manager.register_shape("comoara.gif")
screen_manager.register_shape("jucator.gif")
screen_manager.register_shape("monstru.gif")
screen_manager.register_shape("usa.gif")
screen_manager.register_shape("cheie.gif")

# Define the appearance of the maze
maze = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP  XXXXXXE         XXXXX",
    "X   XXXXXX  XXXXXX  XXXXX",
    "X       XX  XXXXXXDDXXXXX",
    "X       XX  XXX       EXX",
    "XXXXXX  XX  XXX        XX",
    "XXXXXX  XX  XXXXXX  XXXXX",
    "XXXXXX  XX    XXXX  XXXXX",
    "X KXXX        XXXX TXXXXX",
    "X  XXX  XXXXXXXXXXXXXXXXX",
    "X         XXXXXXXXXXXXXXX",
    "X                XXXXXXXX",
    "XXXXXXXXXXXX     XXXXX  X",
    "XXXXXXXXXXXXXXX  XXXXX  X",
    "XXX  XXXXXXXXXX  XXXXX  X",
    "XXX                     X",
    "XXX         XXXXXXXXXXXXX",
    "XXXXXXXXXX  XXXXXXXXXXXXX",
    "XXXXXXXXXX              X",
    "XX   XXXXX E            X",
    "XX   XXXXXXXXXXXXX  XXXXX",
    "XX    YXXXXXXXXXXXDDXXXXX",
    "XX          XXXX        X",
    "XXXX                    O",
    "XXXXXXXXXXXXXXXXXXXXXXXXX"
]

treasures = []  # Create a treasure list
keys = []  # Create a key list
closed_doors = []  # Create a closed door list
exits = []  # Create an exit list

# Create class instances
wall = Wall()
player = Player()

# Setup Maze Builder
maze_builder = MazeBuilder(maze)
walls, doors = maze_builder.build_maze()

# Create Movement and Collision Managers
movement_manager = PlayerMovementManager(player, walls, doors)
collision_manager = CollisionManager()

screen_manager.set_key_bindings(movement_manager)

# Start moving enemies
enemies = maze_builder.enemies  # Assuming enemies list is populated in MazeBuilder
for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

for treasure in maze_builder.treasures:
    treasure.hide_temporarily()

# Main Game Loop
while True:
    # Check for player collision with treasure
    for treasure in maze_builder.treasures:
        if collision_manager.detect_treasure_collision(player, maze_builder.treasures):
            player.update_status(score_increment=treasure.award)
            treasure.destroy()
            maze_builder.treasures.remove(treasure)

            # Flash all walls in the maze
            for wall_location in maze_builder.walls:
                wall_to_flash = Wall()
                wall_to_flash.goto(wall_location[0], wall_location[1])
                wall_to_flash.flash()

    # Check for player collision with key
    for key in maze_builder.keys:
        if key.is_picked_up(player):
            key.display_pickup_message()  # Display a message in the console
            player.key = True  # Update player's status to having the key
            key.destroy()  # Remove the key from the screen
            maze_builder.keys.remove(key)  # Remove the key from the list

        if collision_manager.detect_key_collision(player, maze_builder.keys):
            player.key = True
            key.destroy()
            maze_builder.keys.remove(key)

    # Check for player proximity to door
    for door in maze_builder.closed_doors:
        if collision_manager.is_next_to(player, door) and player.key:
            doors.remove((door.x(), door.y()))
            maze_builder.closed_doors.remove(door)
            door.destroy()

    # Check for player collision with enemy
    for enemy in enemies:
        if collision_manager.detect_enemy_collision(player, maze_builder.enemies):
            player.update_status(life_decrement=enemy.life)
            if player.life == 0:
                turtle.color("blue")
                style = ("Courier", 80, "bold")
                turtle.write("YOU DIED", font=style, align="center")
                turtle.done()
            else:
                # Flash walls red when the player touches an enemy
                for wall_location in maze_builder.walls:
                    wall_to_flash = Wall()
                    wall_to_flash.goto(wall_location[0], wall_location[1])
                    wall_to_flash.flash(flash_color="red")

    # Check for player collision with exit
    for exit_obj in maze_builder.exits:
        if collision_manager.is_collision(player, exit_obj):
            exit_obj.destroy()
            maze_builder.exits.remove(exit_obj)
            turtle.color("blue")
            style = ("Courier", 30, "bold")
            turtle.write("YOU WIN!!! $ gained: " + str(player.award), font=style, align="center")
            turtle.done()

    # Update Screen
    screen_manager.update_screen()

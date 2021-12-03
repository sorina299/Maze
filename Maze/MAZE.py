import turtle # A useful python module to create a graphical interface to our program
import math # This module includes mathematical expressions
import random # This module implements pseudo-random number generators for various distributions

# Create a window with different features
my_window = turtle.Screen()
my_window.setup(700, 700)
my_window.bgcolor("black")
my_window.title("MAZE")
my_window.tracer(0) # Turn off screen updates

# Adding images for our elements in the maze
turtle.register_shape("comoara.gif")
turtle.register_shape("jucator.gif")
turtle.register_shape("monstru.gif")
turtle.register_shape("usa.gif")
turtle.register_shape("cheie.gif")

##########################################################################################################################################################################

# All the classes use the turtle module which means that everything a turtle can do, our class will do the same
# Create the Wall Class
class Wall(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("gray")
        self.penup()
        self.speed(0)

##########################################################################################################################################################################

#Create the Player Class
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

##########################################################################################################################################################################

# Create the Treasure Class
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

##########################################################################################################################################################################

# Create the Key Class
class Key(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("cheie.gif")
        self.penup()
        self.speed(0)
        self.award = 1000
        self.goto(x, y)

    # The function which remove the key from the screen
    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

##########################################################################################################################################################################

# Create the Door Class
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

##########################################################################################################################################################################

# Create the Enemy Class
class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("monstru.gif")
        self.penup()
        self.speed(0)
        self.life = 20
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"]) # The enemy is moving randomly

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
        if(move_to_x, move_to_y) not in walls and (move_to_x, move_to_y) not in doors and (move_to_x, move_to_y) not in exits:
            self.goto(move_to_x, move_to_y)
        else:
            # Choose a different direction
            self.direction = random.choice(["up", "down", "left", "right"])

        # Set timer to move next time
        turtle.ontimer(self.move, t=random.randint(100, 300))

##########################################################################################################################################################################

# Create the Exit Class
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

##########################################################################################################################################################################

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

walls = []# Create a wall coordinate list
treasures = [] # Create a treasure list
keys = [] # Create a key list
enemies = [] # Create an enemy list
closed_doors = [] # Create a closed door list
doors = [] # Create a door list
exits = [] # Create an exit list

# Create the maze
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            # Get the character at each x,y coordinate
            # Note the order of the y and x in the next line
            character = level[y][x]

            # Calculate the screen x, y coordinates
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            # Check if it is an X (representing a wall)
            if character == "X":
                wall.goto(screen_x, screen_y)
                wall.stamp()
                # Add coordinates to wall list
                walls.append((screen_x, screen_y))

            # Check if it is a D (representing a door)
            if character == "D":
                closed_doors.append(Door(screen_x, screen_y))
                doors.append((screen_x, screen_y))

            # Check if it is a P (representing the player)
            if character == "P":
                player.goto(screen_x, screen_y)

            # Check if it is a T (representing a treasure)
            if character == "T":
                treasures.append(Treasure(screen_x, screen_y))

            # Check if it is an E (representing an enemy)
            if character == "E":
                enemies.append(Enemy(screen_x, screen_y))

            # Check if it is a K (representing a key)
            if character == "K":
                keys.append(Key(screen_x, screen_y))

            # Check if it is an O (representing the exit)
            if character == "O":
                exits.append(Exit(screen_x, screen_y))



# Create class instances
wall = Wall()
player = Player()

# Set up the maze
setup_maze(maze)

# Keyboard Binding
turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")

# Start moving enemies 
for enemy in enemies:
    turtle.ontimer(enemy.move, t = 250)

# Main Game Loop
while True:
    # Check for player collision with treasure
    # Iterate through treasure list
    for treasure in treasures:
        if player.is_collision(treasure):
            player.award = player.award + treasure.award # Add the treasure gold to the player gold
            treasure.destroy() # Make the treasure disappear
            treasures.remove(treasure) # Remove the treasure from the treasure list

    # Check for player collision with key
    # Iterate through key list
    for key in keys:
        if player.is_collision(key):
            player.key = True # Add the key to player's items for future usage
            key.destroy() # Make the key disappear
            keys.remove(key) # Remove the key from the key list
            
    # Check for player proximity to door
    # Iterate through closed door list
    for door in closed_doors:
        if player.is_next(door) and player.key == True:
            doors.remove((door.x(), door.y()))  
            closed_doors.remove(door) 
            door.destroy() # Make the door disappear

    # Check for player collision with enemy
    # Iterate through enemy list
    for enemy in enemies:
        if player.is_collision(enemy):
            # The player's life decreases by a constant value if he touches the enemy
            player.life = player.life - enemy.life
            print("The player has" + str(player.life) + "life")
            # If player's life becomes 0 you lost the game
            if player.life == 0:
                turtle.color("blue")
                style = ("Courier", 80, "bold")
                turtle.write("YOU DIED", font = style, align = "center")
                turtle.done()

    # Check for player collision with exit
    # Iterate through exit list
    for exit in exits:
        if player.is_collision(exit):
            exit.destroy() 
            exits.remove(exit) 
            turtle.color("blue")
            style = ("Courier", 30, "bold")
            turtle.write("YOU WIN!!! $ gained:" + str(player.award), font = style, align = "center")      
            turtle.done() # stop the Turtle 


    # Update Screen
    my_window.update()

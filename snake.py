import setup_data as sd


class Snake:

    def __init__(self, x, y):
        self.width = 10
        self.height = 10

        self.x = x
        self.y = y

        self.x_range = range(0, sd.WIDTH)
        self.y_range = range(0, sd.HEIGHT)

        self.color = sd.SNAKE_COLOR  # red
        self.step = sd.STEP

        self.last_move = 'right'  # the snake stars moving right
        self.moves = [self.last_move]

        self.is_head = True

        if self.is_head:
            self.tail = []  # Appended with a new snake if an apple was eaten

    def move_up(self):
        self.y -= self.step
        self.last_move = 'up'

    def move_down(self):
        self.y += self.step
        self.last_move = 'down'

    def move_right(self):
        self.x += self.step
        self.last_move = 'right'

    def move_left(self):
        self.x -= self.step
        self.last_move = 'left'

    @staticmethod
    def opposite_direction(direction):

        opposite = {
            'up': 'down',
            'down': 'up',
            'right': 'left',
            'left': 'right'
        }

        return opposite.get(direction)

    def move(self, direction):

        # The snake can't immediately change its direction to the opposite side
        if direction != self.opposite_direction(self.last_move):

            if direction == 'up':
                self.move_up()

            elif direction == 'down':
                self.move_down()

            elif direction == 'right':
                self.move_right()

            elif direction == 'left':
                self.move_left()

            self.moves.append(direction)
            self.move_tail()

        elif self.is_head:
            self.move(self.last_move)

    def move_tail(self):

        if self.tail:
            index = -2
            current_last_move = self.moves[index]

            # Every snake in the tail repeats the way of the snake spawned before it
            for i in range(len(self.tail)):
                snake = self.tail[i]
                snake.move(current_last_move)
                current_last_move = snake.moves[index]

    def eat(self, food):

        food_x_range = range(food.x, food.x + food.width)
        food_y_range = range(food.y, food.y + food.width)

        # Checking if the snake has the same coordinates as an apple
        if self.x in food_x_range and self.y in food_y_range:
            food.get_eaten()

            # Creating a new snake - a part of the main snake's tail
            snake = self if not self.tail else self.tail[-1]

            new_x, new_y = snake.x, snake.y
            delta = self.step

            if snake.last_move == 'up':
                new_y += delta

            elif snake.last_move == 'down':
                new_y -= delta

            elif snake.last_move == 'right':
                new_x -= delta

            elif snake.last_move == 'left':
                new_x += delta

            new_snake = Snake(new_x, new_y)
            new_snake.last_move = snake.last_move
            new_snake.moves = [snake.last_move]
            new_snake.is_head = False

            self.tail.append(new_snake)

    def ate_itself(self):
        """Checks if the snake ate itself"""

        if self.tail:
            for snake in self.tail:
                if self.x == snake.x and self.y == snake.y:
                    return True

        return False

    def in_border(self):
        return self.x in self.x_range and self.y in self.y_range

    def is_alive(self):
        return not self.ate_itself() and self.in_border()

from random import randrange
import setup_data as sd


class Food:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Food is spawned randomly with step of width at x axis and height at y axis, so the snake can perfectly fit it
        self.x = randrange(self.width, sd.WIDTH - self.width + 1, self.width)
        self.y = randrange(self.height * 10, sd.HEIGHT - self.height + 1, self.height)  # * 10 so it doesn't spawn
        # at the score and help label

        self.color = sd.FOOD_COLOR  # green
        self.eaten = False

    def get_eaten(self):
        self.eaten = True

    @staticmethod
    def spawn_big_food():

        # A big apple is twice bigger than the regular one
        w, h = sd.FOOD_WIDTH * 2, sd.FOOD_HEIGHT * 2
        big_apple = Food(w, h)

        return big_apple

import pygame as pg
import setup_data as sd
from snake import Snake
from food import Food


pg.init()

# Screen setup
screen = pg.display.set_mode(sd.SIZE)
pg.display.set_caption("Snake game")

score_list = []  # Keeps track of all the scores


def game():
    running = True
    paused = False

    score = 0  # counts all the eaten apples

    # Creating both snake and an apple
    snake = Snake(sd.WIDTH // 2, sd.HEIGHT // 2)
    apple = Food(sd.FOOD_WIDTH, sd.FOOD_HEIGHT)

    while running:
        pg.time.delay(sd.TIME_DELAY)

        # Spawning a new random apple on the screen and increasing the score if the previous apple was eaten
        if apple.eaten:

            # A big apple gives 3 points instead of 1
            if apple.width > sd.FOOD_WIDTH:
                score += 3
            else:
                score += 1

            # Spawning a big apple every 10 times
            if score % 10 == 0:
                apple = apple.spawn_big_food()
            else:
                apple = Food(sd.FOOD_WIDTH, sd.FOOD_HEIGHT)

        # Exiting the gamer if user clicks the "quit" button
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            # Pause
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if paused:
                    paused = False
                else:
                    paused = True

        # Snake movement (only if game is not paused)
        keys = pg.key.get_pressed()

        if not paused:
            if keys[pg.K_UP] or keys[pg.K_w]:
                snake.move('up')

            elif keys[pg.K_DOWN] or keys[pg.K_s]:
                snake.move('down')

            elif keys[pg.K_RIGHT] or keys[pg.K_d]:
                snake.move('right')

            elif keys[pg.K_LEFT] or keys[pg.K_a]:
                snake.move('left')
            else:
                snake.move(snake.last_move)

        # Checking if the snake's head or tail went out the border or the snake ate itself
        if not snake.is_alive() or any(not i.is_alive() for i in snake.tail):
            running = False

        # Eating the apple if it's possible
        snake.eat(apple)

        # Filling the screen with black so the snake's previous positions aren't displayed
        screen.fill(sd.BLACK)

        # Displaying both snake and food
        pg.draw.rect(screen, snake.color, (snake.x, snake.y, snake.width, snake.height))
        pg.draw.rect(screen, apple.color, (apple.x, apple.y, apple.width, apple.height))

        # Displaying the snake's tail
        for i in snake.tail:
            pg.draw.rect(screen, sd.SNAKE_COLOR, (i.x, i.y, snake.width, snake.height))

        # Creating a label displaying the score
        font = pg.font.SysFont(sd.FONT, sd.FONT_SIZE)

        score_label = font.render(f"Score: {score}", True, sd.LABEL_COLOR)
        help_label = font.render("space - pause", True, sd.LABEL_COLOR)

        screen.blit(score_label, sd.FONT_COORDINATES)
        screen.blit(help_label, (sd.WIDTH - 200, 10))

        # Updating the display
        pg.display.update()

    score_list.append(score)


# Game over window with labels representing game stats and other stuff
def game_over():
    running = True

    while running:
        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False

            # Restarting the game if space bar is pressed
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                game()

        screen.fill(sd.BLACK)

        # Text of every label
        text = ["Game over", f"Final score: {score_list[-1]}", f"Best score: {max(score_list)}",
                "Thanks for playing :)",
                "Press down the space bar to play again..."]

        # Displaying all the labels
        for i, params in enumerate(sd.PARAMS):
            color, font_size, coordinates = params

            font = pg.font.SysFont(sd.FONT, font_size)
            label = font.render(text[i], True, color)

            screen.blit(label, coordinates)

        pg.display.update()


def main():
    game()
    game_over()


if __name__ == '__main__':
    main()

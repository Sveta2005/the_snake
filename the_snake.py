from random import choice, randint

import pygame as pg

"""Константы для размеров поля и сетки."""
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE


"""Направления движения."""
POINTER = tuple[int, int]
UP: POINTER = (0, -1)
DOWN: POINTER = (0, 1)
LEFT: POINTER = (-1, 0)
RIGHT: POINTER = (1, 0)
DEFAULT_OCCUPIED = []
"""Цвет фона - черный."""
COLOR = tuple[int, int, int]
BOARD_BACKGROUND_COLOR: COLOR = (0, 0, 0)
DEFAULT_COLOR: COLOR = BOARD_BACKGROUND_COLOR
"""Цвет границы ячейки."""
BORDER_COLOR: COLOR = (93, 216, 228)

"""Цвет яблока."""
APPLE_COLOR: COLOR = (255, 0, 0)

"""Цвет змейки."""
SNAKE_COLOR: COLOR = (0, 255, 0)

"""Скорость движения змейки."""
SPEED: int = 20

"""Настройка игрового окна."""
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

"""Заголовок окна игрового поля."""
pg.display.set_caption('Змейка')

"""Настройка времени."""
clock = pg.time.Clock()


class GameObject:
    """Базовый класс, общие атрибуты(позиция, цвет объекта)."""

    def __init__(self, body_color: COLOR = DEFAULT_COLOR) -> None:
        self.position: POINTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self) -> None:
        """Метод для переопредения в дочерних классах,
        отрисовка объекта на поле.
        """
        raise NotImplementedError()


class Snake(GameObject):
    """Змейка и ее поведение."""

    def __init__(self, body_color: COLOR = SNAKE_COLOR) -> None:
        super().__init__(body_color=body_color)
        self.length: int = 1
        self.positions: list[tuple[int, int]] = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.direction_new = tuple(20 * elem for elem in self.direction)
        self.last: tuple[int, int] = self.position

    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.direction_new = tuple(20 * elem for elem in self.direction)
            self.next_direction = None

    def move(self) -> None:
        """Обновление положения змейки."""
        x, y = self.get_head_position()
        new_head: tuple[int, int] = (
            (self.direction_new[0] + x) % SCREEN_WIDTH,
            (self.direction_new[1] + y) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        DEFAULT_OCCUPIED.append(new_head)

    def draw(self) -> None:
        """Отрисовка змейки."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        """Отрисовка головы змейки."""
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        """Затирание последнего сегмента."""
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> POINTER:
        """Получение текущей головной позиции."""
        return self.positions[0]

    def reset(self) -> None:
        """Сброс змейки в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None


class Apple(GameObject):
    """Яблоко и действия с ним."""

    def __init__(
            self, snake_positions=DEFAULT_OCCUPIED,
            body_color: COLOR = APPLE_COLOR) -> None:
        super().__init__(body_color=body_color)
        self.snake_positions = snake_positions
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions) -> None:
        """Определить рандомное положение яблока."""
        while True:
            width: int = randint(0, GRID_WIDTH) * GRID_SIZE
            height: int = randint(0, GRID_HEIGHT) * GRID_SIZE
            self.position: tuple[int, int] = width, height
            if (width, height) not in snake_positions:
                break

    def draw(self) -> None:
        """Отрисовка яблока."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object) -> None:
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Сама игра."""
    pg.init()
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.move()
        snake.update_direction()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(DEFAULT_OCCUPIED)
            apple.draw()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        pg.display.update()


if __name__ == '__main__':
    main()

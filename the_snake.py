from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """базовый класс, общие атрибуты(позиция, цвет объекта)"""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """метод для переопредения в дочерних классах,
        отрисовка объекта на поле
        """
        pass


class Snake(GameObject):
    """змейка и ее поведение"""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.body_color = SNAKE_COLOR
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT  # направление движения
        self.next_direction = None  # направление после нажатия
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """обновление положения змейки"""
        x, y = self.get_head_position()  # координаты x и y текущей головы
        direction__multiply = tuple(20 * elem for elem in self.direction)
        new_head = (
            (direction__multiply[0] + x) % SCREEN_WIDTH,
            (direction__multiply[1] + y) % SCREEN_HEIGHT
        )  # новая позиция головы
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """отрисовывает змейку"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """получение текущей головной позиции"""
        return self.positions[0]

    def reset(self):
        """сброс в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None


class Apple(GameObject):
    """яблоко и действия с ним, отображ в рандомной клетке"""

    def __init__(self):
        self.randomize_position()  # яблоко в случайном месте
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """определить рандомное положение яблока"""
        width = randint(0, GRID_WIDTH) * GRID_SIZE
        height = randint(0, GRID_HEIGHT) * GRID_SIZE
        self.position = width, height
        
    # Метод draw класса Apple
    def draw(self):
        """отрисовать яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """обновление состояния"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    while True:   # Тут опишите основную логику игры.
        clock.tick(SPEED)  # изменение положения не более 20 раз/сек
        apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.move()
        snake.update_direction()
        if snake.get_head_position() == apple.position:
            # проверить съела ли яблоко
            snake.length += 1
            apple.randomize_position()
            apple.draw()
            
        if snake.get_head_position() in snake.positions[1:]:
            # столкновение с собой(если да, то reset)
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        pygame.display.update()
        
        

if __name__ == '__main__':
    main()

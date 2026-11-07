import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
RED = (220, 20, 60)


class Goal:
    def __init__(self):
        self.box = pygame.Rect(150, 70, 500, 200)

        self.image = pygame.image.load(
            "goal.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image, self.box.size
        )

        # This smaller box is the area where goals count.
        self.score_area = pygame.Rect(
            190, 105, 420, 140
        )

    def is_goal(self, ball):
        return self.score_area.collidepoint(
            ball.box.center
        )

    def draw(self, screen):
        screen.blit(self.image, self.box)


class Goalkeeper:
    def __init__(self):
        self.box = pygame.Rect(
            340, 140, 120, 105
        )

        self.image = pygame.image.load(
            "goalkeeper.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image, self.box.size
        )

        self.speed = 6

    def move(self, goal):
        self.box.x += self.speed

        if self.box.left <= goal.score_area.left:
            self.box.left = goal.score_area.left
            self.speed = -self.speed

        elif self.box.right >= goal.score_area.right:
            self.box.right = goal.score_area.right
            self.speed = -self.speed

    def catches(self, ball):
        return self.box.colliderect(ball.box)

    def get_faster(self):
        if self.speed > 0:
            self.speed += 1
        else:
            self.speed -= 1

    def reset(self):
        self.box.x = 340
        self.speed = 6

    def draw(self, screen):
        screen.blit(self.image, self.box)


class Ball:
    def __init__(self):
        self.box = pygame.Rect(
            378, 478, 45, 45
        )

        self.image = pygame.image.load(
            "ball.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image, self.box.size
        )

        self.start_x = 400
        self.start_y = 500

        self.reset()

    def shoot(self, mouse_position):
        if self.is_shot:
            return

        mouse_x = mouse_position[0]

        self.speed_x = (
            mouse_x - self.x
        ) / 25

        self.speed_y = -12
        self.is_shot = True

    def move(self):
        if self.is_shot:
            self.x += self.speed_x
            self.y += self.speed_y

            self.box.center = (
                int(self.x),
                int(self.y),
            )

    def has_missed(self):
        return (
            self.box.bottom < 0
            or self.box.left > WIDTH
            or self.box.right < 0
        )

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y

        self.speed_x = 0
        self.speed_y = 0
        self.is_shot = False

        self.box.center = (
            self.start_x,
            self.start_y,
        )

    def draw(self, screen):
        screen.blit(self.image, self.box)


class Scoreboard:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont(
            "arial", 25, bold=True
        )

    def increase(self):
        self.score += 1

    def reset(self):
        self.score = 0

    def draw(self, screen):
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            WHITE,
        )

        screen.blit(score_text, (20, 20))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption(
            "Python Mini Cup"
        )

        self.clock = pygame.time.Clock()

        self.goal = Goal()
        self.goalkeeper = Goalkeeper()
        self.ball = Ball()
        self.scoreboard = Scoreboard()

        self.game_over = False
        self.running = True

        self.game_over_font = pygame.font.SysFont(
            "arial", 35, bold=True
        )

    def restart(self):
        self.ball.reset()
        self.goalkeeper.reset()
        self.scoreboard.reset()
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
                and self.game_over
            ):
                self.restart()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.restart()
                else:
                    self.ball.shoot(event.pos)

    def update(self):
        if self.game_over:
            return

        self.goalkeeper.move(self.goal)
        self.ball.move()

        if (
            self.ball.is_shot
            and self.goalkeeper.catches(self.ball)
        ):
            self.ball.is_shot = False
            self.game_over = True

        elif (
            self.ball.is_shot
            and self.goal.is_goal(self.ball)
        ):
            self.scoreboard.increase()
            self.goalkeeper.get_faster()
            self.ball.reset()

        elif (
            self.ball.is_shot
            and self.ball.has_missed()
        ):
            self.ball.is_shot = False
            self.game_over = True

    def draw(self):
        self.screen.fill(GREEN)

        self.goal.draw(self.screen)
        self.goalkeeper.draw(self.screen)
        self.ball.draw(self.screen)
        self.scoreboard.draw(self.screen)

        if (
            not self.ball.is_shot
            and not self.game_over
        ):
            pygame.draw.line(
                self.screen,
                WHITE,
                self.ball.box.center,
                pygame.mouse.get_pos(),
                2,
            )

        if self.game_over:
            message = self.game_over_font.render(
                "GAME OVER - Click or press R",
                True,
                RED,
            )

            message_box = message.get_rect(
                center=(400, 350)
            )

            self.screen.blit(
                message,
                message_box,
            )

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()


game = Game()
game.run()
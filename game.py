import pygame
from settings import *
from hand_tracking import HandTracking

# TODO: Colocar limitadores de chão e teto no objeto
# TODO: Colocar uma força da gravidade que contraria o movimento de subida
# TODO: Refazer todo a movimentação do bloco

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.set_screen()
        self.active = False
        self.running = True

        self.starting_y = HEIGHT-40
        self.target_y = 0
        self.player_x = 50
        self.player_y = self.starting_y

        self.speed_constant = SPEED_CONSTANT
        self.gravity = GRAVITY

        # Ruler dimensions and positioning
        self.ruler_width = 30
        self.ruler_height = HEIGHT
        self.ruler_x = 0
        self.ruler_y = 0

        self.remaining_time = 30
        self.score = 0

    def set_screen(self):
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption('Blocos escaladores')
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.timer = pygame.time.Clock()

    def _instruction_text(self):
        # show texts before starting game 
        instruction_text = self.font.render(f'Pressione espaço para começar', True, WHITE, BLACK)
        self.screen.blit(instruction_text, (200, 50))
        instruction_text_2 = self.font.render(f'Feche a sua mão para subir o bloco', True, WHITE, BLACK)
        self.screen.blit(instruction_text_2, (200, 100))

    def _points_text(self):
        self.score = int(100 - (self.player_y / 560) * 100)
        score_text = self.font.render(f'Score: {self.score}', True, WHITE, BLACK)
        self.screen.blit(score_text, (200, 150))

    def _redraw_objects(self):
        # Objects that are redraw every frame
        floor = pygame.draw.rect(self.screen, WHITE, [0, HEIGHT-18, WIDTH, 40])
        player = pygame.draw.rect(self.screen, GREEN, [self.player_x, self.player_y, 100, 20])
        ruler = pygame.draw.rect(self.screen, WHITE, (self.ruler_x, self.ruler_y, self.ruler_width, self.ruler_height))
        # Ruler marks
        for i in range(0, self.ruler_height, 20):
            pygame.draw.line(self.screen, BLACK, (self.ruler_x, self.ruler_y + i), (self.ruler_x + self.ruler_width, self.ruler_y + i), 2)

    def _user_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.active:
                        # Restart game
                        self.active = True
                        self.start_time = pygame.time.get_ticks()
                        self.player_y = self.starting_y

    def _timer_text(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        self.remaining_time = max(TIMER - int(elapsed_time / 1000), 0)
        countdown_text = self.font.render(str(self.remaining_time), True, WHITE)
        self.screen.blit(countdown_text, (200, 200))

    def _move_player(self, m_finger_y, palm_base_y):
        distance_hand = m_finger_y - palm_base_y
        up_multiplier = 1 - abs(distance_hand)
        dist_helper = (self.player_y - 0) // DIST_CONSTANT
        movement = -(up_multiplier * self.speed_constant + dist_helper) + self.gravity
        self.player_y += movement

    def _fix_player(self):
        if self.player_y > self.starting_y:
            self.player_y = self.starting_y
        if self.player_y < self.target_y:
            self.player_y = self.target_y

    def fix_fps(self):
        self.timer.tick(FPS)

    def update(self, m_finger_y, palm_base_y):
        self.screen.fill(BACKGROUND)
        if not self.active:
            self._instruction_text()

        self._points_text()
        self._redraw_objects()

        self._user_events()
        if self.active:
            self._timer_text()
            self._move_player(m_finger_y, palm_base_y)

        self._fix_player()
        
        pygame.display.flip()
        # self.fix_fps()

if __name__ == "__main__":
    hand_track = HandTracking()
    game = Game()
    while game.running:
        m_finger_y, palm_base_y = hand_track.scan_hands()
        game.update(m_finger_y, palm_base_y)
        hand_track.show_camera()

        if game.active and hand_track.hands_detected:
            hand_track.build_frame()

        if game.remaining_time == 0 and game.active:
            game.active = False
            hand_track.save(game.score)
        
        game.fix_fps()

    pygame.quit()
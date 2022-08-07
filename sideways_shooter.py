import pygame, sys
from time import sleep
import random
from settings import Settings
from ship import Ship
from bullet import Bullet
from meteor import Meteor
from stats import Stats
from scoreboard import ScoreBoard
from button import Button


class SidewaysShooter:
    '''Overall class to manage game assets and behavior.'''
    def __init__(self):

        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Sideways Shooter")
        self.bg_surface = pygame.image.load(self.settings.bg_path)
        self.screen.blit(pygame.transform.scale(self.bg_surface, (1280,720)), (0,0))

        self.stats = Stats(self)
        self.sb = ScoreBoard(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.meteors = pygame.sprite.Group()

        self._create_meteors()

        self.play_button = Button(self, "Play")
        self._make_difficulty_buttons()
        
    def run(self):
        '''Run game.'''
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_meteors()

            self.update_screen()

    def _make_difficulty_buttons(self):
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium")
        self.hard_button = Button(self, "Hard")

        self.easy_button.rect.top = self.play_button.rect.top + 2* self.easy_button.rect.height
        self.easy_button.rect.left = self.play_button.rect.left - 400
        self.easy_button._update_msg_position()

        self.medium_button.rect.top = self.play_button.rect.top + 2* self.medium_button.rect.height
        self.medium_button._update_msg_position()

        self.hard_button.rect.top = self.play_button.rect.top + 2* self.hard_button.rect.height
        self.hard_button.rect.right = self.play_button.rect.right + 400
        self.hard_button._update_msg_position()

    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                    self._check_dificulty_buttons(mouse_pos)
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        button_clicked =  self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self._start_game()

    def _check_dificulty_buttons(self, mouse_pos):
        easy_button_clicked =  self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked =  self.medium_button.rect.collidepoint(mouse_pos)
        hard_button_clicked =  self.hard_button.rect.collidepoint(mouse_pos)

        if easy_button_clicked:
            self.settings.difficulty_level = "easy"
            print("easy")
        elif medium_button_clicked:
            self.settings.difficulty_level = "medium"
            print("medium")
        elif hard_button_clicked:
            self.settings.difficulty_level = "hard"
            print("hard")

    def _start_game(self):
        self.stats.reset_stats()
        self.stats.game_active = True
        
        self.sb.prep_score()
        self.sb.prep_lvl()
        self.sb.prep_ships()

        self.meteors.empty()
        self.bullets.empty()

        self._create_meteors()
        self.ship.center_ship()

        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        # Start game
        elif event.key == pygame.K_p:
            self._start_game()
        # Pause game
        elif event.key == pygame.K_s:
            self.stats.game_active = False
        elif event.key == pygame.K_UP:
            self.ship.ship_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.ship_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_UP:
            self.ship.ship_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.ship_down = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
                if bullet.rect.left >= self.screen_rect.right:
                    self.bullets.remove(bullet)
        self._bullet_meteor_collision()

    def _bullet_meteor_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.meteors, True, True)
        if  collisions:
            # Update score.
            for meteors in collisions.values():
                self.stats.score += self.settings.meteor_points * len(meteors)
            self.sb.prep_score()
            self.sb.check_high_score()
        if  not self.meteors:
            # Make new meteors and delete the old bullets.
            self.bullets.empty()
            self._create_meteors()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_lvl()

    def _create_meteors(self):
        '''Create a meteor shower.'''
        #Find the number of meteors in a column.
        meteor = Meteor(self)
        meteor_width, meteor_height = meteor.rect.size
        avalible_space_y = self.settings.screen_height - 4* meteor_height
        num_meteors_y = avalible_space_y // (3* meteor_height)
        #print(num_meteors_y)

        # Find number of columns.
        ship_width = self.ship.rect.width
        avalible_space_x = 2 * self.screen_rect.width + 2* meteor_width - 4*ship_width
        num_columns =  avalible_space_x // (3*meteor_width)
        #print(meteor_width)
        #print(avalible_space_x)
        #print(num_columns)

        # Create meteor shower.
        for column in range(num_columns):
            for meteor_num in range(num_meteors_y):
                self._create_single_meteor(meteor_num, column)

    def _create_single_meteor(self,meteor_num, column):
        '''Create meteor and place it in row.'''
        meteor = Meteor(self)
        meteor_width, meteor_height = meteor.rect.size
        meteor.y = random.randint(50, 250) + 3* meteor_height * meteor_num
        meteor.rect.y = meteor.y

        meteor.rect.x = 13 * self.ship.rect.width +(2* meteor_width * column) + random.randint(0,220)
        self.meteors.add(meteor)

    def _update_meteors(self):
        self.meteors.update()
        for meteor in self.meteors.copy():
            if meteor.rect.right <= self.screen_rect.left:
                self.meteors.remove(meteor)
        #print(len(self.meteors))

        # Detect ship-meteor collisions.
        if pygame.sprite.spritecollideany(self.ship, self.meteors):
            self.ship_hitted()

    def ship_hitted(self):
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.meteors.empty()
            self.bullets.empty()
            self._create_meteors()
            self.ship.center_ship()
            sleep(0.1)
        else:
            self.sb.prep_ships()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def update_screen(self):
        self.screen.blit(pygame.transform.scale(self.bg_surface, (1280,720)), (0,0))
        self.ship.blit_player()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.meteors.draw(self.screen)
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

        pygame.display.flip()
                
S1 = SidewaysShooter()
S1.run()
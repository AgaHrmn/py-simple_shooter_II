
class Settings():
    '''Class to magane game's static settings'''
    def __init__(self):

        # screen
        self.bg_path = r"python_crash_course\part_2\pygame_excercises\sideways_shooter\images\bg_image.png"
        self.screen_width = 1280
        self.screen_height = 720

        # ship
        self.ship_limit = 3

        # bullets
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (250,250,250)
        self.bullets_allowed = 7

        # scale
        self.speed_scale = 1.1
        self.points_scale = 1.5

        self.difficulty_level = "medium"

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        if self.difficulty_level == "easy":
            self.ship_limit = 5
            self.bullets_allowed = 15
            self.ship_speed = 1
            self.bullet_speed = 3
            self.meteor_speed = -0.3
        elif self.difficulty_level == "medium":
            self.ship_limit = 3
            self.bullets_allowed = 10
            self.ship_speed = 2
            self.bullet_speed = 4
            self.meteor_speed = -1.5
        if self.difficulty_level == "hard":
            self.ship_limit = 2
            self.bullets_allowed = 5
            self.ship_speed = 3
            self.bullet_speed = 5
            self.meteor_speed = -2

        self.meteor_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speed_scale
        self.bullet_speed *= self.speed_scale
        self.meteor_speed *= self.speed_scale
        self.meteor_points = int(self.points_scale * self.meteor_points)

    def set_difficulty(self, diff_setting):
        if diff_setting == "easy":
            print("easy")
        if diff_setting == "medium":
            pass
        if diff_setting == "hard":
            pass
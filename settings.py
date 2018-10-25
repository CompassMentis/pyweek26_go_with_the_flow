class Settings:
    width = 1600
    height = 900
    turn_angle = 5
    speed_increase = 0.2
    maximum_speed = 2

    @property
    def size(self):
        return self.width, self.height


settings = Settings()

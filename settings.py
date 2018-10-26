class Settings:
    width = 1600
    map_width = 1410
    height = 900
    turn_angle = 1
    speed_increase = 0.03
    maximum_speed = 3

    @property
    def size(self):
        return self.width, self.height


settings = Settings()

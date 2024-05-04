class Snowflake:
    def __init__(self, x, y, vertical_speed, horizontal_speed, snowflake_id):
        self.x = x
        self.y = y
        self.vertical_speed = vertical_speed
        self.horizontal_speed = horizontal_speed
        self.state = "falling"
        self.snowflake_id = snowflake_id

    def fall(self):
        if self.state == "falling":
            self.y += self.vertical_speed
            self.x += self.horizontal_speed
            if self.x <= 0 or self.x >= 1600:
                self.horizontal_speed = -self.horizontal_speed
        elif self.state == "disintegrating":
            self.vertical_speed -= 0.1
            self.y += self.vertical_speed
            self.x += self.horizontal_speed
            if self.vertical_speed <= 0:
                self.state = "disintegrated"


    def draw(self, screen, snowflake_image):
        screen.blit(snowflake_image, (self.x, self.y))

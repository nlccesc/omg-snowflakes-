class Snowflake:
    def __init__(self, x, y, vertical_speed, horizontal_speed, snowflake_id):
        self.x = x
        self.y = y
        self.vertical_speed = vertical_speed
        self.horizontal_speed = horizontal_speed
        self.state = "falling"
        self.snowflake_id = snowflake_id  # Unique identifier for each snowflake

    def fall(self):
        # Update the position of the snowflake based on its speed
        self.y += self.vertical_speed
        self.x += self.horizontal_speed
        if self.x <= 0 or self.x >= 1600:
            self.horizontal_speed = -self.horizontal_speed  # Bounce off the edges

        # Transition to disintegrating state based on vertical position
        if self.y >= 1200 or self.state == "disintegrating":
            self.vertical_speed -= 0.1
            if self.vertical_speed <= 0:
                self.state = "disintegrated"

    def draw(self, screen, snowflake_image):
        # Draw the snowflake at its current position
        screen.blit(snowflake_image, (self.x, self.y))

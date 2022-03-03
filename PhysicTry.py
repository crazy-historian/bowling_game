import arcade
import pymunk
import timeit
import math

screen_width = 1280
screen_height = 720
screen_title = "physic ball"


class PhysicsSprite(arcade.Sprite):
    def __init__(self, pymunk_shape, file):
        super().__init__(file, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.pymunk_shape = pymunk_shape


class CircleSprite(PhysicsSprite):
    def __init__(self, pymunk_shape, file):
        super().__init__(pymunk_shape, file)
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2


class BoxSprite(PhysicsSprite):
    def __init__(self, pymunk_shape, file, width, height):
        super().__init__(pymunk_shape, file)
        self.width = width
        self.height = height


class MyPhysic(arcade.View):

    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.GO_GREEN)

        self.space = pymunk.Space()
        self.space.iterations = 35
        self.space.gravity = (0.0, -900.0)

        self.sprite_list: arcade.SpriteList[PhysicsSprite] = arcade.SpriteList()
        self.static_lines = []

        self.shape_being_dragged = None
        self.last_mouse_position = 0, 0
        self.draw_time = 0
        self.processing_time = 0

        floor_height = 80
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, [0, floor_height], [screen_width, floor_height], 0.0)
        shape.friction = 10
        self.space.add(shape, body)
        self.static_lines.append(shape)

        for row in range(10):
            for column in range(10):
                size = 32
                mass = 100.0
                x = 500 + column * 32
                y = (floor_height + size / 2) + row * size
                moment = pymunk.moment_for_box(mass, (size, size))
                body = pymunk.Body(mass, moment)
                body.position = pymunk.Vec2d(x, y)
                shape = pymunk.Poly.create_box(body, (size, size))
                shape.elasticity = 0.2
                shape.friction = 0.9
                self.space.add(body, shape)

                sprite = BoxSprite(shape, ":resources:images/tiles/boxCrate_double.png", width=size, height=size)
                self.sprite_list.append(sprite)

    def on_draw(self):
        self.clear()

        draw_start_time = timeit.default_timer()

        self.sprite_list.draw()

        for line in self.static_lines:
            body = line.body

            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            arcade.draw_line(pv1.x, pv1.y, pv2.x, pv2.y, arcade.color.WHITE, 2)

        output = f"Processing time: {self.processing_time:.3f}"
        arcade.draw_text(output, 20, screen_height - 20, arcade.color.WHITE, 12)

        self.draw_time = timeit.default_timer() - draw_start_time

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.last_mouse_position = x, y

            shape_list = self.space.point_query((x, y), 1, pymunk.ShapeFilter())

            if len(shape_list) > 0:
                self.shape_being_dragged = shape_list[0]

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            mass = 60
            radius = 30
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            body.position = x, y
            body.velocity = 10, 10
            shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
            shape.friction = 1
            self.space.add(body, shape)

            sprite = CircleSprite(shape, "images/ball.png")
            self.sprite_list.append(sprite)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.shape_being_dragged = None

    def on_mouse_motion(self, x, y, dx, dy):
        if self.shape_being_dragged is not None:
            self.last_mouse_position = x, y
            self.shape_being_dragged.shape.body.position = self.last_mouse_position
            self.shape_being_dragged.shape.body.velocity = dx * 20, dy * 20

    def on_update(self, delta_time):
        start_time = timeit.default_timer()

        for sprite in self.sprite_list:
            if sprite.pymunk_shape.body.position.y < 0:
                self.space.remove(sprite.pymunk_shape, sprite.pymunk_shape.body)
                sprite.remove_from_sprite_lists()

        self.space.step(1/60.0)
        if self.shape_being_dragged is not None:
            self.shape_being_dragged.shape.body.position = self.last_mouse_position
            self.shape_being_dragged.shape.body.velocity = 0, 0

        for sprite in self.sprite_list:
            sprite.center_x = sprite.pymunk_shape.body.position.x
            sprite.center_y = sprite.pymunk_shape.body.position.y
            sprite.angle = math.degrees(sprite.pymunk_shape.body.angle)

        self.processing_time = timeit.default_timer() - start_time


def main():
    window = arcade.Window(screen_width, screen_height, screen_title)
    start_view = MyPhysic()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
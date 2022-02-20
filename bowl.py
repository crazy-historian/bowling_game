# 1 нужно прописать менюшку
# сделать одну для преподавателя,1 для ученика
import arcade
import time
import arcade.gui
import json

screen_width = 1280
screen_height = 720
title = "Bowling Game"

# Загружаем наш файл в переменную data
with open('task.json', 'r', encoding='utf-8') as modes:
    data = {}
    data.update(json.load(modes))


# Класс главного меню игры
class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        # цвет фона
        arcade.set_background_color(arcade.color.GOLD)
        # выравнивание кнопок
        self.v_box = arcade.gui.UIBoxLayout()
        #  кнопка студента
        student_button = arcade.gui.UIFlatButton(text="Режим ученика", width=200)
        student_button.on_click = self.on_click_student
        self.v_box.add(student_button.with_space_around(bottom=20))
        # кнопка преподавателя
        teacher_button = arcade.gui.UIFlatButton(text="Режим преподавателя", width=200)
        teacher_button.on_click = self.on_click_teacher
        self.v_box.add(teacher_button.with_space_around(bottom=20))
        # кнопка выхода
        quit_button = QuitButton(text="Закрыть", width=200)
        self.v_box.add(quit_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_student(self, event):
        game_view = BowlGameView()
        self.window.show_view(game_view)

    def on_click_teacher(self, event):
        game = Teacher_View()
        self.window.show_view(game)

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()


# Класс кнопки выхода
class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


# Класс интерфейса преподавателя
class Teacher_View(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.DENIM)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Режим преподавателя", self.window.width / 2, self.window.height / 2, arcade.color.WHITE,
                         font_size=20, anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.TAB:
            start_view = MainMenuView()
            self.window.show_view(start_view)
        elif symbol == arcade.key.ESCAPE:
            arcade.close_window()


# Класс паузы
class PauseView(arcade.View):
    def __init__(self, game_view, width):
        super().__init__()
        self.game_view = game_view
        self.width = width

    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Пауза", self.width / 2, screen_height / 2 + 50, arcade.color.BLACK, font_size=30,
                         anchor_x="center")
        arcade.draw_text("Нажмите ENTER чтоб вернуться", self.width / 2, screen_height / 2, arcade.color.BLACK,
                         font_size=20, anchor_x="center")
        arcade.draw_text("Нажмите ESC чтоб закрыть", self.width / 2, screen_height / 2 - 30, arcade.color.BLACK,
                         font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game = BowlGameView()
            self.window.show_view(game)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
        if key == arcade.key.TAB:
            start_view = MainMenuView()
            self.window.show_view(start_view)


# Класс победы
class WinView(arcade.View):
    def __init__(self, width):
        super().__init__()
        self.width = width

    def on_show(self):
        arcade.set_background_color(arcade.color.GOLD)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Поздравляю уровень пройден", self.width / 2, screen_height / 2 + 50, arcade.color.WHITE,
                         font_size=30, anchor_x="center")
        arcade.draw_text("Чтобы продолжить нажмите ENTER", self.width / 2, screen_height / 2, arcade.color.WHITE,
                         font_size=20, anchor_x="center")

    def on_key_press(self, symbol: int, modifers: int):
        if symbol == arcade.key.ENTER:
            game = BowlGameView()
            self.window.show_view(game)
        elif symbol == arcade.key.ESCAPE:
            arcade.close_window()


# Класс поражения
class GameOverviewView(arcade.View):
    def __init__(self, width):
        super().__init__()
        self.width = width

    def on_show(self):
        arcade.set_background_color(arcade.color.TEA_ROSE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Попробуй ещё раз", self.width / 2, screen_height / 2 + 50, arcade.color.WHITE,
                         font_size=30, anchor_x="center")
        arcade.draw_text("Нажмите ENTER", self.width / 2, screen_height / 2, arcade.color.WHITE,
                         font_size=20, anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            game_view = BowlGameView()
            self.window.show_view(game_view)
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()


# Класс самой игры
class BowlGameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.pressed = None
        arcade.set_background_color(arcade.color.BROWN)
        self.mode = data
        # задаем длину дорожки по файлу
        if self.mode["length"] == "long":
            self.screen_width = 1280
        elif self.mode["length"] == "middle":
            self.screen_width = 1024
        elif self.mode["length"] == "short":
            self.screen_width = 768
        # здесь задаем по нашему файлу количество кеглей n
        if self.mode["powered"] == "middle":
            self.n = 6
        elif self.mode["powered"] == "hard":
            self.n = 9
        elif self.mode["powered"] == "easy":
            self.n = 3
        arcade.get_window().set_size(self.screen_width, screen_height)
        self.player = Player(self.screen_width)
        self.ball = Ball(self.screen_width)
        self.pin_list = pin_list(self.screen_width, self.n)

    def on_draw(self):
        arcade.start_render()
        # рисуем дорожку
        arcade.draw_lrtb_rectangle_filled(0, screen_width, screen_height / 2.5, 0, arcade.color.WOOD_BROWN)
        # рисуем аут
        arcade.draw_lrtb_rectangle_filled(0, screen_width, 50, 0, arcade.color.BLACK)
        # иконка персонажа
        self.player.draw()
        # иконка шара
        self.ball.draw()
        # Отрисовываем кегли
        self.pin_list.on_draw()

    def on_update(self, delta_tie):
        pass
        # self.player.update(self.pressed)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
        if symbol == arcade.key.TAB:
            start_view = MainMenuView()
            self.window.show_view(start_view)
        if symbol == arcade.key.ENTER:
            pause = PauseView(self, self.screen_width)
            self.window.show_view(pause)
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.pressed = "D"
        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.pressed = "A"
        if symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.pressed = "S"
        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.pressed = "W"

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.D or _symbol == arcade.key.RIGHT:
            self.pressed = None
        if _symbol == arcade.key.A or _symbol == arcade.key.LEFT:
            self.pressed = None
        if _symbol == arcade.key.S or _symbol == arcade.key.DOWN:
            self.pressed = None
        if _symbol == arcade.key.W or _symbol == arcade.key.UP:
            self.pressed = None


class Player(arcade.Sprite):
    def __init__(self, width_p):
        super().__init__("images/player.png", 0.3, center_x=width_p / 6, center_y=screen_height / 2)


class Ball(arcade.Sprite):
    def __init__(self, width_b):
        super().__init__("images/ball.png", 0.2, center_x=width_b / 4, center_y=screen_height / 3)


class pin_list(arcade.SpriteList):
    def __init__(self, width_pin, n):
        super().__init__()
        self.x = width_pin - 100
        self.y = screen_height - 400
        self.n = n
        self.pin_list = arcade.SpriteList()

        for i in range(0, self.n):
            pin = arcade.Sprite("images/pin.png", 0.2, center_x=self.x, center_y=self.y)
            self.pin_list.append(pin)
            if i < 2:
                self.x -= 50
            elif i < 4:
                self.x += 50
            elif i < 5:
                self.y += 150
            elif i == 6:
                self.x += 50
            elif i > 7:
                self.x = self.x
            else:
                self.y += 100
            self.y -= 50

    def on_draw(self):
        self.pin_list.draw()


def main():
    window = arcade.Window(screen_width, screen_height, title)
    start_view = MainMenuView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()

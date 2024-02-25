import glfw
from engine import Drawable, Window, key_callback_decorator, Rectangle


class DrawLab1(Drawable):
    delta = 2
    stop_rotating = 0
    moving_step = 0.05
    angle = 0.0
    angle2 = 0.0
    pos_x = 0.0
    pos_y = 0.0
    size = 1
    size_step = 0.1
    eps = 10 ** (-6)

    def draw(self):
        # Сначала переместим объект к целевой точке
        self.move_to(self.pos_x, self.pos_y, 0)

        # Изменение размера объекта
        self.scale(self.size, self.size, 200)

        # Затем выполним поворот вокруг оси Z
        self.rotate(self.angle, 0, 0, 1)

        self.angle += self.delta * self.stop_rotating

    @key_callback_decorator
    def key_callback(self, states):
        if states.get(glfw.KEY_MINUS):
            if self.size - self.size_step > self.eps:
                self.size -= self.size_step
        if states.get(glfw.KEY_EQUAL):
            self.size += self.size_step
        if states.get(glfw.KEY_RIGHT) and self.delta > 0:
            self.delta = -self.delta
        if states.get(glfw.KEY_LEFT) and self.delta < 0:
            self.delta = -self.delta
        if states.get(glfw.KEY_SPACE):
            self.stop_rotating ^= 1
        if states.get(glfw.KEY_S):
            self.pos_y -= self.moving_step
        if states.get(glfw.KEY_W):
            self.pos_y += self.moving_step
        if states.get(glfw.KEY_D):
            self.pos_x += self.moving_step
        if states.get(glfw.KEY_A):
            self.pos_x -= self.moving_step


def main():
    window = Window(640, 640, 'First lab Lisov')
    lab1_figure = DrawLab1()

    lab1_figure.add_child(Rectangle(-0.5, -0.5, 0.5, 0.5, [0.5, 0.4, 0]))
    lab1_figure.add_child(Rectangle(0.2, 0.2, 0.4, 0.4, [0, 0.4, 0]))
    lab1_figure.add_child(Rectangle(-0.2, 0.2, -0.4, 0.4, [0, 0.4, 0]))
    lab1_figure.add_child(Rectangle(0.4, -0.2, -0.4, -0.37, [1, 0.4, 0]))

    window.add_child(lab1_figure)
    window.run()


if __name__ == "__main__":
    main()

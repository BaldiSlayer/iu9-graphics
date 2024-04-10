import glfw
from engine import Drawable, Window, key_callback_decorator, Rectangle
from OpenGL.GL import *


class DrawLab2(Drawable):
    alpha = 0.0
    beta = 0.0
    size = 0.7
    fill = True

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
        if states.get(glfw.KEY_RIGHT):
            self.alpha += 2
        elif states.get(glfw.KEY_LEFT):
            self.alpha -= 2
        elif states.get(glfw.KEY_UP):
            self.beta -= 2
        elif states.get(glfw.KEY_DOWN):
            self.beta += 2
        elif states.get(glfw.KEY_SPACE):
            fill = not self.fill
            if fill:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)


def main():
    window = Window(640, 640, 'Second lab Lisov')
    lab2_figure = DrawLab2()

    window.add_child(lab2_figure)
    window.run()


if __name__ == "__main__":
    main()

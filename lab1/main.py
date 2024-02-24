import glfw
from OpenGL.GL import *
from engine import drawing_decorator, Drawable, Window, key_callback_decorator


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

    @drawing_decorator
    def draw(self):
        # Сначала переместим объект к целевой точке
        glTranslate(self.pos_x, self.pos_y, 0)

        # Изменение размера объекта
        glScalef(self.size, self.size, 200)

        # Затем выполним поворот вокруг оси Z
        glRotatef(self.angle, 0, 0, 1)

        # После вращения вернем объект обратно к исходной позиции
        glTranslate(-self.pos_x, -self.pos_y, 0)

        # больший квадрат
        glBegin(GL_POLYGON)
        glColor3f(0.5, 0.4, 0)
        glVertex2f(self.pos_x + 0.5, self.pos_y + 0.5)
        glVertex2f(self.pos_x + -0.5, self.pos_y + 0.5)
        glVertex2f(self.pos_x + -0.5, self.pos_y + -0.5)
        glVertex2f(self.pos_x + 0.5, self.pos_y + -0.5)
        glEnd()

        # рот
        glBegin(GL_POLYGON)
        glColor3f(1, 0.4, 0)
        # верхний правый
        glVertex2f(self.pos_x + 0.4, self.pos_y - 0.2)
        # верхний левый
        glVertex2f(self.pos_x + -0.4, self.pos_y - 0.2)
        glVertex2f(self.pos_x + -0.4, self.pos_y + -0.37)
        glVertex2f(self.pos_x + 0.4, self.pos_y + -0.37)
        glEnd()

        glBegin(GL_POLYGON)
        glColor3f(0, 0.4, 0)
        glVertex2f(self.pos_x + -0.2, self.pos_y + 0.4)
        glVertex2f(self.pos_x + -0.4, self.pos_y + 0.4)
        glVertex2f(self.pos_x + -0.4, self.pos_y + 0.2)
        glVertex2f(self.pos_x + -0.2, self.pos_y + 0.2)
        glEnd()

        glBegin(GL_POLYGON)
        glColor3f(0, 0.4, 0)
        glVertex2f(self.pos_x + 0.2, self.pos_y + 0.4)
        glVertex2f(self.pos_x + 0.4, self.pos_y + 0.4)
        glVertex2f(self.pos_x + 0.4, self.pos_y + 0.2)
        glVertex2f(self.pos_x + 0.2, self.pos_y + 0.2)
        glEnd()

        self.angle += self.delta * self.stop_rotating
        glfw.swap_buffers(self.window)

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
    lab1_figure.window = window.window
    window.add_child(lab1_figure)
    window.run()


if __name__ == "__main__":
    main()

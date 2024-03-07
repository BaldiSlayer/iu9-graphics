import glfw
import numpy as np
from OpenGL.GL import *
from math import cos, sin

alpha, beta = 0.0, 0.0
size = 0.7
is_filled = 1


def draw_cube(size):
    glBegin(GL_QUADS)

    glColor3f(0.3, 0.3, 0.8)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glVertex3f(-size / 2, -size / 2, size / 2)

    glColor3f(0.8, 0.3, 0.3)
    glVertex3f(size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)

    glColor3f(0.3, 0.8, 0.3)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(-size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, -size / 2, -size / 2)

    glColor3f(0.8, 0.8, 0.3)
    glVertex3f(-size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)

    glColor3f(0.3, 0.8, 0.8)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, -size / 2)

    glColor3f(0.8, 0.3, 0.8)
    glVertex3f(-size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glEnd()


def dymetrical_bla():
    global alpha, beta

    alpha_rad = np.radians(alpha)
    beta_rad = np.radians(beta)

    glMultMatrixf(np.array([
        [1, 0, 0, 0],
        [0, cos(beta_rad), -sin(beta_rad), 0],
        [0, sin(beta_rad), cos(beta_rad), 0],
        [0, 0, 0, 1]
    ]))

    glMultMatrixf(np.array([
        [cos(alpha_rad), 0, sin(alpha_rad), 0],
        [0, 1, 0, 0],
        [-sin(alpha_rad), 0, cos(alpha_rad), 0],
        [0, 0, 0, 1]
    ]))

    glMultMatrixf(np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [-0.34, 0, 1, 0],
            [0, 0, 0, 1]
    ]))


def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "Lab 2 Lisov Aleksey", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    while not glfw.window_should_close(window):
        display(window)

    glfw.destroy_window(window)
    glfw.terminate()


def display(window):
    glLoadIdentity()

    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)

    # сдвиг маленького куба
    glMultMatrixf([1, 0, 0, 0,
                   0, 1, 0, 0,
                   0, 0, 1, 0,
                   0.75, 0.75, 0, 1])

    glMultMatrixf([
        cos(0.3), sin(0.3) * sin(0.6), sin(0.6) * cos(0.6), 0,
        0, cos(0.6), -sin(0.6), 0,
        sin(0.3), -cos(0.3) * sin(0.6), -cos(0.3) * cos(0.6), 0,
        0, 0, 0, 1,
    ])

    draw_cube(0.19480450843)


    # отрисовка основного куба
    glLoadIdentity()

    dymetrical_bla()

    draw_cube(size)

    glfw.swap_buffers(window)
    glfw.poll_events()


def key_callback(window, key, scancode, action, mods):
    global alpha, beta, is_filled, size

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_RIGHT:
            alpha += 2
        elif key == glfw.KEY_LEFT:
            alpha -= 2
        elif key == glfw.KEY_UP:
            beta -= 2
        elif key == glfw.KEY_DOWN:
            beta += 2
        elif key == glfw.KEY_W:
            size += 0.1
        elif key == glfw.KEY_S:
            size -= 0.1
        elif key == glfw.KEY_SPACE:
            is_filled ^= 1
            if is_filled:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)


if __name__ == "__main__":
    main()

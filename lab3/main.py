import glfw
from OpenGL.GL import *
from math import cos, sin

alpha = 15.0
beta = 48.0
segments = 10


def draw_cylinder(radius, height, segments):
    segment_angle = 2.0 * 3.14 / segments

    glBegin(GL_TRIANGLE_STRIP)

    for i in range(0, segments + 1):
        x = radius * cos(i * segment_angle)
        y = radius * sin(i * segment_angle)
        z = 0.0
        glVertex3f(x, y, z)
        glColor3f(0.0, i / 10.0, 1.0)
        glVertex3f(x, y, height)

    for i in range(0, segments + 1):
        x = radius * cos(i * segment_angle)
        y = radius * sin(i * segment_angle)

        glVertex3f(x, y, 0.0)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(x, y, height)

    glEnd()


def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "Lab 3 Lisov Aleksey", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        display(window)

    glfw.destroy_window(window)
    glfw.terminate()


def display(window):
    global segments

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glLoadIdentity()
    # glPushMatrix()
    glMatrixMode(GL_PROJECTION)
    glRotatef(beta * 50.0, 1.0, 0.0, 0.0)
    glRotatef(alpha * 50.0, 0.0, 1.0, 0.0)

    draw_cylinder(0.5, 0.6, segments)

    # glPopMatrix()

    glfw.swap_buffers(window)
    glfw.poll_events()


def key_callback(window, key, scancode, action, mods):
    global alpha, beta, segments

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_RIGHT:
            alpha += 0.1
        elif key == glfw.KEY_LEFT:
            alpha -= 0.1
        elif key == glfw.KEY_UP:
            beta += 0.1
        elif key == glfw.KEY_DOWN:
            beta -= 0.1
        elif key == glfw.KEY_W:
            segments += 5
        elif key == glfw.KEY_S:
            segments -= 5
        elif key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)



if __name__ == "__main__":
    main()

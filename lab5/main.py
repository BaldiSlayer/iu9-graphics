import random
import tripy
import glfw
from OpenGL.GL import *
from PolygonCut import *

clipped = False
EPS = 1e-6
test = 0
original = False
clipper = False


def random_color():
    return random.randint(0, 256) / 256, random.randint(0, 256) / 256, random.randint(0, 256) / 256


def polygon(vertexes, color):
    return {
        'vertices': vertexes,
        'color': color,
        'triangulation': tripy.earclip([(i.x, i.y) for i in vertexes]),
    }


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        # Compare the x-coordinates first
        if self.x < other.x:
            return True
        elif self.x > other.x:
            return False
        else:
            # If x-coordinates are equal, compare the y-coordinates
            return self.y < other.y


def draw_polygon(triangles, color=(1.0, 1.0, 1.0)):
    for triangle in triangles:
        glColor3f(*color)
        glBegin(GL_POLYGON)
        for vertex in triangle:
            glVertex2f(vertex[0], vertex[1])
        glEnd()


def weiler_atherton(subject_polygon, clip_polygon):
    subj = ' '.join(f"{point.x} {point.y}" for point in subject_polygon)
    clip = ' '.join(f"{point.x} {point.y}" for point in clip_polygon)

    arr = []
    result = PolyClipping(subj, clip, False)

    for elem in result:
        b = elem.split()
        vertexes = []
        for p in range(0, len(b), 2):
            vertexes.append(Point(float(b[p]), float(b[p + 1])))

        arr.append(polygon(vertexes, color=random_color()))

    return arr


class Lab5:
    def __init__(self, width, height, title):
        if not glfw.init():
            return

        self.window = glfw.create_window(width, height, title, None, None)

        if not self.window:
            glfw.terminate()
            return

        self.title, self.width, self.height = title, width, height

        self.original = polygon([], color=random_color())
        self.clipper = polygon([], color=random_color())

        if test == 1:
            self.original = polygon([
                Point(0.161, 0.137),
                Point(0.281, 0.431),
                Point(0.619, 0.418),
                Point(0.558, 0.192)], (0.5, 0.5, 0.5))

            self.clipper = polygon([
                Point(0.183, 0.391),
                Point(0.224, 0.240),
                Point(0.610, 0.107),
                Point(0.657, 0.361),
                Point(0.429, 0.376), ], (0.2, 0.2, 0.2))

        if test == 2:
            self.original = polygon([
                Point(0.161, 0.137),
                Point(0.281, 0.431),
                Point(0.619, 0.418),
                Point(0.558, 0.192),
                Point(0.429, 0.376)], (0.5, 0.5, 0.5))

            self.clipper = polygon([
                Point(0.183, 0.391),
                Point(0.224, 0.240),
                Point(0.610, 0.107),
                Point(0.657, 0.361),
                Point(0.429, 0.376), ], (0.2, 0.2, 0.2))

        self.clipped = []

        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_mouse_button_callback(self.window, self.mouseCallback)

    def run(self):
        while not glfw.window_should_close(self.window):
            self.display()
            glfw.poll_events()

        glfw.destroy_window(self.window)
        glfw.terminate()

    def display(self):
        global clipped

        glMatrixMode(GL_PROJECTION)
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)

        if not clipped:
            if test == 0:
                if original:
                    draw_polygon(self.original['triangulation'], self.original['color'])
                if clipper:
                    draw_polygon(self.clipper['triangulation'], self.clipper['color'])
            else:
                draw_polygon(self.clipper['triangulation'], self.clipper['color'])
                draw_polygon(self.original['triangulation'], self.original['color'])
        else:
            for i in self.clipped:
                draw_polygon(i['triangulation'], i['color'])

        glfw.swap_buffers(self.window)

    def key_callback(self, _, key, scancode, action, mods):
        global clipped, original, clipper

        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_SPACE:
                clipped = True
                self.clipped = weiler_atherton(self.original['vertices'], self.clipper['vertices'])
            elif key == glfw.KEY_S:
                if test == 0:
                    original = True
                    self.original = polygon(self.original['vertices'], self.original['color'])
            elif key == glfw.KEY_C:
                if test == 0:
                    clipper = True
                    self.clipper = polygon(self.clipper['vertices'], self.clipper['color'])

    def mouseCallback(self, window, button, action, mods):
        if action == glfw.PRESS:
            if button == glfw.MOUSE_BUTTON_LEFT:
                xpos, ypos = glfw.get_cursor_pos(window)
                width, height = glfw.get_window_size(window)
                # Convert to normalized device coordinates (NDC)
                xndc = 2 * (xpos / width) - 1
                yndc = 1 - 2 * (ypos / height)

                if not original:
                    self.original['vertices'].append(Point(xndc, yndc))
                elif not clipper:
                    self.clipper['vertices'].append(Point(xndc, yndc))

                print(f"Mouse clicked at OpenGL NDC: ({xndc}, {yndc})")


def main():
    Lab5(800, 800, "Lab 5").run()


if __name__ == "__main__":
    main()

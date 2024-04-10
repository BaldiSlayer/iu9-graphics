from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

width = 200
height = 200
field = [[0] * width] * height

class Edge:
    def __init__(self, x_min, x_max, y_min, y_max, dx, dy):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.dx = dx


def create_edge_table(vertices):
    edges = []

    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]

        if y1 < y2:
            x_min, y_min = x1, y1
            x_max, y_max = x2, y2
        else:
            x_min, y_min = x2, y2
            x_max, y_max = x1, y1

        if y1 != y2:
            dx = (x_max - x_min) / (y_max - y_min)
            dy = 1 / (y_max - y_min)

            edge = Edge((x_min), (x_max), (y_min), (y_max), (dx), (dy))
            edges.append(edge)

    return sorted(edges, key=lambda edge: (edge.y_min, edge.x_min))


def draw_scanline(edges):
    active_edges = []
    y = edges[0].y_min

    while active_edges or edges:
        if edges:
            while edges and edges[0].y_min == y:
                active_edges.append(edges.pop(0))
            active_edges.sort(key=lambda edge: (edge.y_min, edge.x_min))

        scanline = []

        for edge in active_edges:
            scanline.append(edge.x_min)

        scanline.sort()

        for i in range(0, len(scanline), 2):
            x1 = round(scanline[i])
            x2 = round(scanline[i + 1])
            print(x1, x2)

            for t in range(x1, x2):
                draw_point(t, y)

        y += 1

        active_edges = [edge for edge in active_edges if edge.y_max != y]


def draw_point(x, y):
    const_addable = 1
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x+const_addable, y+const_addable)
    glEnd()


def draw_line(x0, y0, x1, y1):
    x0 = round(x0)
    y0 = round(y0)
    x1 = round(x1)
    y1 = round(y1)

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1

    if dy <= dx:
        m = dx / 2
        while x0 != x1:
            glVertex2f(x0, y0)  # Рисуем пиксель
            m -= dy
            if m < 0:
                y0 += sy
                m += dx
            x0 += sx
    else:
        m = dy / 2
        while y0 != y1:
            glVertex2f(x0, y0)  # Рисуем пиксель
            m -= dx
            if m < 0:
                x0 += sx
                m += dy
            y0 += sy
    glVertex2f(x1, y1)

def draw_polygon(vertices):
    #glBegin(GL_LINES)
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]

        draw_line(x1, y1, x2, y2)
    #glEnd()


# целочисленный алгоритм Брезенхема
def line(x0, y0, x1, y1):
    x0 = round(x0)
    y0 = round(y0)
    x1 = round(x1)
    y1 = round(y1)

    delta_x = abs(x1 - x0)
    delta_y = abs(y1 - y0)
    error = 0
    delta_err = (delta_y + 1)
    y = y0
    dir_y = y1 - y0

    if dir_y > 0:
        dir_y = 1

    if dir_y < 0:
        dir_y = -1

    for x in range(x0, x1 + 1):
        draw_point(x, y)
        error = error + delta_err

        if error >= (delta_x + 1):
            y = y + dir_y
            error = error - (delta_x + 1)


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(1.0, 1.0, 1.0)

    vertices = [(50, 50), (200, 100), (150, 200), (100, 150)]
    edges = create_edge_table(vertices)

    # draw_point(20, 20)

    # line(20, 20, 40, 40)

    # draw_polygon(vertices)
    draw_scanline(edges)

    glFlush()


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(0, 300, 0, 300)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Lisov lab 4")

    glutDisplayFunc(display)

    init()

    glutMainLoop()


if __name__ == "__main__":
    main()

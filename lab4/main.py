import glfw
from OpenGL.GL import *

visible = False
fillable = False
testing = False

EPS = 5

def scale_b(brig):
    return int(brig * 255)


class Lab4:
    def __init__(self, width, height, title):
        if not glfw.init():
            return

        self.window = glfw.create_window(width, height, title, None, None)

        if not self.window:
            glfw.terminate()
            return

        self.title, self.width, self.height = title, width, height
        self.field = [0] * (width * height)
        self.owners = dict()

        if testing:
            self.figures = [
                [
                    [1, 1], [500, 1], [250, 200], [1, 500]
                ],
                [
                    [300, 300], [400, 300], [400, 300], [300, 400]
                ],
                [
                    [10, 20], [30, 300], [250, 300], [300, 30]
                ],
            ]

        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_mouse_button_callback(self.window, self.mouseCallback)

    def drawFigures(self):
        self.field = [0] * (self.width * self.height)
        i = 0
        for fig in self.figures:
            self.drawFigure(fig, i)
            i += 1

    def fillFigures(self):
        #for i in range(self.height):
        #    for j in range(self.width):
        #        print(self.field[i * self.width + j], end=' ')
        #    print()

        u = -1
        for i in range(self.height):
            if i == u:
                sadffsadsafd = 0

            info = []
            for elems in range(len(self.figures)):
                info.append({
                    'lines': [],
                    'fill': False,
                    'start': 0,
                    'end': 0
                })

            startLineIdx = i * self.width
            for j in range(startLineIdx, startLineIdx + self.width):
                if self.field[j] == 255:
                    currentFigure = info[self.owners[(j - startLineIdx, i)]]
                    if not currentFigure['fill']:
                        currentFigure['fill'] = True
                        currentFigure['start'] = j - startLineIdx
                    else:
                        currentFigure['end'] = j - startLineIdx - 1
                        if abs(currentFigure['start'] - currentFigure['end']) > EPS:
                            currentFigure['fill'] = False
                            currentFigure['lines'].append([currentFigure['start'], currentFigure['end']])

            for elem in info:
                print(elem['lines'], i)
                for line in elem['lines']:
                    for j in range(line[0], line[1] + 1):
                        self.set_pixel(j, i, -1)

    def set_pixel(self, x, y, owner, brightness=255):
        brightness = min(255, max(0, int(brightness)))
        if 0 <= x < self.width and 0 <= y < self.height:
            index = y * self.width + x
            self.field[index] = brightness
            self.owners[(x, y)] = owner

    def drawFigure(self, figure, ind):
        #for i in range(len(figure)):
        #    figure[i] = [figure[i][0], self.height - figure[i][1]]

        def plot_line_low(x0, y0, x1, y1):
            dx = x1 - x0
            dy = y1 - y0
            yi = 1 if dy > 0 else -1
            dy = abs(dy)
            brightness = 1.0

            D = 2 * dy - dx
            y = y0

            for x in range(x0, x1 + 1):
                self.set_pixel(x, y, ind, scale_b(brightness))
                if D > 0:
                    y = y + yi
                    D = D - 2 * dx
                D = D + 2 * dy

        def plot_line_high(x0, y0, x1, y1):
            dx = x1 - x0
            dy = y1 - y0
            xi = 1 if dx > 0 else -1
            dx = abs(dx)
            brightness = 1.0

            D = 2 * dx - dy
            x = x0

            for y in range(y0, y1 + 1):
                self.set_pixel(x, y, ind, scale_b(brightness))
                if D > 0:
                    x = x + xi
                    D = D - 2 * dy
                D = D + 2 * dx

        # рисуем линии (границы)
        # с помощью алгоритма Брезенхема с устранением ступенчатости
        for i in range(0, len(figure)):
            x0, y0 = figure[i]
            x1, y1 = figure[(i + 1) % len(figure)]

            if abs(y1 - y0) < abs(x1 - x0):
                if x0 > x1:
                    plot_line_low(x1, y1, x0, y0)
                else:
                    plot_line_low(x0, y0, x1, y1)
            else:
                if y0 > y1:
                    plot_line_high(x1, y1, x0, y0)
                else:
                    plot_line_high(x0, y0, x1, y1)

    def run(self):
        while not glfw.window_should_close(self.window):
            self.display()
            glfw.poll_events()

        glfw.destroy_window(self.window)
        glfw.terminate()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT)

        if visible:
            glDrawPixels(self.width, self.height,
                         GL_BLUE, GL_UNSIGNED_BYTE,
                         self.field)

        glfw.swap_buffers(self.window)

    def mouseCallback(self, w, button, action, _):
        global visible

        if not visible and not testing:
            if action == glfw.PRESS and button == glfw.MOUSE_BUTTON_LEFT:
                x, y = glfw.get_cursor_pos(w)

                try:
                    len(self.figures)
                except Exception as e:
                    self.figures = [[]]

                self.figures[0].append([int(x), self.height - int(y)])

    def key_callback(self, _, key, scancode, action, mods):
        global visible, EPS

        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(self.window, True)
            elif key == glfw.KEY_UP:
                self.width += 10
                self.height += 10
                glfw.set_window_size(self.window, self.width, self.height)
            elif key == glfw.KEY_DOWN:
                self.width -= 10
                self.height -= 10
                glfw.set_window_size(self.window, self.width, self.height)
            elif key == glfw.KEY_SPACE:
                try:
                    len(self.figures)
                except Exception as e:
                    self.figures = [[]]

                if len(self.figures[0]) >= 3:
                    visible = True
                    self.drawFigures()
                    # self.fillFigures()
            elif key == glfw.KEY_ENTER:
                try:
                    len(self.figures)
                except Exception as e:
                    self.figures = [[]]

                if testing:
                    EPS = 0

                if len(self.figures[0]) >= 3:
                    visible = True
                    self.drawFigures()
                    self.fillFigures()

def main():
    Lab4(800, 800, "Lab 4").run()


if __name__ == "__main__":
    main()

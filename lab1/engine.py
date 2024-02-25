import glfw
from OpenGL.GL import *
from abc import ABC, abstractmethod


class PropertyWrapper:
    properties = dict()

    def __init__(self, last_, new_):
        if last_ is not None:
            self.properties = last_.properties.copy()

        for k, v in new_.items():
            self.properties[k] = v

    def __getattr__(self, item):
        if item in self.properties:
            return self.properties[item]
        else:
            raise AttributeError(f"'PropertyWrapper' object has no attribute '{item}'")

    def __repr__(self):
        return str(self.properties)


def get_properties(obj) -> dict:
    properties = {}
    for attribute in dir(obj):
        if not attribute.startswith('__') and attribute != '_abc_impl' and not callable(getattr(obj, attribute)):
            properties[attribute] = getattr(obj, attribute)
    return properties


def drawing_decorator(func):
    def drawing_wrapper(self, *args, **kwargs):
        glPushMatrix()
        func(self, *args, **kwargs)

        transmitted_values = PropertyWrapper(self.parent_properties, get_properties(self))

        if hasattr(self, 'children'):
            for child in self.children:
                child.parent_properties = transmitted_values
                child.draw()

        glPopMatrix()

    return drawing_wrapper


def key_callback_decorator(func):
    def key_callback_wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        if hasattr(self, 'children'):
            for child in self.children:
                child.states = self.states
                child.key_callback(self.states)

    return key_callback_wrapper


class Drawable(ABC):
    children: list["Drawable"] = []
    window = None
    parent_properties: PropertyWrapper

    def __init_subclass__(cls):
        cls.children = []
        cls.parent_properties = PropertyWrapper(None, {})
        cls.draw = drawing_decorator(cls.draw)

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    @key_callback_decorator
    def key_callback(self):
        pass

    def add_child(self, child: "Drawable"):
        self.children.append(child)

    def move_to(self, x, y, z):
        glTranslate(x, y, z)

    def scale(self, x, y, z):
        glScalef(x, y, z)

    def rotate(self, angle, x, y, z):
        glRotatef(angle, x, y, z)


class Window(Drawable):
    states = {}

    def __init__(self, width: int, height: int, title: str):
        if not glfw.init():
            return
        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            return

    def draw(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glClearColor(1.0, 1.0, 1.0, 1.0)

        self.draw()

        glfw.swap_buffers(self.window)

    @key_callback_decorator
    def key_callback(self, window, key, scancode, action, mods):
        if action in [0, 1]:
            self.states[key] = action

    def run(self):
        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, self.key_callback)

        while not glfw.window_should_close(self.window):
            self.display()
            glfw.poll_events()

        glfw.destroy_window(self.window)
        glfw.terminate()


class Rectangle(Drawable):
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    color = []

    def __init__(self, x1, y1, x2, y2, color):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.color = color

    @abstractmethod
    def draw(self):
        glBegin(GL_POLYGON)
        glColor3f(*self.color)
        glVertex2f(self.x1, self.y2)
        glVertex2f(self.x2, self.y2)
        glVertex2f(self.x2, self.y1)
        glVertex2f(self.x1, self.y1)
        glEnd()

    @key_callback_decorator
    def key_callback(self, states):
        pass

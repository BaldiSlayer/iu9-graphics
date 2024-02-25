import glfw
from OpenGL.GL import *
from abc import ABC, abstractmethod


def get_properties(obj):
    properties = {}
    for attribute in dir(obj):
        if not attribute.startswith('__') and attribute != '_abc_impl' and not callable(getattr(obj, attribute)):
            properties[attribute] = getattr(obj, attribute)
    return properties


def drawing_decorator(func):
    def drawing_wrapper(self, *args, **kwargs):
        # print(get_properties(self))
        glPushMatrix()
        func(self, *args, **kwargs)
        if hasattr(self, 'children'):
            for child in self.children:
                child.draw()
        glPopMatrix()

    return drawing_wrapper


def key_callback_decorator(func):
    def key_callback_wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        if hasattr(self, 'children'):
            for child in self.children:
                child.key_callback(self.states)

    return key_callback_wrapper


class Drawable(ABC):
    children: list["Drawable"] = []
    window = None

    def __init_subclass__(cls):
        cls.children = []
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
        # I don't know
        # Maybe it is not true for some cases
        child.window = self.window


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

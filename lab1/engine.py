import glfw
from OpenGL.GL import *
from abc import ABC, abstractmethod


def drawing_decorator(func):
    def drawing_wrapper(self, *args, **kwargs):
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

    def __init_subclass__(cls, **kwargs):
        cls.children = []

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def key_callback(self):
        pass

    def add_child(self, child):
        self.children.append(child)


class Window(Drawable):
    states = {}

    def __init__(self, width: int, height: int, title: str):
        if not glfw.init():
            return
        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            return

    @drawing_decorator
    def draw(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glClearColor(1.0, 1.0, 1.0, 1.0)

        self.draw()

        glfw.poll_events()

    @key_callback_decorator
    def key_callback(self, window, key, scancode, action, mods):
        if action in [0, 1]:
            self.states[key] = action

    def run(self):
        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, self.key_callback)
        while not glfw.window_should_close(self.window):
            self.display()
        glfw.destroy_window(self.window)
        glfw.terminate()
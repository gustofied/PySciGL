from OpenGL.constant import Constant
import numpy as np
import OpenGL.GL as GL
from OpenGL.GL.shaders import compileShader, compileProgram
import glfw
import glfw.GLFW as GLFW_CONSTANTS
import time
import ctypes
from pathlib import Path

glfw.init()
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)
window = glfw.create_window(300,300, "learnings", None, None)
glfw.make_context_current(window)
glfw.swap_interval(0) #vsync something


def make_shader_programme(vertex_filename: str, fragment_filename: str) -> int:
    vertex_module = make_shader_module(vertex_filename, GL.GL_VERTEX_SHADER)
    fragment_module = make_shader_module(fragment_filename, GL.GL_FRAGMENT_SHADER)
    return compileProgram(vertex_module, fragment_module)

def make_shader_module(filename: str, module_type: Constant) -> int:

    with open(filename, "r") as file:
        source_code = file.read()
        return compileShader(source_code, module_type)

class Renderer:
    
    
    def __init__(self):

        GL.glClearColor(0.3, 0.05, 0.15, 0.95)
        self.VAO = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.VAO)
        self.shader = make_shader_programme("learning_shader_vertex.txt", "learning_shader_fragment.txt")

    def draw(self):

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glUseProgram(self.shader)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

    def destroy(self):

        GL.glDeleteProgram(self.shader)


renderer = Renderer()

old_time = glfw.get_time()

while not glfw.window_should_close(window):
    glfw.poll_events()
    if (glfw.get_key(window, glfw.KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS):
        glfw.set_window_should_close(window, True)

    new_time = glfw.get_time()
    fps = 1 / (new_time - old_time)

    old_time = new_time

    glfw.set_window_title(window, f"FPS: {fps:.2f}")
    
    renderer.draw()

    glfw.swap_buffers(window)

renderer.destroy()
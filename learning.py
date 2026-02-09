import numpy as np
import OpenGL.GL as GL
from OpenGL.GL.shaders import compileShader
import glfw
import glfw.GLFW as GLFW_CONSTANTS
import time
import ctypes
from pathlib import Path
d
glfw.init()
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)
window = glfw.create_window(300,300, "learnings", None, None)
glfw.make_context_current(window)
# glfw.swap_interval(0) #vsync something


GL.glClearColor(0.3, 0.05, 0.15, 0.95)

old_time = glfw.get_time()

while not glfw.window_should_close(window):
    glfw.poll_events()
    if (glfw.get_key(window, glfw.KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS):
        glfw.set_window_should_close(window, True)

    new_time = glfw.get_time()
    fps = 1 / (new_time - old_time)

    old_time = glfw.get_time()

    glfw.set_window_title(window, f"FPS: {fps:.2f}")
    
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)

    #render here
    glfw.swap_buffers(window)

glfw.terminate()
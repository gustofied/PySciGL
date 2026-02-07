from OpenGL.GLES2 import glCreateShader, glCompileShader, glCreateProgram
import numpy as np
import OpenGL.GL as GL
from OpenGL.GL.shaders import compileShader, glAttachShader
import glfw
import glfw.GLFW as GLFW_CONSTANTS
import time
import ctypes
from pathlib import Path

# Window
glfw.init()
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)
window = glfw.create_window(400, 400, "sppedrun", None, None)
glfw.make_context_current(window)
glfw.swap_interval(1)

GL.glClearColor(0.2, 0.3, 0.3, 0.3)


dir = Path(__file__).resolve().parent
fragment_dir = dir / "m_fragment.txt"
vertex_dir = dir / "v_fragment.txt"

with open(fragment_dir, "r") as file:
    framenty = file.read()

with open(vertex_dir, "r") as file:
    vertexy = file.read()

print(framenty)
print(vertexy)

vertex = GL.glCreateShader(GL.GL_VERTEX_ARRAY)
GL.glShaderSource(vertex, vertexy)
GL.glCompileShader(vertex)


fragment = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
# GL_BUFFER_ARRAY
GL.glShaderSource(fragment, framenty)
GL.glCompileShader(fragment)

programmen = glCreateProgram()
GL.glAttachShader(programmen, vertex)
GL.glAttachShader(programmen, fragment)
GL.glLinkProgram(programmen)

dataen = np.array([
    [-0.75, 0.75, 0],
    [-0.75, -0.75, 0],
    [0.75, -0.75, 0],
]
)

vao = GL.glCreateVertexArrays()
vbo = GL.glCreateBuffers()

gl




# GL.glUseProgram(programmen)





while not glfw.window_should_close(window):
    glfw.poll_events()

    if glfw.get_key(window, glfw.KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
        glfw.set_window_should_close(window, True)

    GL.glClear(GL.GL_COLOR_BUFFER_BIT)

    glfw.swap_buffers(window)
    


    
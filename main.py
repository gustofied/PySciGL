from OpenGL.GL.VERSION.GL_1_0 import GL_COLOR_BUFFER_BIT
import OpenGL.GL as GL
from OpenGL.GL.shaders import compileShader
import numpy as np
import glfw
import glfw.GLFW as GLFW_CONSTANTS
from pathlib import Path
import ctypes

# as always we start with the winow

glfw.init()
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)
window = glfw.create_window(300, 300, "hellow", None, None)
glfw.make_context_current(window)
glfw.swap_interval(0)


my_dir = Path(__file__).resolve().parent
v_path = my_dir / "v_shader.txt"
f_path = my_dir / "f_shader.txt"


with open(v_path, "r") as file:
    vshader = file.read()

with open(f_path, "r") as file:
    fshader = file.read()

# compile and link


vertexShader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
GL.glShaderSource(vertexShader, vshader)
GL.glCompileShader(vertexShader)

fragmentShader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
GL.glShaderSource(fragmentShader, fshader)
GL.glCompileShader(fragmentShader)

programmen = GL.glCreateProgram()
GL.glAttachShader(programmen, vertexShader)
GL.glAttachShader(programmen, fragmentShader)
GL.glLinkProgram(programmen)

# GL.glDeleteShader(programmen, vertexShader)
# GL.glDeleteShader(programmen, fragmentShader)


# some data in cpu

vertices = np.array(
    [
    [-0.75, 0.75, 0],
    [-0.75, -0.75, 0],
    [0.75, -0.75, 0]
    ], dtype=np.float32
)

vao = GL.glGenVertexArrays(1)
vbo = GL.glGenBuffers(1)

GL.glBindVertexArray(vao)
GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
GL.glBufferData(GL.GL_ARRAY_BUFFER, 36, vertices, GL.GL_STATIC_DRAW)
GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 12, ctypes.c_void_p(0))
GL.glEnableVertexAttribArray(0)

GL.glUseProgram(programmen)


GL.glClearColor(0.43, 0.33, 0.23, 0.5)

# loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    if glfw.get_key(window,GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
        glfw.set_window_should_close(window, True)

    GL.glClear(GL_COLOR_BUFFER_BIT)

    GL.glBindVertexArray(vao)
    GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

    # draw here

    glfw.swap_buffers(window)

glfw.terminate()
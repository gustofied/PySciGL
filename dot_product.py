from OpenGL.GL.VERSION.GL_1_0 import GL_COLOR_BUFFER_BIT
import OpenGL.GL as GL
from OpenGL.GL.shaders import compileShader
import numpy as np
import glfw
import glfw.GLFW as GLFW_CONSTANTS
from pathlib import Path
import ctypes

# as always we start with the winow
def run():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)
    window = glfw.create_window(600, 600, "Dot Product", None, None)
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

    GL.glDeleteShader(vertexShader)
    GL.glDeleteShader(fragmentShader)

    # some data in cpu

    vertices = np.array(
        [
        [ 0.0, 0.0, 0.0],
        [-0.75, -0.75, 0.0],
        [ 0.0, 0.00, 0.0],
        [-0.25, -0.75, 0.0],
        ], dtype=np.float32
    )

    print(vertices.shape)
    # v_1 = vertices[1] - vertices[0]
    # v_2 = vertices[3] - vertices[2]
    # doten = v_1 @ v_2
    # print(doten)

    vao = GL.glGenVertexArrays(1)
    vbo = GL.glGenBuffers(1)

    GL.glBindVertexArray(vao)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_DYNAMIC_DRAW)
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 12, ctypes.c_void_p(0))
    GL.glEnableVertexAttribArray(0)

    GL.glUseProgram(programmen)

    GL.glClearColor(0.43, 0.33, 0.23, 0.5)

    # loop
    theta = 0
    L = np.linalg.norm(vertices[3] - vertices[2])
    print(L)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        if glfw.get_key(window,GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
            glfw.set_window_should_close(window, True)


        GL.glClear(GL_COLOR_BUFFER_BIT)


        if glfw.get_key(window,GLFW_CONSTANTS.GLFW_KEY_RIGHT) == GLFW_CONSTANTS.GLFW_PRESS:
            theta -= 0.02
            vertices[3] = [np.cos(theta) * L, np.sin(theta) * L, 0]
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
            GL.glBufferSubData(GL.GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

        if glfw.get_key(window,GLFW_CONSTANTS.GLFW_KEY_LEFT) == GLFW_CONSTANTS.GLFW_PRESS:
            theta += 0.02
            vertices[3] = [np.cos(theta) * L, np.sin(theta) * L, 0]
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
            GL.glBufferSubData(GL.GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)


        GL.glBindVertexArray(vao)
        GL.glDrawArrays(GL.GL_LINES, 0, 4)

        # draw here

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    run()
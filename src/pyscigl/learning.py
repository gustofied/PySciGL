from OpenGL.constant import Constant
import numpy as np
import OpenGL.GL as GL
from OpenGL.GL.shaders import compileShader, compileProgram
import glfw
import glfw.GLFW as GLFW_CONSTANTS
import time
import ctypes
from pathlib import Path
import numpy as np

def run():

    DATA_TYPE_COLORED_VERTEX = np.dtype({
        "names": ['x', 'y', 'z', 'color'], 
        "formats": [np.float32, np.float32, np.float32, np.uint32],
        "offsets": [0, 4, 8, 12],
        "itemzise": 16
    })


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
        filepath = Path(__file__).parent / filename
        with open(filepath, "r") as file:
            source_code = file.read()
            return compileShader(source_code, module_type)

    class Mesh:

        def __init__(self):
            self.VAO = GL.glGenVertexArrays(1)
            self.VBO, self.EBO = GL.glGenBuffers(2)
            self.index_count = 0
        
        def build_colored_quad(self) -> "Mesh":

            vertices = np.zeros(4, dtype=DATA_TYPE_COLORED_VERTEX)

            vertices[0]["x"] = -0.75
            vertices[0]["y"] = -0.75
            vertices[0]["z"] = 0.0
            vertices[0]["color"] = 0


            vertices[1]["x"] = 0.5
            vertices[1]["y"] = -0.75
            vertices[1]["z"] = 0.0
            vertices[1]["color"] = 1

            vertices[2]["x"] = 0.75
            vertices[2]["y"] = 0.75
            vertices[2]["z"] = 0.0
            vertices[2]["color"] = 2


            vertices[3]["x"] = -0.75
            vertices[3]["y"] = 0.75
            vertices[3]["z"] = 0.0
            vertices[3]["color"] = 0

            GL.glBindVertexArray(self.VAO)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.VBO)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 16, ctypes.c_voidp(0))
            GL.glEnableVertexAttribArray(0)
            GL.glVertexAttribPointer(1, 1, GL.GL_INT, GL.GL_FALSE, 16, ctypes.c_voidp(12))
            GL.glEnableVertexAttribArray(1)

            self.index_count = 6
            indices = np.array(
                [0, 1, 2, 2, 3, 0], dtype=np.ubyte)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.EBO)
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL.GL_STATIC_DRAW)


            return self


        def draw(self) -> None:

            GL.glBindVertexArray(self.VAO)
            GL.glDrawElements(GL.GL_TRIANGLES, self.index_count, GL.GL_UNSIGNED_BYTE, ctypes.c_void_p(0))

        
        def destroy(self) -> None:

            GL.glDeleteVertexArrays(1, (self.VAO))
            GL.glDeleteBuffers(1, (self.VBO))


    class Renderer:
        
        def __init__(self):

            GL.glClearColor(0.3, 0.05, 0.15, 0.95)
            self.mesh = Mesh().build_colored_quad()
            self.shader = make_shader_programme("learning_shader_vertex.txt", "learning_shader_fragment.txt")

        def draw(self):

            GL.glClear(GL.GL_COLOR_BUFFER_BIT)
            GL.glUseProgram(self.shader)
            self.mesh.draw()

        def destroy(self):

            self.mesh.destroy()
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

if __name__ == "__main__":
    run()
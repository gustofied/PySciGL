from PIL import Image
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
        "names": ['x', 'y', 'z', 'color', 'u', 'v'], 
        "formats": [np.float32, np.float32, np.float32, np.uint32,  np.float32,  np.float32],
        "offsets": [0, 4, 8, 12, 16, 20],
        "itemzise": 24 
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
        filepath = Path(__file__).parent / "shaders"/ filename
        with open(filepath, "r") as file:
            source_code = file.read()
            return compileShader(source_code, module_type)


    class Material:

        def __init__(self):

            self.texture = GL.glGenTextures(1)

        def load_from_file(self, filename: str) -> "Material":
            filepath = Path(__file__).parent / "assets"/ filename

            image = Image.open(filepath)    
            width = image.width
            height = image.height                                         
            data = image.transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA").tobytes()


            GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
            # need to look into this call
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width, height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, data)

            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)










            return self

        def use(self) -> None:

            GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)

        
        def destroy(self) -> None:

            GL.glDeleteTextures(1, (self.texture))

    class Mesh:

        def __init__(self):
            self.VAO = GL.glGenVertexArrays(1)
            self.VBO, self.EBO = GL.glGenBuffers(2)
            self.index_count = 0
        
        def build_colored_quad(self) -> "Mesh":

            vertices = np.zeros(6, dtype=DATA_TYPE_COLORED_VERTEX)


            # vertex 0
            vertices[0]["x"] = -1
            vertices[0]["y"] = -0.75
            vertices[0]["z"] = 0.0
            vertices[0]["color"] = 0
            vertices[0]["u"] = 0.0
            vertices[0]["v"] = 0.0

            # vertex 1
            vertices[1]["x"] = 0.25
            vertices[1]["y"] = -0.75
            vertices[1]["z"] = 0.0
            vertices[1]["color"] = 1
            vertices[1]["u"] = 1.0
            vertices[1]["v"] = 0.0

            # vertex 2
            vertices[2]["x"] = -0.15
            vertices[2]["y"] = 0.75
            vertices[2]["z"] = 0.0
            vertices[2]["color"] = 2
            vertices[2]["u"] = 0.5
            vertices[2]["v"] = 1.0

            # vertex 3
            vertices[3]["x"] = -0.5
            vertices[3]["y"] = 0
            vertices[3]["z"] = 0.0
            vertices[3]["color"] = 0
            vertices[3]["u"] = 0.0
            vertices[3]["v"] = 0.5

            # vertex 4
            vertices[4]["x"] = -0.25
            vertices[4]["y"] = -0.75
            vertices[4]["z"] = 0.0
            vertices[4]["color"] = 0
            vertices[4]["u"] = 0.5
            vertices[4]["v"] = 0.0

            # vertex 5
            vertices[5]["x"] = 0.25
            vertices[5]["y"] = 0
            vertices[5]["z"] = 0.0
            vertices[5]["color"] = 0
            vertices[5]["u"] = 1.0
            vertices[5]["v"] = 0.5

            GL.glBindVertexArray(self.VAO)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.VBO)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 24, ctypes.c_voidp(0))
            GL.glEnableVertexAttribArray(0)
            GL.glVertexAttribPointer(1, 1, GL.GL_INT, GL.GL_FALSE, 24, ctypes.c_voidp(12))
            GL.glEnableVertexAttribArray(1)
            GL.glVertexAttribPointer(2, 2, GL.GL_FLOAT, GL.GL_FALSE, 24, ctypes.c_voidp(16))
            GL.glEnableVertexAttribArray(2)

            self.index_count = 9
            indices = np.array(
                [0, 4, 3, 4, 1, 5, 3, 5, 2], dtype=np.ubyte)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.EBO)
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL.GL_STATIC_DRAW)


            return self


        def draw(self) -> None:

            GL.glBindVertexArray(self.VAO)
            GL.glDrawElements(GL.GL_TRIANGLES, self.index_count, GL.GL_UNSIGNED_BYTE, ctypes.c_void_p(0))

        
        def destroy(self) -> None:

            GL.glDeleteVertexArrays(1, (self.VAO))
            GL.glDeleteBuffers(2, (self.VBO, self.VBO))


    class Renderer:
        
        def __init__(self):

            GL.glClearColor(0.3, 0.05, 0.15, 0.95)
            self.mesh = Mesh().build_colored_quad()
            self.material = Material().load_from_file("texture.png")
            self.shader = make_shader_programme("learning_shader_vertex.txt", "learning_shader_fragment.txt")

        def draw(self):

            GL.glClear(GL.GL_COLOR_BUFFER_BIT)
            GL.glUseProgram(self.shader)
            self.material.use()
            self.mesh.draw()

        def destroy(self):

            self.mesh.destroy()
            self.material.destroy()
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
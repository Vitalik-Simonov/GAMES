import numpy as np
import taichi as ti
import taichi_glsl as ts
from settings import *

ti.init(arch=ti.cuda)  # ti.cpu ti.gpu ti.vulkan ti.opengl ti.metal(macOS)

# load texture
texture_size = texture.get_size()[0]
# texture color normalization  0 - 255 --> 0.0 - 1.0
texture_array = pg.surfarray.array3d(texture).astype(np.float32) / 255


@ti.data_oriented
class PyShader:
    def __init__(self, app):
        self.app = app
        self.screen_array = np.full((width, height, 3), [0, 0, 0], np.uint8)
        # taichi fields
        self.screen_field = ti.Vector.field(3, ti.uint8, (width, height))
        self.texture_field = ti.Vector.field(3, ti.float32, texture.get_size())
        self.texture_field.from_numpy(texture_array)

    @ti.kernel
    def render(self, time: ti.float32, delta: ti.float32):
        """fragment shader imitation"""
        for frag_coord in ti.grouped(self.screen_field):
            # normalized pixel coords

            uv = frag_coord
            uv.x += delta

            uv.x %= texture_size
            uv.y %= texture_size

            col = vec3(0.0)

            col += self.texture_field[uv.x, uv.y]

            col = ts.clamp(col, 0.0, 1.0)
            self.screen_field[frag_coord.x, resolution.y - frag_coord.y] = col * 255

    def update(self, delta):
        time = pg.time.get_ticks() * 1e-03  # time in sec

        self.render(time, delta)
        self.screen_array = self.screen_field.to_numpy()

    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

    def run(self, delta):
        self.update(delta)
        self.draw()


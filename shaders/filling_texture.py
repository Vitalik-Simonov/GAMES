import pygame as pg
import numpy as np
import taichi as ti
import taichi_glsl as ts
from taichi_glsl import vec2, vec3


ti.init(arch=ti.cuda)  # ti.cpu ti.gpu ti.vulkan ti.opengl ti.metal(macOS)
# resolution = width, height = vec2(1940, 1015)
resolution = width, height = vec2(1600, 900)

# load texture
texture = pg.image.load('img/city.png')
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
    def render(self, time:ti.float32, flag: ti.int32):
        """fragment shader imitation"""

        for frag_coord in ti.grouped(self.screen_field):
            col = vec3(0.0)
            uv = (frag_coord - 0.5 * resolution) / resolution.y
            rho = ts.length(uv)

            col += self.texture_field[frag_coord.x, resolution.y - frag_coord.y]

            if flag:
                col += 0.1 / rho * time * 2

            col = ts.clamp(col, 0.0, 1.0)

            self.screen_field[frag_coord.x, resolution.y - frag_coord.y] = col * 255

    def update(self, flag, time):
        self.render(time, flag)
        self.screen_array = self.screen_field.to_numpy()

    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

    def run(self, flag, time):
        self.update(flag, time)
        self.draw()


class App:
    def __init__(self):
        self.screen = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        self.shader = PyShader(self)

    def run(self):
        flag = 0
        start = 0
        while True:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
                elif i.type == pg.MOUSEBUTTONDOWN:
                    flag = 1
                    start = pg.time.get_ticks()

            time = (pg.time.get_ticks() - start) * 1e-03  # time in sec
            self.shader.run(flag, time)
            pg.display.flip()

            self.clock.tick()
            pg.display.set_caption(f'FPS: {self.clock.get_fps() :.2f}')


if __name__ == '__main__':
    app = App()
    app.run()

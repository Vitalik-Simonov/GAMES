import pygame as pg
import numpy as np
import taichi as ti
import taichi_glsl as ts
from taichi_glsl import vec2, vec3

ti.init(arch=ti.cuda)  # ti.cpu ti.gpu ti.vulkan ti.opengl ti.metal(macOS)
resolution = width, height = vec2(1600, 900)

# load texture
texture = pg.image.load('img/wall2.jpg')  # texture res - 2^n x 2^n (512 x 512, 1024 x 1024, ...)
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

            uv.x %= resolution.x

            col = vec3(0.0)

            col += self.texture_field[uv.x, resolution.y - uv.y]
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


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(resolution, pg.SCALED)
        self.clock = pg.time.Clock()
        self.shader = PyShader(self)

    def run(self):
        delta = 0
        while True:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()

            if pg.key.get_pressed()[pg.K_RIGHT]:
                delta += 1
            elif pg.key.get_pressed()[pg.K_LEFT]:
                delta -= 1

            self.shader.run(delta)
            pg.display.flip()

            self.clock.tick()
            pg.display.set_caption(f'FPS: {self.clock.get_fps() :.2f}')


if __name__ == '__main__':
    app = App()
    app.run()

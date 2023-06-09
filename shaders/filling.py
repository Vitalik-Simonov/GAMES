import pygame as pg
import numpy as np
import taichi as ti
import taichi_glsl as ts
from taichi_glsl import vec2, vec3


ti.init(arch=ti.cuda)  # ti.cpu ti.gpu ti.vulkan ti.opengl ti.metal(macOS)
# resolution = width, height = vec2(1940, 1015)
resolution = width, height = vec2(1600, 900)

@ti.data_oriented
class PyShader:
    def __init__(self, app):
        self.app = app
        self.screen_array = np.full((width, height, 3), [0, 0, 0], np.uint8)
        # taichi fields
        self.screen_field = ti.Vector.field(3, ti.uint8, (width, height))

    @ti.kernel
    def render(self, time:ti.float32):
        """fragment shader imitation"""

        for frag_coord in ti.grouped(self.screen_field):
            col = vec3(0.0)
            uv = (frag_coord - 0.5 * resolution) / resolution.y
            rho = ts.length(uv)

            col += 0.1 / rho * time * 2

            col = ts.clamp(col, 0.0, 1.0)

            self.screen_field[frag_coord.x, resolution.y - frag_coord.y] = col * 255

    def update(self):
        time = pg.time.get_ticks() * 1e-03  # time in sec
        self.render(time)
        self.screen_array = self.screen_field.to_numpy()

    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

    def run(self):
        self.update()
        self.draw()


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(resolution)
        self.clock = pg.time.Clock()
        self.shader = PyShader(self)

    def run(self):
        while True:
            self.shader.run()
            pg.display.flip()

            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick()
            pg.display.set_caption(f'FPS: {self.clock.get_fps() :.2f}')


if __name__ == '__main__':
    app = App()
    app.run()

import pygame as pg
import numpy as np
import taichi as ti
import taichi_glsl as ts
from taichi_glsl import vec2, vec3
from fu import *

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
        c1 = vec3(0.5, 0.0, 0.1)
        c2 = vec3(0.9, 0.1, 0.0)
        c3 = vec3(0.2, 0.1, 0.7)
        c4 = vec3(1.0, 0.9, 0.1)
        c5 = vec3(0.1)
        c6 = vec3(0.9)
        # speed = vec2(1.2, 0.1)
        speed = vec2(0, 0)
        shift = 1.77 + ts.sin(time * 2.0) / 10.0
        dist = 6.0 + ts.sin(time * 0.4) / .6

        for frag_coord in ti.grouped(self.screen_field):

            p = frag_coord.xy * dist / resolution.xx
            p.x -= time / 1.1
            q = fbm(p - time * 0.01 + 1.0 * ts.sin(time) / 10.0)
            # qb = fbm(p - time * 0.002 + 0.1 * ts.cos(time) / 5.0)
            # q2 = fbm(p - time * 0.44 - 5.0 * ts.cos(time) / 7.0) - 6.0
            # q3 = fbm(p - time * 0.9 - 10.0 * ts.cos(time) / 30.0) - 4.0
            # q4 = fbm(p - time * 2.0 - 20.0 * ts.sin(time) / 20.0) + 2.0
            # q = (q + qb - q2 - q3 + q4) / 3.8
            # r = vec2(fbm(p + q / 2.0 + time * speed.x - p.x - p.y), fbm(p + q - time * speed.y))
            # c = ts.mix(c1, c2, fbm(p + r)) + ts.mix(c3, c4, r.x) - ts.mix(c5, c6, r.y)
            # color = vec3(c * ts.cos(shift * frag_coord.y / resolution.y))
            # color -= .25
            # color.r *= 1.02
            # hsv = rgb2hsv(color)
            # hsv.y *= hsv.z * 0.8
            # hsv.z *= hsv.y * 1.3
            # color = hsv2rgb(hsv)

            # color = ts.clamp(color, 0.0, 1.0)
            # self.screen_field[frag_coord.x, resolution.y - frag_coord.y] = color * 255

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

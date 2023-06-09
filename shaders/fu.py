import taichi_glsl as ts
from taichi_glsl import vec2, vec3
from random import randrange as rnd


def rotate2D(uv, a):
    s = ts.sin(a)
    c = ts.cos(a)

    sr = ts.mat([list(uv)[0], 0], [list(uv)[1], 0])

    re = list(ts.mat(
        [c, -s],
        [s, c]
    ) @ sr)
    print(re)
    res = vec2(re[0][0], re[1][0])

    return res


def scale2D(uv, x, y):
    sr = ts.mat([list(uv)[0], 0], [list(uv)[1], 0])

    re = list(ts.mat(
        [x, 0],
        [0, y]
    ) @ sr)
    print(re)
    res = vec2(re[0][0], re[1][0])

    return res


def move2D(uv, delt_x, delt_y):
    sr = ts.mat([list(uv)[0], 0, 0], [list(uv)[1], 0, 0], [1, 0, 0])

    re = list(ts.mat(
        [1, 0, delt_x],
        [0, 1, delt_y],
        [0, 0, 1]
    ) @ sr)
    print(re)
    res = vec2(re[0][0], re[1][0])

    return res


def rgb2hsv(c):
    K = ts.vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0)
    p = ts.mix(ts.vec4(c.bg, K.wz), ts.vec4(c.gb, K.xy), ts.step(c.b, c.g))
    q = ts.mix(ts.vec4(p.xyw, c.r), ts.vec4(c.r, p.yzx), ts.step(p.x, c.r))

    d = q.x - min(q.w, q.y)
    e = 1.0e-10
    return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x)


def hsv2rgb(c):
    K = ts.vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0)
    p = abs(ts.fract(c.xxx + K.xyz) * 6.0 - K.www)
    return c.z * ts.mix(K.xxx, ts.clamp(p - K.xxx, 0.0, 1.0), c.y)


def noise(n):
    d = vec2(0.0, 1.0)
    b = ts.floor(n)
    f = ts.smoothstep(vec2(0.0), vec2(1.0), ts.fract(n))
    a1 = ts.mix(rnd(b), rnd(b + d.yx), f.x)
    a2 = ts.mix(rnd(b + d.xy), rnd(b + d.yy), f.x)
    a3 = f.y
    return ts.mix(a1, a2, a3)


def fbm(n):
    total = 0.0
    amplitude = 1.0
    for i in range(5):
        total += noise(n) * amplitude
        n += n * 1.7
        amplitude *= 0.47
    return total

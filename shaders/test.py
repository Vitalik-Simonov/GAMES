import taichi_glsl as ts
from taichi_glsl import vec2, vec3
from fu import *

q = fbm(4 - 3 * 0.01 + 1.0 * ts.sin(3) / 10.0)
"""
昙花一现 · 粒子爱心
Particle heart bloom with breathing, trailing, ethereal glow
"""

import pygame
import math
import random
import sys

# ─── Config ───
W, H = 900, 680
BG = (8, 6, 20)         # deep night-sky blue-black
NUM = 500                # particle count
FPS = 60
TRAIL = 22               # trail fade alpha (lower = longer)

# Ethereal palette — white, cream, pink, lavender, pale blue
PALETTE = [
    (255, 245, 238),
    (255, 222, 230),
    (238, 215, 255),
    (215, 230, 255),
    (255, 240, 220),
    (245, 230, 255),
]

# ─── Heart shape (parametric) ───
def heart_xy(t):
    """t in [0, 2pi] → (x, y)"""
    x = 16 * math.sin(t) ** 3
    y = (13 * math.cos(t) - 5 * math.cos(2 * t)
         - 2 * math.cos(3 * t) - math.cos(4 * t))
    return x, -y

CX, CY = W // 2, H // 2 - 15
SCALE = 17

# Precompute target positions with slight organic jitter
targets = []
for i in range(NUM):
    t = i / NUM * 2 * math.pi + random.uniform(-0.015, 0.015)
    x, y = heart_xy(t)
    x += random.gauss(0, 0.10)
    y += random.gauss(0, 0.10)
    targets.append((x * SCALE + CX, y * SCALE + CY))

# ─── Glow texture cache ───
_glow_cache = {}

def make_glow(radius):
    """Create white glow circle of given pixel radius."""
    r = max(1, int(radius))
    if r in _glow_cache:
        return _glow_cache[r]
    d = r * 2
    surf = pygame.Surface((d, d), pygame.SRCALPHA)
    # Outer soft halo (very faint)
    for i in range(r, r // 2, -2):
        t = (r - i) / (r - r // 2)
        a = int(30 * (1 - t * t))
        if a > 1:
            pygame.draw.circle(surf, (255, 255, 255, a), (r, r), i)
    # Inner glow
    for i in range(r // 2, 0, -1):
        t = 1.0 - i / (r // 2)
        a = int(80 * (1 - t * t))
        pygame.draw.circle(surf, (255, 255, 255, a), (r, r), i)
    # Hot core
    pygame.draw.circle(surf, (255, 255, 255, 200), (r, r), max(1, r // 4))
    _glow_cache[r] = surf
    return surf

# ─── Particle ───
class Particle:
    __slots__ = ('idx', 'tx', 'ty', 'x', 'y', 'vx', 'vy',
                 'color', 'size', 'base_alpha', 'phase',
                 'glow_mul', 'sp_speed', 'sp_phase',
                 '_alpha', '_pulse')

    def __init__(self, idx):
        self.idx = idx
        self.tx, self.ty = targets[idx]
        self.reset()
        # Persist across resets
        self.color = random.choice(PALETTE)
        self.color = tuple(max(0, min(255, c + random.randint(-12, 12)))
                           for c in self.color)
        self.size = random.uniform(2.0, 5.5)
        self.base_alpha = random.uniform(0.55, 1.0)
        self.phase = random.uniform(0, 2 * math.pi)
        self.glow_mul = random.uniform(1.0, 2.5)
        self.sp_speed = random.uniform(1.5, 3.5)
        self.sp_phase = random.uniform(0, 2 * math.pi)

    def reset(self):
        self.x = random.uniform(0, W)
        self.y = random.uniform(0, H)
        self.vx = 0.0
        self.vy = 0.0

    def update(self, breath, elapsed):
        # Target with breathing scale
        tx = (self.tx - CX) * breath + CX
        ty = (self.ty - CY) * breath + CY

        dx = tx - self.x
        dy = ty - self.y
        dist = math.hypot(dx, dy)

        if dist > 0.3:
            force = 0.006 + 0.003 * min(dist / 50.0, 1.0)
            self.vx += dx * force
            self.vy += dy * force
            self.vx *= 0.93
            self.vy *= 0.93
            self.x += self.vx
            self.y += self.vy
        else:
            self.x += (tx - self.x) * 0.06
            self.y += (ty - self.y) * 0.06

        # Alpha: breath + individual sparkle
        bm = 0.7 + 0.3 * math.sin(elapsed * 0.9 + self.phase)
        sp = 0.88 + 0.12 * math.sin(elapsed * self.sp_speed + self.sp_phase)
        self._alpha = self.base_alpha * bm * sp

        # Pulsing size
        self._pulse = self.size * (0.92 + 0.08 *
                      math.sin(elapsed * 0.6 + self.phase * 0.7))


# ─── Init ───
pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("昙花一现 · 粒子爱心")
clock = pygame.time.Clock()

particles = [Particle(i) for i in range(NUM)]
trail_surf = pygame.Surface((W, H))
trail_surf.set_alpha(TRAIL)
particle_layer = pygame.Surface((W, H), pygame.SRCALPHA)

running = True
elapsed = 0.0
show_hint = 3.0  # seconds

# ─── Main ───
while running:
    dt = clock.tick(FPS) / 1000.0
    elapsed += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                for p in particles:
                    p.reset()
                elapsed = 0

    # ─── Breath: 0.82 ~ 1.18 ───
    breath = 1.0 + 0.18 * math.sin(elapsed * 1.1)

    # ─── Trail overlay (fades previous frame) ───
    trail_surf.fill(BG)
    screen.blit(trail_surf, (0, 0))

    # ─── Render particles ───
    particle_layer.fill((0, 0, 0, 0))

    for p in particles:
        p.update(breath, elapsed)

        a = p._alpha
        if a <= 0.01:
            continue

        size = p._pulse
        px, py = int(p.x), int(p.y)
        col = p.color
        alpha = int(a * 255)

        # Glow halo (white → tinted via blend with colored core)
        gr = int(size * p.glow_mul)
        glow = make_glow(gr)
        glow.set_alpha(int(a * 180))
        particle_layer.blit(glow, (px - gr, py - gr),
                            special_flags=pygame.BLEND_ALPHA_SDL2)

        # Core circle
        cr = max(1, int(size * 0.45))
        pygame.draw.circle(particle_layer, (*col, alpha), (px, py), cr)

        # Bright white center
        hr = max(1, cr // 2)
        pygame.draw.circle(particle_layer, (255, 255, 255, alpha),
                           (px, py), hr)

    screen.blit(particle_layer, (0, 0))

    # ─── Hint ───
    if elapsed < show_hint:
        font = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 17)
        txt = font.render("空格键 = 重新散落 · ESC = 退出", True,
                          (120, 140, 180))
        alpha = int(200 * (1 - elapsed / show_hint))
        txt.set_alpha(alpha)
        screen.blit(txt, (W // 2 - txt.get_width() // 2, H - 50))

    pygame.display.flip()

pygame.quit()
sys.exit()

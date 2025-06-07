import pygame
from typing import Tuple
from config import WHITE, BLACK

class CourierSprite:
    """Representasi kurir; menggambar segitiga dengan arah dan status paket"""
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y
        self.direction = 'RIGHT'
        self.size = 16
        self.has_package = False

    def move_to(self, nx: int, ny: int):
        dx, dy = nx - self.x, ny - self.y
        if abs(dx) > abs(dy):
            self.direction = 'RIGHT' if dx > 0 else 'LEFT'
        else:
            self.direction = 'DOWN' if dy > 0 else 'UP'
        self.x, self.y = nx, ny

    def draw(self, screen: pygame.Surface, scale: float, offset: Tuple[int, int]):
        ox, oy = offset
        sx = int(self.x * scale) + ox
        sy = int(self.y * scale) + oy
        sz = max(8, int(self.size * scale))
        if self.direction == 'RIGHT':
            pts = [(sx + sz, sy), (sx - sz // 2, sy - sz // 2), (sx - sz // 2, sy + sz // 2)]
        elif self.direction == 'LEFT':
            pts = [(sx - sz, sy), (sx + sz // 2, sy - sz // 2), (sx + sz // 2, sy + sz // 2)]
        elif self.direction == 'UP':
            pts = [(sx, sy - sz), (sx - sz // 2, sy + sz // 2), (sx + sz // 2, sy + sz // 2)]
        else:
            pts = [(sx, sy + sz), (sx - sz // 2, sy - sz // 2), (sx + sz // 2, sy - sz // 2)]
        color = (0, 255, 0) if self.has_package else (0, 0, 255)
        pygame.draw.polygon(screen, color, pts)
        pygame.draw.polygon(screen, BLACK, pts, 2)

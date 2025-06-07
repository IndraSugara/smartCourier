import pygame
import os
import random
import numpy as np
from typing import Tuple, List, Optional
from PIL import Image
from config import WINDOW_WIDTH, WINDOW_HEIGHT, MAP_OFFSET, ROAD_COLOR_MIN, ROAD_COLOR_MAX

class MapProcessor:
    """Kelas untuk memuat dan memproses peta digital"""
    def __init__(self):
        self.map_image: Optional[pygame.Surface] = None
        self.road_grid: Optional[np.ndarray] = None
        self.scaled_road_grid: Optional[np.ndarray] = None
        self.map_width = 0
        self.map_height = 0
        self.scale_factor = 1.0
        self._cached_road_positions: List[Tuple[int, int]] = []

    def load_map(self, file_path: str) -> bool:
        try:
            if not os.path.exists(file_path):
                print(f"File tidak ditemukan: {file_path}")
                return False

            pil_image = Image.open(file_path).convert('RGB')
            width, height = pil_image.size
            if not (1000 <= width <= 1500 and 700 <= height <= 1000):
                print(f"Warning: ukuran peta {width}x{height} di luar spesifikasi.")

            data = pil_image.tobytes()
            self.map_image = pygame.image.fromstring(data, (width, height), 'RGB')
            self.map_width, self.map_height = width, height

            max_w = WINDOW_WIDTH - 2 * MAP_OFFSET[0]
            max_h = WINDOW_HEIGHT - 2 * MAP_OFFSET[1]
            sx = min(1.0, max_w / width)
            sy = min(1.0, max_h / height)
            self.scale_factor = min(sx, sy)
            if self.scale_factor < 1.0:
                sw, sh = int(width * self.scale_factor), int(height * self.scale_factor)
                self.map_image = pygame.transform.scale(self.map_image, (sw, sh))

            mask = self._process_road_grid(pil_image)
            self.road_grid = mask
            self._cached_road_positions = [
                (x, y)
                for y in range(self.map_height)
                for x in range(self.map_width)
                if mask[y, x]
            ]

            sw = int(self.map_width * self.scale_factor)
            sh = int(self.map_height * self.scale_factor)
            mask_img = Image.fromarray((mask * 255).astype('uint8'))
            mask_img = mask_img.resize((sw, sh), Image.NEAREST)
            self.scaled_road_grid = (np.array(mask_img) > 0)

            print(f"Peta berhasil dimuat: {file_path} ({width}x{height})")
            return True
        except Exception as e:
            print(f"Error load map: {e}")
            return False

    def _process_road_grid(self, pil_image: Image.Image) -> np.ndarray:
        arr = np.array(pil_image)
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        mask = (
            (r >= ROAD_COLOR_MIN[0]) & (r <= ROAD_COLOR_MAX[0]) &
            (g >= ROAD_COLOR_MIN[1]) & (g <= ROAD_COLOR_MAX[1]) &
            (b >= ROAD_COLOR_MIN[2]) & (b <= ROAD_COLOR_MAX[2])
        )
        return mask

    def is_road(self, x: int, y: int) -> bool:
        if self.road_grid is None:
            return False
        if not (0 <= x < self.map_width and 0 <= y < self.map_height):
            return False
        return bool(self.road_grid[y, x])

    def get_three_random_distinct(self) -> Optional[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]:
        if len(self._cached_road_positions) < 3:
            return None
        return tuple(random.sample(self._cached_road_positions, 3))

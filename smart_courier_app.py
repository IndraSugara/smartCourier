import pygame
import sys
import os
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, MAP_OFFSET, DEFAULT_MAP_PATH, WHITE, BLACK, YELLOW, RED, GRAY
from map_processor import MapProcessor
from pathfinder import PathFinder
from courier_sprite import CourierSprite

class SmartCourierApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Smart Courier")
        self.clock = pygame.time.Clock()
        self.map = MapProcessor()
        self.pf = None
        self.courier = None
        self.source = None
        self.destination = None
        self.current_path = []
        self.path_index = 0
        self.is_animating = False
        self._setup_ui()
        self._load_default_map()

    def _setup_ui(self):
        button_x = WINDOW_WIDTH - 160
        button_y_start = 50
        button_spacing = 60
        self.buttons = {
            'load': pygame.Rect(button_x, button_y_start, 140, 40),
            'random': pygame.Rect(button_x, button_y_start + button_spacing, 140, 40),
            'start': pygame.Rect(button_x, button_y_start + 2 * button_spacing, 140, 40),
        }

    def _load_default_map(self):
        if os.path.exists(DEFAULT_MAP_PATH):
            if self.map.load_map(DEFAULT_MAP_PATH):
                self.pf = PathFinder(self.map)
                self._randomize_positions()

    def _draw_button(self, rect, text, enabled=True):
        bg = WHITE if enabled else GRAY
        fg = BLACK if enabled else (64, 64, 64)
        pygame.draw.rect(self.screen, bg, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 2)
        surf = pygame.font.Font(None, 24).render(text, True, fg)
        self.screen.blit(surf, surf.get_rect(center=rect.center))

    def _handle_load(self):
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk(); root.withdraw()
        path = filedialog.askopenfilename(
            title="Pilih Peta",
            filetypes=[("Image files", "*.png *.jpeg *.jpg *.bmp *.gif"), ("All files", "*.*")]
        )
        root.destroy()
        if path and self.map.load_map(path):
            self.pf = PathFinder(self.map)
            self._randomize_positions()

    def _randomize_positions(self):
        trio = self.map.get_three_random_distinct()
        if trio:
            self.source, self.destination, courier_pos = trio
            self.courier = CourierSprite(*courier_pos)
            self.courier.has_package = False

    def _start_pathfinding(self):
        if not all([self.pf, self.courier, self.source, self.destination]):
            return
        start = (self.courier.x, self.courier.y)
        path1 = self.pf.a_star(start, self.source)
        path2 = self.pf.a_star(self.source, self.destination)
        if not path1 or not path2:
            print("Gagal menemukan jalur.")
            return
        self.current_path = path1[1:] + path2[1:]
        self.path_index = 0
        self.is_animating = True

    def _update_animation(self):
        if not self.is_animating:
            return
        for _ in range(4):
            if self.path_index < len(self.current_path):
                nxt = self.current_path[self.path_index]
                self.courier.move_to(*nxt)
                if nxt == self.source:
                    self.courier.has_package = True
                    print("Paket diambil.")
                if nxt == self.destination:
                    self.courier.has_package = False
                    print("Paket diantar.")
                self.path_index += 1
            else:
                self.is_animating = False
                print("Selesai.")
                break

    def _handle_click(self, pos):
        for name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if name == 'load':
                    self._handle_load()
                elif name == 'random':
                    self._randomize_positions()
                elif name == 'start':
                    self._start_pathfinding()
                break

    def _draw_all(self):
        self.screen.fill(WHITE)
        if self.map.map_image:
            self.screen.blit(self.map.map_image, MAP_OFFSET)
            for pos, color in [(self.source, YELLOW), (self.destination, RED)]:
                if pos:
                    x = int(pos[0] * self.map.scale_factor) + MAP_OFFSET[0]
                    y = int(pos[1] * self.map.scale_factor) + MAP_OFFSET[1]
                    pygame.draw.circle(self.screen, color, (x, y), 8)
                    pygame.draw.circle(self.screen, BLACK, (x, y), 8, 2)
        if self.courier:
            self.courier.draw(self.screen, self.map.scale_factor, MAP_OFFSET)
        has_map = bool(self.map.map_image)
        has_pos = self.source and self.destination
        can_start = has_map and has_pos and not self.is_animating
        self._draw_button(self.buttons['load'], "Load Peta", True)
        self._draw_button(self.buttons['random'], "Acak Posisi", has_map)
        self._draw_button(self.buttons['start'], "Mulai", can_start)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self._handle_click(ev.pos)
            self._update_animation()
            self._draw_all()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

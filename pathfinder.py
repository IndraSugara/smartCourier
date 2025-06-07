import heapq
import itertools
from typing import Tuple, List, Optional
from map_processor import MapProcessor

class PathFinder:
    """Implementasi algoritma A* untuk jalur terpendek"""
    def __init__(self, mp: MapProcessor):
        self.map = mp
        self.dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self._counter = itertools.count()

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = pos
        neighbors = []
        for dx, dy in self.dirs:
            nx, ny = x + dx, y + dy
            if self.map.is_road(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def a_star(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        if start == goal:
            return [start]
        if not self.map.is_road(*start) or not self.map.is_road(*goal):
            return None

        open_heap = []
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        heapq.heappush(open_heap, (f_score[start], next(self._counter), start))
        came_from = {}
        closed = set()

        while open_heap:
            _, _, current = heapq.heappop(open_heap)
            if current in closed:
                continue
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            closed.add(current)
            for nb in self.get_neighbors(current):
                if nb in closed:
                    continue
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(nb, float('inf')):
                    came_from[nb] = current
                    g_score[nb] = tentative_g
                    f_score[nb] = tentative_g + self.heuristic(nb, goal)
                    heapq.heappush(open_heap, (f_score[nb], next(self._counter), nb))
        return None

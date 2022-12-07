import random
from collections import namedtuple


class FindRectangle:
    """
    Implementacja algorytmu do szukania pozostałych prostokątów w większym prostokącie,
    wypełnionym innymi prostokątami.
    """
    Region = namedtuple("Region", 'x1 y1 x2 y2')

    def find_rectangle(self, frame: tuple, regions: list[tuple]) -> list[tuple]:
        remaining_rectangles = []
        width, height, offset_x, offset_y = frame
        frame_r = self.Region(offset_x, offset_y, offset_x + width, offset_y + height)
        regions_r = []
        for region in regions:
            width, height, offset_x, offset_y = region
            regions_r.append(self.Region(offset_x, offset_y, offset_x + width, offset_y + height))
        for rect in self._split_rectangles(frame_r, regions_r):
            remaining_rectangles.append((rect.x2 - rect.x1, rect.y2 - rect.y1, rect.x1, rect.y1))
        return remaining_rectangles

    def _intersections(self, frame: Region, rect: Region) -> bool:
        """Sprawdza czy rect jest wewnątrz frame - True. False jeśli wyszedł poza frame."""
        return frame.x1 < rect.x2 and frame.x2 > rect.x1 and \
               frame.y1 < rect.y2 and frame.y2 > rect.y1

    def _clip_rectangle(self, frame: Region, rect: Region) -> Region:
        """Wycina prostokąt większy od rect ale mniejszy od frame"""
        return self.Region(max(frame.x1, rect.x1), max(frame.y1, rect.y1),
                           min(frame.x2, rect.x2), min(frame.y2, rect.y2))

    def _clip_rectangles(self, frame: Region, rects: list[Region]) -> list[Region]:
        """Z listy istniejacych prostokątów wycina kolejne, w ramach framea"""
        return [self._clip_rectangle(frame, r) for r in rects if self._intersections(frame, r)]

    def _split_rectangles(self, frame: Region, rects: list[Region]) -> Region:
        if frame.x1 >= frame.x2 or frame.y1 >= frame.y2:
            pass    # frame niepoprawny
        elif not rects:
            yield frame   # jeśli nie ma wewnątrz frame innych prostokątów to jedym wynikiem jest frame
        else:
            selected = random.choice(rects)
            above = self.Region(frame.x1, frame.y1, frame.x2, selected.y1)
            left = self.Region(frame.x1, selected.y1, selected.x1, selected.y2)
            right = self.Region(selected.x2, selected.y1, frame.x2, selected.y2)
            below = self.Region(frame.x1, selected.y2, frame.x2, frame.y2)
            yield from self._split_rectangles(above, self._clip_rectangles(above, rects))
            yield from self._split_rectangles(left, self._clip_rectangles(left, rects))
            yield from self._split_rectangles(right, self._clip_rectangles(right, rects))
            yield from self._split_rectangles(below, self._clip_rectangles(below, rects))


if __name__ == '__main__':
    find_rectangle = FindRectangle()
    wynik = find_rectangle.find_rectangle((10, 10, 0, 0), [(2, 2, 0, 0), (5, 5, 5, 0), (5, 5, 0, 5)])
    print(wynik)

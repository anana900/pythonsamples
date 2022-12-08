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

    def _clip_rectangles(self, frame: Region, rectangles: list[Region]) -> list[Region]:
        rectangle_list = []
        for rectangle in rectangles:
            if frame.x1 < rectangle.x2 and frame.x2 > rectangle.x1 and \
                    frame.y1 < rectangle.y2 and frame.y2 > rectangle.y1:
                rectangle_list.append(self.Region(max(frame.x1, rectangle.x1), max(frame.y1, rectangle.y1),
                                                  min(frame.x2, rectangle.x2), min(frame.y2, rectangle.y2)))
        return rectangle_list

    def _split_rectangles(self, frame: Region, rects: list[Region]) -> Region:
        if frame.x1 >= frame.x2 or frame.y1 >= frame.y2:
            pass
        elif not rects:
            yield frame
        else:
            selected = random.choice(rects)
            rectangle_above = self.Region(frame.x1, frame.y1, frame.x2, selected.y1)
            rectangle_left = self.Region(frame.x1, selected.y1, selected.x1, selected.y2)
            rectangle_right = self.Region(selected.x2, selected.y1, frame.x2, selected.y2)
            rectangle_below = self.Region(frame.x1, selected.y2, frame.x2, frame.y2)
            yield from self._split_rectangles(rectangle_above, self._clip_rectangles(rectangle_above, rects))
            yield from self._split_rectangles(rectangle_left, self._clip_rectangles(rectangle_left, rects))
            yield from self._split_rectangles(rectangle_right, self._clip_rectangles(rectangle_right, rects))
            yield from self._split_rectangles(rectangle_below, self._clip_rectangles(rectangle_below, rects))


if __name__ == '__main__':
    find_rectangle = FindRectangle()
    wynik = find_rectangle.find_rectangle((10, 10, 0, 0), [(2, 2, 0, 0), (5, 5, 5, 0), (5, 5, 0, 5)])
    print(wynik)

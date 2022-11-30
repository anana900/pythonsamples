import random
from collections import namedtuple

Rectangle = namedtuple("Rectangle", 'x1 y1 x2 y2')


class FindRectangle:
    """
    Implementacja algorytmu do szukania pozostałych prostokątów w większym prostokącie,
    wypełnionym innymi prostokątami.
    """
    def find_rectangle(self, frame: tuple, regions: list[tuple]) -> list[tuple]:
        remaining_rectangles = []
        width, height, offset_x, offset_y = frame
        frame_r = Rectangle(offset_x, offset_y, offset_x + width, offset_y + height)
        regions_r = []
        for region in regions:
            width, height, offset_x, offset_y = region
            regions_r.append(Rectangle(offset_x, offset_y, offset_x + width, offset_y + height))
        for rect in self.split_rectangles(frame_r, regions_r):
            remaining_rectangles.append((rect.x2 - rect.x1, rect.y2 - rect.y1, rect.x1, rect.y1))
        return remaining_rectangles

    def intersections(self, frame: Rectangle, rect: Rectangle) -> bool:
        """Sprawdza czy rect jest wewnątrz frame - True. False jeśli wyszedł poza frame."""
        return frame.x1 < rect.x2 and frame.x2 > rect.x1 and \
               frame.y1 < rect.y2 and frame.y2 > rect.y1

    def clip_rectangle(self, frame: Rectangle, rect: Rectangle) -> Rectangle:
        """Wycina prostokąt większy od rect ale mniejszy od frame"""
        return Rectangle(max(frame.x1, rect.x1), max(frame.y1, rect.y1),
                         min(frame.x2, rect.x2), min(frame.y2, rect.y2))

    def clip_rectangles(self, frame: Rectangle, rects: list[Rectangle]) -> list[Rectangle]:
        """Z listy istniejacych prostokątów wycina kolejne, w ramach framea"""
        return [self.clip_rectangle(frame, r) for r in rects if self.intersections(frame, r)]

    def split_rectangles(self, frame: Rectangle, rects: list[Rectangle]) -> Rectangle:
        if frame.x1 >= frame.x2 or frame.y1 >= frame.y2:
            pass    # frame niepoprawny
        elif not rects:
            yield frame   # jeśli nie ma wewnątrz frame innych prostokątów to jedym wynikiem jest frame
        else:
            selected = random.choice(rects)
            above = Rectangle(frame.x1, frame.y1, frame.x2, selected.y1)
            left = Rectangle(frame.x1, selected.y1, selected.x1, selected.y2)
            right = Rectangle(selected.x2, selected.y1, frame.x2, selected.y2)
            below = Rectangle(frame.x1, selected.y2, frame.x2, frame.y2)
            yield from self.split_rectangles(above, self.clip_rectangles(above, rects))
            yield from self.split_rectangles(left, self.clip_rectangles(left, rects))
            yield from self.split_rectangles(right, self.clip_rectangles(right, rects))
            yield from self.split_rectangles(below, self.clip_rectangles(below, rects))



if __name__ == '__main__':
    frame = Rectangle(0, 0, 10, 10)
    #              x1 y1 x2 y2
    r1 = Rectangle(0, 5, 2, 7)
    r2 = Rectangle(6, 2, 8, 4)
    rects = list()
    rects.append(r1)
    rects.append(r2)

    class Rect:
        def __init__(self, x1, y1, x2, y2):
            self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        def __repr__(self):
            return f"{self.x1} {self.y1} {self.x2} {self.y2}"

    r1 = Rect(0, 5, 2, 7)
    r2 = Rect(6, 2, 8, 4)
    rects = list()
    rects.append(r1)
    rects.append(r2)
    print(rects)

    shift_y = 0
    for y in range(10):
        if y not in set(list(range(2, 4)) + list(range(5, 7))):
            shift_y += 1
        else:
            print("odjac od wszystkich regionow ", shift_y)
            for r in rects:
                r.y1 -= shift_y
                r.y2 -= shift_y
            shift_y = 0

    print(rects)
    exit(0)

    find_rectangle = FindRectangle()
    wynik = find_rectangle.find_rectangle((10, 10, 0, 0), [(5, 5, 5, 0), (5, 5, 0, 5)])
    print(wynik)

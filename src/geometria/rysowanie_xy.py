from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from typing import Union


class Region:
    def __init__(self, width, height, offset_x, offset_y, label="", color="black"):
        self.SubRegionWidth = width
        self.SubRegionWidth_minimum = 0
        self.SubRegionWidth_maximum = 0
        self.SubRegionWidth_increment = 0
        self.SubRegionHeight = height
        self.SubRegionHeight_minimum = 0
        self.SubRegionHeight_maximum = 0
        self.SubRegionHeight_increment = 0
        self.SubRegionOffsetX = offset_x
        self.SubRegionOffsetX_minimum = 0
        self.SubRegionOffsetX_maximum = 0
        self.SubRegionOffsetX_increment = 0
        self.SubRegionOffsetY = offset_y
        self.SubRegionOffsetY_minimum = 0
        self.SubRegionOffsetY_maximum = 0
        self.SubRegionOffsetY_increment = 0
        self.label = label
        self.color = color


class MultiROI:
    def __init__(self, sensor_width: int = 0, sensor_height: int = 0,
                 colored: bool = True, lines: bool = False, hide_values: bool = True):
        self.configured_regions = list()
        self.colored = colored
        self.lines = lines
        self.hide_values = hide_values
        self.mycolors = {"green": False, "blue": False, "orange": False, "red": False}
        self.sensor_width, self.sensor_height, self.width_minimum, self.height_minimum = \
            self._sensor_parameters(sensor_width, sensor_height)

        print(f"Sensor defined: Width {self.sensor_width}, Height {self.sensor_height}, "
              f"Width_min {self.width_minimum}, Height_min {self.height_minimum}")
        scale_factor = self.sensor_width/self.sensor_height
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(8*scale_factor, 4), sharex=True, sharey=True)

    def draw_region(self, axis, width, height, offset_x, offset_y, _no, _colo) -> Region:
        #  Print Region
        axis.add_patch(Rectangle((offset_x, offset_y), width, height,
                                 label=_no, fill=None, alpha=0.5, color=_colo))
        # Print dotted lines
        if self.lines:
            axis.vlines(offset_x, 0, offset_y, linestyle="dotted", alpha=0.3, color=_colo)
            axis.hlines(offset_y, 0, offset_x, linestyle="dotted", alpha=0.3, color=_colo)
        # Print label
        axis.annotate(f"Region{_no}", (offset_x + width//2, offset_y + height//2),
                      color=_colo, weight='bold', fontsize=6, ha='center', va='center')
        region = Region(width, height, offset_x, offset_y, _no, _colo)
        return region

    def draw_configuration(self, width: Union[int, str], height: Union[int, str],
                           offset_x: Union[int, str] = 0, offset_y: Union[int, str] = 0) -> Region:
        width, height, offset_x, offset_y = self._serialise_and_trim_to_sensor(
            width, height, offset_x, offset_y)
        # Plot limits and axis
        self.ax1.set_xlim([0, self.sensor_width])
        self.ax1.set_ylim([0, self.sensor_height])
        self.ax1.invert_yaxis()
        self.ax1.xaxis.tick_top()
        if self.hide_values:
            self.ax1.axes.xaxis.set_ticklabels([0, "min_width", "", "", "", "max_width"], fontsize=6)
            self.ax1.axes.yaxis.set_ticklabels([0, "min_height", "", "", "", "max_height"], fontsize=6)
        # keep the same scale for x and y axis
        self.ax1.set_aspect('equal')
        #  Print Region
        _no, _colo = self._select_color(self.colored)
        region = self.draw_region(self.ax1, width, height, offset_x, offset_y, _no, _colo)
        self.configured_regions.append(region)
        return region

    def draw_expected(self, width: Union[int, str], height: Union[int, str],
                      offset_x: Union[int, str] = 0, offset_y: Union[int, str] = 0) -> Region:
        width, height, offset_x, offset_y = self._serialise_and_trim_to_sensor(
            width, height, offset_x, offset_y)
        # Plot limits and axis
        self.ax2.set_xlim([0, self.sensor_width])
        self.ax2.set_ylim([0, self.sensor_height])
        self.ax2.invert_yaxis()
        self.ax2.xaxis.tick_top()
        if self.hide_values:
            self.ax2.axes.xaxis.set_ticklabels([0, "min_width", "", "", "", "max_width"], fontsize=6)
            self.ax2.axes.yaxis.set_ticklabels([0, "min_height", "", "", "", "max_height"], fontsize=6)
        # keep the same scale for x and y axis
        self.ax2.set_aspect('equal')
        #  Print Region
        _no, _colo = self._select_color(self.colored)
        return self.draw_region(self.ax2, width, height, offset_x, offset_y, _no, _colo)

    def draw_multi_roi(self):
        width_sum = []
        height_sum = []
        for region in self.configured_regions:
            width_sum += list(range(region.SubRegionOffsetX, region.SubRegionOffsetX + region.SubRegionWidth))
            height_sum += list(range(region.SubRegionOffsetY, region.SubRegionOffsetY + region.SubRegionHeight))
        multi_roi_width_points = sorted(list(set(width_sum)))
        multi_roi_width = len(multi_roi_width_points)
        multi_roi_height_points = sorted(list(set(height_sum)))
        multi_roi_height = len(multi_roi_height_points)
        offset_x = multi_roi_width_points[0]
        offset_y = multi_roi_height_points[0]
        # prints output frame ROI
        _colo = "black"
        #  Print Region
        self.ax2.add_patch(Rectangle((offset_x, offset_y), multi_roi_width, multi_roi_height,
                                     linestyle="dashdot", fill=None, alpha=1, color=_colo))
        if self.lines:
            self.ax2.vlines(offset_x, 0, offset_y, linestyle="dotted", alpha=0.3, color=_colo)
            self.ax2.hlines(offset_y, 0, offset_x, linestyle="dotted", alpha=0.3, color=_colo)

    def _draw_result(self) -> None:
        # Plot limit and axis
        self.ax2.set_xlim([0, self.sensor_width])
        self.ax2.set_ylim([0, self.sensor_height])
        self.ax2.invert_yaxis()
        self.ax2.xaxis.tick_top()
        if self.hide_values:
            self.ax2.axes.xaxis.set_ticklabels([])
            self.ax2.axes.yaxis.set_ticklabels([])
        # keep the same scale for x and y axis
        self.ax2.set_aspect('equal')
        self.draw_multi_roi()

    def _serialise_and_trim_to_sensor(self, width, height, offset_x, offset_y):
        # serialise
        if width == "min":
            width = self.width_minimum
        if width == "max":
            width = self.sensor_width
        if height == "min":
            height = self.height_minimum
        if height == "max":
            height = self.sensor_height
        if offset_x == "min":
            offset_x = 0
        if offset_x == "max":
            offset_x = self.sensor_width - width
        if offset_y == "min":
            offset_y = 0
        if offset_y == "max":
            offset_y = self.sensor_height - height
        # trim
        w, h, ox, oy = width, height, offset_x, offset_y
        if width > self.sensor_width:
            w = self.sensor_width
            print(f"WARNING - clipping Width {width} -> {w}")
        if width < self.width_minimum:
            w = self.width_minimum
            print(f"WARNING - clipping Width {width} -> {w}")
        if height > self.sensor_height:
            h = self.sensor_height
            print(f"WARNING - clipping Height {height} -> {h}")
        if height < self.height_minimum:
            h = self.height_minimum
            print(f"WARNING - clipping Height {height} -> {h}")
        if offset_x < 0:
            ox = 0
            print(f"WARNING - clipping OffsetX {offset_x} -> {ox}")
        if offset_x > self.sensor_width - width:
            ox = self.sensor_width - width
            print(f"WARNING - clipping OffsetX {offset_x} -> {ox}")
        if offset_y < 0:
            oy = 0
            print(f"WARNING - clipping OffsetY {offset_y} -> {oy}")
        if offset_y > self.sensor_height - height:
            oy = self.sensor_height - height
            print(f"WARNING - clipping OffsetY {offset_y} -> {oy}")
        return w, h, ox, oy

    def _select_color(self, colored: bool) -> tuple:
        for region_no, colo in enumerate(self.mycolors):
            if not self.mycolors[colo]:
                self.mycolors[colo] = True
                colo = colo if colored else "black"
                return region_no, colo
        print("WARNING - out of defined colors. Selected black.")
        return -1, "black"

    def reset_color(self) -> None:
        self.mycolors = {"green": False, "blue": False, "orange": False, "red": False}

    @staticmethod
    def _sensor_parameters(sensor_width, sensor_height) -> tuple:
        if 20 > sensor_width >= 0 and 20 > sensor_height >= 0:
            return 100, 100, 20, 5
        elif sensor_width >= 20 and sensor_height >= 20:
            return sensor_width, sensor_height, int(sensor_width*0.2), int(sensor_height*0.05)
        else:
            raise ValueError(f"Incorrect data. Sensor dimensions must be both higher or equal to 0, "
                             f"but provided sensor_width: {sensor_width} and sensor_height: {sensor_height}")

    def enable(self):
        self._draw_result()
        plt.show()


if __name__ == '__main__':
    m = MultiROI(500, 500, lines=False, colored=False)
    Region0 = m.draw_configuration("min", "min", 60, 60)
    Region1 = m.draw_configuration("min", "min", "max", 10)
    Region2 = m.draw_configuration("min", 150, "max", 222)
    m.reset_color()
    m.draw_expected("min", "min", 60, Region1.SubRegionHeight + Region1.SubRegionOffsetY)
    m.draw_expected("min", "min", Region0.SubRegionWidth + Region0.SubRegionOffsetX, 10)
    m.draw_expected("min", 150, Region0.SubRegionWidth + Region0.SubRegionOffsetX,
                    Region1.SubRegionHeight + Region1.SubRegionOffsetY + Region0.SubRegionHeight)
    m.enable()

# # sort region by OffsetX
# region_list = sorted(region_list, key=lambda x: x.SubRegionOffsetX)
# previous_width = None
# width_shift = 0
# previous_height = None
# height_shift = 0
# for region in region_list:
#     if previous_width:
#         if region.SubRegionOffsetX > previous_width:
#             width_shift = region.SubRegionOffsetX - previous_width
#         else:
#             width_shift = 0
#     previous_width = region.SubRegionOffsetX + region.SubRegionWidth - width_shift
#     if previous_height:
#         if region.SubRegionOffsetY > previous_height:
#             height_shift = region.SubRegionOffsetY - previous_height
#         else:
#             height_shift = 0
#     previous_height = region.SubRegionOffsetY + region.SubRegionHeight - height_shift
#     self.draw_region(self.ax2, region.SubRegionWidth, region.SubRegionHeight,
#                      region.SubRegionOffsetX - width_shift,
#                      region.SubRegionOffsetY - height_shift,
#                      region.label, region.color)
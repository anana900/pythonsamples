import random

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from typing import Union
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

# screen shot https://stackoverflow.com/questions/19964345/how-to-do-a-screenshot-of-a-tkinter-application
# https://stackoverflow.com/questions/31607458/how-to-add-clipboard-support-to-matplotlib-figures


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Multiple Region Drawer")

        container = tk.Frame(self)
        container.pack()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry('800x600')

        # Button for closing
        exit_button = ttk.Button(self, text="Quit", command=lambda: exit(0))
        exit_button.pack(side=tk.TOP)

        # Sensor settings
        ttk.Label(self, text="Sensor Width").pack(side=tk.TOP)
        self.sensor_width = ttk.Entry(self)
        self.sensor_width.insert(tk.END, "500")
        self.sensor_width.bind("<Return>", self.update_sensor)
        self.sensor_width.pack()
        self.sensor_height = ttk.Entry(self)
        self.sensor_height.insert(tk.END, "500")
        self.sensor_height.bind("<Return>", self.update_sensor)
        self.sensor_height.pack()
        self.sensor_width_val = int(self.sensor_width.get())
        self.sensor_height_val = int(self.sensor_height.get())

        # Region entries
        self.r0 = ttk.Entry(self)
        self.r0.insert(tk.END, f"{self.sensor_width_val},{self.sensor_height_val},{0},{0}")
        self.r0.bind("<Return>", self.draw_charts)
        self.r0.pack()
        self.r1 = ttk.Entry(self)
        self.r1.bind("<Return>", self.draw_charts)
        self.r1.pack()
        self.r2 = ttk.Entry(self)
        self.r2.bind("<Return>", self.draw_charts)
        self.r2.pack()
        self.r3 = ttk.Entry(self)
        self.r3.bind("<Return>", self.draw_charts)
        self.r3.pack()

        # Rysowanie wykresu
        self.m = MultiROI(self.sensor_width_val, self.sensor_height_val, lines=False, colored=True)
        self.canvas = None
        container.pack()
        self.draw_charts()

        self.mainloop()

    def draw_charts(self, *args):
        # Clean charts before update
        self.m.ax1.clear()
        self.m.ax2.clear()
        self.m.expected_regions = []
        self.m.configured_regions = []
        # Draw region configuration
        region_raw_list = [self.r0.get(), self.r1.get(), self.r2.get(), self.r3.get()]
        for index, region_raw in enumerate(region_raw_list):
            if region_raw:
                w, h, ox, oy, *_ = [int(item) for item in region_raw.split(',')]
                self.m.draw_configuration(w, h, ox, oy, f"Region{index}")
        # Draw region results
        self.m.find_expected_regions_position(self.m.configured_regions)
        for rr in self.m.expected_regions:
            self.m.draw_expected(rr.SubRegionWidth, rr.SubRegionHeight, rr.SubRegionOffsetX, rr.SubRegionOffsetY, rr.label)
        self.m.draw_result()
        # handle graph presentation
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()
        self.canvas = FigureCanvasTkAgg(self.m.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        #plt.savefig('plot.png', dpi=120, bbox_inches='tight')

    def update_sensor(self, *args):
        self.sensor_width_val = int(self.sensor_width.get())
        self.sensor_height_val = int(self.sensor_height.get())
        del self.m
        self.m = MultiROI(self.sensor_width_val, self.sensor_height_val, lines=False, colored=True)
        self.draw_charts()


class Region:
    def __init__(self, width, height, offset_x, offset_y, label=""):
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

    def __repr__(self):
        return f"{self.SubRegionWidth} {self.SubRegionHeight} {self.SubRegionOffsetX} {self.SubRegionOffsetY}"


class MultiROI:
    FONT_SIZE = 6
    FRAME_WIDTH = 8
    FRAME_HEIGHT = 4

    def __init__(self, sensor_width: int = 0, sensor_height: int = 0,
                 colored: bool = True, lines: bool = False, hide_values: bool = True):
        self.configured_regions = list()
        self.expected_regions = list()
        self.colored = colored
        self.lines = lines
        self.hide_values = hide_values
        self.region_colors = {"Region0": "green", "Region1": "blue", "Region2": "orange", "Region3": "red"}
        self.sensor_width, self.sensor_height, self.width_minimum, self.height_minimum = \
            self._sensor_parameters(sensor_width, sensor_height)

        print(f"Sensor defined: Width {self.sensor_width}, Height {self.sensor_height}, "
              f"Width_min {self.width_minimum}, Height_min {self.height_minimum}")
        scale_factor = self.sensor_width/self.sensor_height
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(self.FRAME_WIDTH*scale_factor, self.FRAME_HEIGHT),
                                                      sharex=True, sharey=True)

    def _draw_region(self, axis, region: Region) -> None:
        if region.label in self.region_colors:
            _colo = self.region_colors[region.label]
        else:
            _colo = "black"
        _label = region.label
        #  Print Region
        axis.add_patch(Rectangle((region.SubRegionOffsetX, region.SubRegionOffsetY),
                                 region.SubRegionWidth, region.SubRegionHeight,
                                 label=_label, fill=None, alpha=0.5, color=_colo))
        # Print dotted lines
        if self.lines:
            axis.vlines(region.SubRegionOffsetX, 0, region.SubRegionOffsetY, linestyle="dotted", alpha=0.3, color=_colo)
            axis.hlines(region.SubRegionOffsetY, 0, region.SubRegionOffsetX, linestyle="dotted", alpha=0.3, color=_colo)
        # Print label
        axis.annotate(region.label, (region.SubRegionOffsetX + region.SubRegionWidth//2,
                                     region.SubRegionOffsetY + region.SubRegionHeight//2),
                      color=_colo, weight='bold', fontsize=self.FONT_SIZE, ha='center', va='center')

    def draw_configuration(self, width: Union[int, str], height: Union[int, str],
                           offset_x: Union[int, str] = 0, offset_y: Union[int, str] = 0, label="") -> None:
        width, height, offset_x, offset_y = self._serialise_and_trim_to_sensor(width, height, offset_x, offset_y)
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
        _region = Region(width, height, offset_x, offset_y, label)
        self._draw_region(self.ax1, _region)
        self.configured_regions.append(_region)

    def draw_expected(self, width: Union[int, str], height: Union[int, str],
                      offset_x: Union[int, str] = 0, offset_y: Union[int, str] = 0, label="") -> None:
        width, height, offset_x, offset_y = self._serialise_and_trim_to_sensor(width, height, offset_x, offset_y)
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
        _region = Region(width, height, offset_x, offset_y, label)
        self._draw_region(self.ax2, _region)

    def draw_expected_roi(self):
        width_sum = []
        height_sum = []
        if self.expected_regions:
            for region in self.expected_regions:
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
                                         linestyle="dashdot", fill=None, hatch='//', alpha=1, color=_colo))
            if self.lines:
                self.ax2.vlines(offset_x, 0, offset_y, linestyle="dotted", alpha=0.3, color=_colo)
                self.ax2.hlines(offset_y, 0, offset_x, linestyle="dotted", alpha=0.3, color=_colo)

    def draw_result(self) -> None:
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
        self.draw_expected_roi()

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

    @staticmethod
    def _sensor_parameters(sensor_width, sensor_height) -> tuple:
        if 20 > sensor_width >= 0 and 20 > sensor_height >= 0:
            return 100, 100, 20, 5
        elif sensor_width >= 20 and sensor_height >= 20:
            return sensor_width, sensor_height, int(sensor_width*0.2), int(sensor_height*0.05)
        else:
            raise ValueError(f"Incorrect data. Sensor dimensions must be both higher or equal to 0, "
                             f"but provided sensor_width: {sensor_width} and sensor_height: {sensor_height}")

    def _get_offset_y_as_set(self, regions: list) -> set:
        total_height_list = []
        height_lists = [list(range(r.SubRegionOffsetY, r.SubRegionOffsetY + r.SubRegionHeight)) for r in regions]
        for height_list in height_lists:
            total_height_list += height_list
        return set(total_height_list)

    def _get_offset_x_as_set(self, regions: list) -> set:
        total_width_list = []
        width_lists = [list(range(r.SubRegionOffsetX, r.SubRegionOffsetX + r.SubRegionWidth)) for r in regions]
        for width_list in width_lists:
            total_width_list += width_list
        return set(total_width_list)

    def find_expected_regions_position(self, regions: list) -> None:
        new_regions = []
        new_regions_final = []
        if len(regions) > 1:
            regions_sorted_by_offset_y = sorted(regions, key=lambda region: region.SubRegionOffsetY)
            sum_of_offset_x_shifts = 0
            sum_of_offset_y_shifts = 0
            height_set = self._get_offset_y_as_set(regions)
            new_regions.append(regions_sorted_by_offset_y[0])
            for r_first, r_second in zip(regions_sorted_by_offset_y[:-1], regions_sorted_by_offset_y[1:]):
                if r_first.SubRegionHeight + r_first.SubRegionOffsetY < r_second.SubRegionOffsetY \
                        and not height_set & set(list(range(r_first.SubRegionHeight + r_first.SubRegionOffsetY, r_second.SubRegionOffsetY))):
                    rr = Region(r_second.SubRegionWidth, r_second.SubRegionHeight, r_second.SubRegionOffsetX,
                                r_first.SubRegionHeight + r_first.SubRegionOffsetY - sum_of_offset_y_shifts, r_second.label)
                    y = (r_second.SubRegionOffsetY - (r_first.SubRegionHeight + r_first.SubRegionOffsetY))
                    sum_of_offset_y_shifts += y
                    new_regions.append(rr)
                else:
                    rr = Region(r_second.SubRegionWidth, r_second.SubRegionHeight, r_second.SubRegionOffsetX,
                                r_second.SubRegionOffsetY - sum_of_offset_y_shifts, r_second.label)
                    new_regions.append(rr)

            regions_sorted_by_offset_x = sorted(new_regions, key=lambda region: region.SubRegionOffsetX)
            width_set = self._get_offset_x_as_set(regions_sorted_by_offset_x)
            new_regions_final.append(regions_sorted_by_offset_x[0])
            for r_first, r_second in zip(regions_sorted_by_offset_x[:-1], regions_sorted_by_offset_x[1:]):
                if r_first.SubRegionWidth + r_first.SubRegionOffsetX < r_second.SubRegionOffsetX \
                        and not width_set & set(list(range(r_first.SubRegionWidth + r_first.SubRegionOffsetX, r_second.SubRegionOffsetX))):
                    rr = Region(r_second.SubRegionWidth, r_second.SubRegionHeight,
                                r_first.SubRegionWidth + r_first.SubRegionOffsetX - sum_of_offset_x_shifts,
                                r_second.SubRegionOffsetY, r_second.label)
                    x = (r_second.SubRegionOffsetX - (r_first.SubRegionWidth + r_first.SubRegionOffsetX))
                    sum_of_offset_x_shifts += x
                    new_regions_final.append(rr)
                else:
                    rr = Region(r_second.SubRegionWidth, r_second.SubRegionHeight,
                                r_second.SubRegionOffsetX - sum_of_offset_x_shifts, r_second.SubRegionOffsetY, r_second.label)
                    new_regions_final.append(rr)
        else:
            new_regions_final = regions
        self.expected_regions = new_regions_final


if __name__ == '__main__':
    app = MainApp()

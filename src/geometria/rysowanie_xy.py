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
                w, h, ox, oy, *_ = [item.strip().lower() for item in region_raw.split(',')]
                w, h, ox, oy = self.m.serialise_and_trim_to_sensor(w, h, ox, oy)
                self.m.draw_configuration(w, h, ox, oy, f"Region{index}")
        # Draw region results
        self.m.find_expected_regions_position(self.m.configured_regions)
        for rr in self.m.expected_regions:
            self.m.draw_expected(rr.Width, rr.Height, rr.OffsetX, rr.OffsetY, rr.label)
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
        self.Width = width
        self.Width_minimum = 0
        self.Width_maximum = 0
        self.Width_increment = 0
        self.Height = height
        self.Height_minimum = 0
        self.Height_maximum = 0
        self.Height_increment = 0
        self.OffsetX = offset_x
        self.OffsetX_minimum = 0
        self.OffsetX_maximum = 0
        self.OffsetX_increment = 0
        self.OffsetY = offset_y
        self.OffsetY_minimum = 0
        self.OffsetY_maximum = 0
        self.OffsetY_increment = 0
        self.label = label

    def __repr__(self):
        return f"{self.Width} {self.Height} {self.OffsetX} {self.OffsetY}"


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
        axis.add_patch(Rectangle((region.OffsetX, region.OffsetY),
                                 region.Width, region.Height,
                                 label=_label, fill=None, alpha=0.5, color=_colo))
        # Print dotted lines
        if self.lines:
            axis.vlines(region.OffsetX, 0, region.OffsetY, linestyle="dotted", alpha=0.3, color=_colo)
            axis.hlines(region.OffsetY, 0, region.OffsetX, linestyle="dotted", alpha=0.3, color=_colo)
        # Print label
        axis.annotate(region.label, (region.OffsetX + region.Width//2,
                                     region.OffsetY + region.Height//2),
                      color=_colo, weight='bold', fontsize=self.FONT_SIZE, ha='center', va='center')

    def draw_configuration(self, width: Union[int, str], height: Union[int, str],
                           offset_x: Union[int, str] = 0, offset_y: Union[int, str] = 0, label="") -> None:
        width, height, offset_x, offset_y = self.serialise_and_trim_to_sensor(width, height, offset_x, offset_y)
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
        width, height, offset_x, offset_y = self.serialise_and_trim_to_sensor(width, height, offset_x, offset_y)
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
                width_sum += list(range(region.OffsetX, region.OffsetX + region.Width))
                height_sum += list(range(region.OffsetY, region.OffsetY + region.Height))
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

    def serialise_and_trim_to_sensor(self, width, height, offset_x, offset_y) -> tuple:
        if isinstance(width, str):
            if width == "min":
                width = self.width_minimum
            elif width == "max":
                width = self.sensor_width
            else:
                width = int(width)
        if isinstance(height, str):
            if height == "min":
                height = self.height_minimum
            elif height == "max":
                height = self.sensor_height
            else:
                height = int(height)
        if isinstance(offset_x, str):
            if offset_x == "min":
                offset_x = 0
            elif offset_x == "max":
                offset_x = self.sensor_width - width
            else:
                offset_x = int(offset_x)
        if isinstance(offset_y, str):
            if offset_y == "min":
                offset_y = 0
            elif offset_y == "max":
                offset_y = self.sensor_height - height
            else:
                offset_y = int(offset_y)
        return width, height, offset_x, offset_y

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
        height_lists = [list(range(r.OffsetY, r.OffsetY + r.Height)) for r in regions]
        for height_list in height_lists:
            total_height_list += height_list
        return set(total_height_list)

    def _get_offset_x_as_set(self, regions: list) -> set:
        total_width_list = []
        width_lists = [list(range(r.OffsetX, r.OffsetX + r.Width)) for r in regions]
        for width_list in width_lists:
            total_width_list += width_list
        return set(total_width_list)

    def find_expected_regions_position(self, regions: list) -> None:
        new_regions = []
        new_regions_final = []
        if len(regions) > 1:
            regions_sorted_by_offset_y = sorted(regions, key=lambda region: region.OffsetY)
            sum_of_offset_x_shifts = 0
            sum_of_offset_y_shifts = 0
            height_set = self._get_offset_y_as_set(regions)
            new_regions.append(regions_sorted_by_offset_y[0])
            for r_first, r_second in zip(regions_sorted_by_offset_y[:-1], regions_sorted_by_offset_y[1:]):
                if r_first.Height + r_first.OffsetY < r_second.OffsetY \
                        and not height_set & set(list(range(r_first.Height + r_first.OffsetY, r_second.OffsetY))):
                    rr = Region(r_second.Width, r_second.Height, r_second.OffsetX,
                                r_first.Height + r_first.OffsetY - sum_of_offset_y_shifts, r_second.label)
                    y = (r_second.OffsetY - (r_first.Height + r_first.OffsetY))
                    sum_of_offset_y_shifts += y
                    new_regions.append(rr)
                else:
                    rr = Region(r_second.Width, r_second.Height, r_second.OffsetX,
                                r_second.OffsetY - sum_of_offset_y_shifts, r_second.label)
                    new_regions.append(rr)

            regions_sorted_by_offset_x = sorted(new_regions, key=lambda region: region.OffsetX)
            width_set = self._get_offset_x_as_set(regions_sorted_by_offset_x)
            new_regions_final.append(regions_sorted_by_offset_x[0])
            for r_first, r_second in zip(regions_sorted_by_offset_x[:-1], regions_sorted_by_offset_x[1:]):
                if r_first.Width + r_first.OffsetX < r_second.OffsetX \
                        and not width_set & set(list(range(r_first.Width + r_first.OffsetX, r_second.OffsetX))):
                    rr = Region(r_second.Width, r_second.Height,
                                r_first.Width + r_first.OffsetX - sum_of_offset_x_shifts,
                                r_second.OffsetY, r_second.label)
                    x = (r_second.OffsetX - (r_first.Width + r_first.OffsetX))
                    sum_of_offset_x_shifts += x
                    new_regions_final.append(rr)
                else:
                    rr = Region(r_second.Width, r_second.Height,
                                r_second.OffsetX - sum_of_offset_x_shifts, r_second.OffsetY, r_second.label)
                    new_regions_final.append(rr)
        else:
            new_regions_final = regions
        self.expected_regions = new_regions_final


if __name__ == '__main__':
    app = MainApp()

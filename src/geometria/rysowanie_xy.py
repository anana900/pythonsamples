from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from typing import Union
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

# screen shot https://stackoverflow.com/questions/19964345/how-to-do-a-screenshot-of-a-tkinter-application
# https://stackoverflow.com/questions/31607458/how-to-add-clipboard-support-to-matplotlib-figures

DEFAULT_SENSOR_SIZE = ("820", "640")
SCALE_FACTOR = False
MENU_BUTTON_WIDTH = 8


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Multiple Region Drawer")
        self.geometry(f"{DEFAULT_SENSOR_SIZE[0]}x{DEFAULT_SENSOR_SIZE[1]}")

        font_settings = tk.font.Font(family='Arial', size=8, weight='bold')
        region_help = tk.StringVar()
        region_help.set('Format: Width, Height, OffsetX, OffsetY. Accept min, max')

        # Button for refresh
        reload_button = tk.Button(self, text="Reload", width=MENU_BUTTON_WIDTH, font=font_settings, command=self.draw_charts)
        reload_button.grid(row=5, column=8, rowspan=1, columnspan=1, sticky=tk.E)

        # Button for cleaning
        clean_button = tk.Button(self, text="Clear", width=MENU_BUTTON_WIDTH, font=font_settings, command=self.clear)
        clean_button.grid(row=3, column=8, rowspan=1, columnspan=1, sticky=tk.E)

        # Button for closing
        exit_button = tk.Button(self, text="Quit", width=MENU_BUTTON_WIDTH, font=font_settings, command=lambda: exit(0))
        exit_button.grid(row=2, column=8, rowspan=1, columnspan=1, sticky=tk.E)

        # Button for copy
        cpy_button = tk.Button(self, text="Copy", width=MENU_BUTTON_WIDTH, font=font_settings, command=self.copy_image)
        cpy_button.grid(row=4, column=8, rowspan=1, columnspan=1, sticky=tk.E)

        # Checkbox for resizing
        self._scale = tk.BooleanVar()
        check_factor = tk.Checkbutton(self, text='Resize Plots', variable=self._scale,
                                      onvalue=True, offvalue=False, command=self.set_scale_factor)
        check_factor.grid(row=2, column=4)
        if SCALE_FACTOR:
            check_factor.select()

        # Sensor settings
        lab_width_max = tk.Label(self, text="Sensor Width")
        lab_width_max.grid(row=2, column=0, sticky=tk.W)
        self.sensor_width = tk.Entry(self)
        self.sensor_width.insert(tk.END, DEFAULT_SENSOR_SIZE[0])
        self.sensor_width.bind("<Return>", self.update_sensor)
        self.sensor_width.grid(row=2, column=1, sticky=tk.W)
        lab_height_max = tk.Label(self, text="Sensor Height")
        lab_height_max.grid(row=3, column=0, sticky=tk.W)
        self.sensor_height = tk.Entry(self)
        self.sensor_height.insert(tk.END, DEFAULT_SENSOR_SIZE[1])
        self.sensor_height.bind("<Return>", self.update_sensor)
        self.sensor_height.grid(row=3, column=1, sticky=tk.W)

        self.sensor_width_val = int(self.sensor_width.get())
        self.sensor_height_val = int(self.sensor_height.get())

        # Info
        lab_info = tk.Label(self, textvariable=region_help, font=("Arial", 8))
        lab_info.grid(row=4, column=1, columnspan=2, sticky=tk.SW)

        # Region entries
        r_gap_width = 35
        lab_r0 = tk.Label(self, text="Region0 config")
        lab_r0.grid(row=5, column=0, sticky=tk.W)
        self.r0 = tk.Entry(self, width=r_gap_width)
        self.r0.insert(tk.END, f"{self.sensor_width_val//8},{self.sensor_height_val//8},{0},{0}")
        self.r0.bind("<Return>", self.draw_charts)
        self.r0.grid(row=5, column=1,  columnspan=2, sticky=tk.W)
        tk.Button(self, text="x", height=1, width=1, font=font_settings,
                  command=lambda: self.r0.delete(0, tk.END)).grid(row=5, column=3, sticky=tk.W)

        lab_r1 = tk.Label(self, text="Region1 config")
        lab_r1.grid(row=6, column=0, sticky=tk.W)
        self.r1 = tk.Entry(self, width=r_gap_width)
        self.r1.insert(tk.END, f"{self.sensor_width_val//8},{self.sensor_height_val//8},"
                               f"{self.sensor_width_val//4},{self.sensor_height_val//4}")
        self.r1.bind("<Return>", self.draw_charts)
        self.r1.grid(row=6, column=1,  columnspan=2, sticky=tk.W)
        tk.Button(self, text="x", height=1, width=1, font=font_settings,
                  command=lambda: self.r1.delete(0, tk.END)).grid(row=6, column=3, sticky=tk.W)

        lab_r2 = tk.Label(self, text="Region2 config")
        lab_r2.grid(row=7, column=0, sticky=tk.W)
        self.r2 = tk.Entry(self, width=r_gap_width)
        self.r2.bind("<Return>", self.draw_charts)
        self.r2.grid(row=7, column=1,  columnspan=2, sticky=tk.W)
        tk.Button(self, text="x", height=1, width=1, font=font_settings,
                  command=lambda: self.r2.delete(0, tk.END)).grid(row=7, column=3, sticky=tk.W)

        lab_r3 = tk.Label(self, text="Region3 config")
        lab_r3.grid(row=8, column=0, sticky=tk.W)
        self.r3 = tk.Entry(self, width=r_gap_width)
        self.r3.bind("<Return>", self.draw_charts)
        self.r3.grid(row=8, column=1,  columnspan=2, sticky=tk.W)
        tk.Button(self, text="x", height=1, width=1, font=font_settings,
                  command=lambda: self.r3.delete(0, tk.END)).grid(row=8, column=3, sticky=tk.W)

        # Rysowanie wykresu
        self.m = MultiROI(self.sensor_width_val, self.sensor_height_val, lines=False, colored=True)
        self.canvas = None
        self.draw_charts()
        self.mainloop()

    def set_scale_factor(self):
        global SCALE_FACTOR
        if self._scale.get():
            SCALE_FACTOR = True
        else:
            SCALE_FACTOR = False

    def copy_image(self):
        self.canvas.postscript(file="file_name.ps", colormode='color')

    def clear(self):
        self.r0.delete(0, tk.END)
        self.r1.delete(0, tk.END)
        self.r2.delete(0, tk.END)
        self.r3.delete(0, tk.END)
        self.draw_charts()

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
            self.m.draw_expected(rr.SubRegionWidth, rr.SubRegionHeight, rr.SubRegionOffsetX, rr.SubRegionOffsetY, rr.label)
        self.m.draw_result()

        if self.canvas:
            FigureCanvasTkAgg(None, self)
            del self.canvas
            #self.canvas.get_tk_widget().pack_forget()

        self.canvas = FigureCanvasTkAgg(self.m.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=9, column=0, columnspan=10, sticky=tk.W)

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
        scale_factor = self.sensor_width / self.sensor_height if SCALE_FACTOR else 1
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(self.FRAME_WIDTH*scale_factor, self.FRAME_HEIGHT),
                                                      sharex="all", sharey="all")
        self.fig.tight_layout()

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
        # TODO zmienić na konfigurowalne z opcja dodania min, max w GUI
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
            sum_of_offset_x_shifts = 0
            sum_of_offset_y_shifts = 0
            regions_sorted_by_offset_y = sorted(regions, key=lambda region: region.SubRegionOffsetY)
            height_set = self._get_offset_y_as_set(regions)
            new_regions.append(regions_sorted_by_offset_y[0])
            for r_first, r_second in zip(regions_sorted_by_offset_y[:-1], regions_sorted_by_offset_y[1:]):
                if r_first.SubRegionHeight + r_first.SubRegionOffsetY < r_second.SubRegionOffsetY:
                    r_first_r_second_diff = set(list(range(r_first.SubRegionHeight + r_first.SubRegionOffsetY,
                                                           r_second.SubRegionOffsetY)))
                    offset_y = len(list(height_set ^ (height_set | r_first_r_second_diff)))
                    sum_of_offset_y_shifts += offset_y
                new_regions.append(Region(r_second.SubRegionWidth, r_second.SubRegionHeight, r_second.SubRegionOffsetX,
                                          r_second.SubRegionOffsetY - sum_of_offset_y_shifts, r_second.label))

            regions_sorted_by_offset_x = sorted(new_regions, key=lambda region: region.SubRegionOffsetX)
            width_set = self._get_offset_x_as_set(regions_sorted_by_offset_x)
            new_regions_final.append(regions_sorted_by_offset_x[0])
            for r_first, r_second in zip(regions_sorted_by_offset_x[:-1], regions_sorted_by_offset_x[1:]):
                if r_first.SubRegionWidth + r_first.SubRegionOffsetX < r_second.SubRegionOffsetX:
                    r_first_r_second_diff = set(list(range(r_first.SubRegionWidth + r_first.SubRegionOffsetX,
                                                           r_second.SubRegionOffsetX)))
                    offset_x = len(list(width_set ^ (width_set | r_first_r_second_diff)))
                    sum_of_offset_x_shifts += offset_x
                new_regions_final.append(Region(r_second.SubRegionWidth, r_second.SubRegionHeight,
                                                r_second.SubRegionOffsetX - sum_of_offset_x_shifts,
                                                r_second.SubRegionOffsetY, r_second.label))
        else:
            new_regions_final = regions
        self.expected_regions = new_regions_final


if __name__ == '__main__':
    app = MainApp()

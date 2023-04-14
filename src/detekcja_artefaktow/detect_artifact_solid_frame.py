import os
import time
from typing import Union

import cv2
import numpy as np


class DetectArtifact:
    """
    2-shape-array - (shape0,shape1)
    (00) (01) (02) (03)
    (10) (11) (12) (13)
    (20) (21) (22) (23)
    (30) (31) (32) (33)
    """
    def __init__(self, max_split_factor_0: int = 32, max_split_factor_1: int = 32, debug: bool = False,
                 video: bool = False) -> None:
        self.artifact_image = None
        self.max_split_factor_0 = max_split_factor_0    # Maximum number of sections on Y axis
        self.max_split_factor_1 = max_split_factor_1    # Maximum number of sections on X axis
        self.debug = debug
        self.video = video
        if self.video:
            cv2.namedWindow('video', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('video', 1600, 800)

    def __del__(self) -> None:
        cv2.destroyAllWindows()

    @staticmethod
    def __convert_pixel_format_and_shape(frame_shape_3) -> np.ndarray:
        if type(frame_shape_3) != np.ndarray:
            if frame_shape_3.PixelFormat != "Mono8":
                frame_shape_3.convert_pixel_format("Mono8")
            frame_shape_3 = frame_shape_3.get_data_as_numpy_array()
        return frame_shape_3.reshape(frame_shape_3.shape[0], frame_shape_3.shape[1])

    def detect_border_artefact(self, frame_shape_2: np.ndarray, border_threshold: float = 0.1):
        border = []
        frame_average = np.average(frame_shape_2)
        shape_0, shape_1 = frame_shape_2.shape
        border.extend(frame_shape_2[0])                                         # top
        border.extend(frame_shape_2[shape_0 - 1])                               # bottom
        border.extend((frame_shape_2[x][0] for x in range(shape_0)))            # left
        border.extend((frame_shape_2[x][shape_1-1] for x in range(shape_0)))    # right
        border_average = np.average(border)
        difference = abs(frame_average - border_average)
        self.log(f"Frame average {frame_average}, border average {border_average}, difference {difference}")
        if difference > border_threshold:
            return True
        return False

    def detect_artifact_in_solid_numpy_frame(self, frame_shape_3,
                                             reference_frame_shape_3 = None,
                                             region_average_threshold: float = 0.1 * 255,
                                             canny_average_threshold: float = 0.5,
                                             canny_min: int = 70, canny_max: int = 90) -> tuple:
        t_start_ns = time.perf_counter_ns()
        # Convert 3 dimension array to 2 dimension array
        numpy_frame = self.__convert_pixel_format_and_shape(frame_shape_3)
        # Differential defect detection
        if not isinstance(reference_frame_shape_3, type(None)):
            reference_numpy_frame = self.__convert_pixel_format_and_shape(reference_frame_shape_3)
            cv2.absdiff(numpy_frame, reference_numpy_frame, numpy_frame)
        prepare_frame_ns = round((time.perf_counter_ns() - t_start_ns) * 1e-6, 2)

        #####################################################################################################
        # Stage0 Detect border artefacts
        #####################################################################################################
        border_artefact = self.detect_border_artefact(numpy_frame)

        #####################################################################################################
        # Stage1 Canny
        #####################################################################################################
        t_start_ns = time.perf_counter_ns()
        canny_edges = cv2.Canny(numpy_frame, canny_min, canny_max)
        canny_average = np.average(canny_edges)
        decision_canny_average = canny_average > canny_average_threshold
        canny_time_ns = round((time.perf_counter_ns() - t_start_ns) * 1e-6, 2)

        #####################################################################################################
        # Stage2 Regions
        #####################################################################################################
        # Split captured frame (array) into smaller regions (arrays)
        # Total number of regions = split_factor_0 * split_factor_1
        t_start_ns = time.perf_counter_ns()
        sub_numpy_frame_list = []
        split_factor_0 = self.max_split_factor_0
        split_factor_1 = self.max_split_factor_1
        # Adjust split factor with sensor and ROI settings
        # Split factors adjustment is necessary as np split can only produce equal sub arrays
        while numpy_frame.shape[0] % split_factor_0 != 0:
            split_factor_0 -= 1
            self.log(f"split_factor_0 changed from {split_factor_0 + 1} to {split_factor_0}")
        while numpy_frame.shape[1] % split_factor_1 != 0:
            split_factor_1 -= 1
            self.log(f"split_factor_1 changed from {split_factor_1 + 1} to {split_factor_1}")
        numpy_frame_0 = np.split(numpy_frame, split_factor_0, axis=0)
        for numpy_frame_0_item in numpy_frame_0:
            numpy_frame_1 = np.split(numpy_frame_0_item, split_factor_1, axis=1)
            for _numpy_frame in numpy_frame_1:
                sub_numpy_frame_list.append(_numpy_frame)
        # Calculate average value of each array
        average_sub_numpy_frame_list = []
        for sub_numpy_frame in sub_numpy_frame_list:
            average_sub_numpy_frame_list.append(np.average(sub_numpy_frame))
        sub_average_min = min(average_sub_numpy_frame_list)
        sub_average_max = max(average_sub_numpy_frame_list)
        sub_average_diff = sub_average_max - sub_average_min
        decision_sub_frames_average = sub_average_diff > region_average_threshold

        if decision_sub_frames_average and numpy_frame.shape[0] > 40 and numpy_frame.shape[1] > 40:
            # Mark artefacts
            sub_average_min_index = average_sub_numpy_frame_list.index(min(average_sub_numpy_frame_list))
            sub_average_max_index = average_sub_numpy_frame_list.index(max(average_sub_numpy_frame_list))
            col_max = sub_average_max_index % split_factor_1
            row_max = sub_average_max_index // split_factor_1
            col_min = sub_average_min_index % split_factor_1
            row_min = sub_average_min_index // split_factor_1
            height = numpy_frame.shape[0] // split_factor_0
            width = numpy_frame.shape[1] // split_factor_1
            thickness = 1 + numpy_frame.shape[0]//1000 + numpy_frame.shape[1]//1000
            self.log(f"Region min max positions col_max {col_max} row_max {row_max} col_min {col_min} "
                     f"row_min {row_min} height {height} width {width} sub_average_max_index "
                     f"{sub_average_max_index} max val {sub_average_max} "
                     f"sub_average_min_index {sub_average_min_index} min val {sub_average_min}")
            cv2.rectangle(numpy_frame, (col_max*width, row_max*height), ((col_max+1)*width, (row_max+1)*height),
                          (50, 0, 50), thickness=thickness)
            cv2.rectangle(numpy_frame, (col_min*width, row_min*height), ((col_min+1)*width, (row_min+1)*height),
                          (200, 0, 200), thickness=thickness)
        sub_frame_time_ns = round((time.perf_counter_ns() - t_start_ns) * 1e-6, 2)

        #####################################################################################################
        #  Make a decision about artifacts
        #####################################################################################################
        time_taken_ns = round(canny_time_ns + sub_frame_time_ns + prepare_frame_ns, 2)
        self.log(f"Detection time {time_taken_ns} [ms] (prepare {prepare_frame_ns} canny {canny_time_ns} "
                 f"region {sub_frame_time_ns})\nCanny decision {decision_canny_average} "
                 f"(value measured {canny_average}, threshold {canny_average_threshold})\n"
                 f"Sub frame decision {decision_sub_frames_average} (value measured {sub_average_diff}, "
                 f"threshold {region_average_threshold})")
        decision = border_artefact and (decision_sub_frames_average or decision_canny_average)
        self.artifact_image = np.concatenate((numpy_frame, canny_edges), axis=1)
        if self.video:
            cv2.imshow('video', self.artifact_image)
            cv2.waitKey(20)     # ms
        return decision, sub_average_diff, canny_average, time_taken_ns

    def log(self, data_to_log: str) -> None:
        if self.debug:
            print(f"{self.__class__.__name__} {data_to_log}")

    def save_frame_as_image(self, save_path: str = "", file_name: str = "") -> None:
        timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")
        os.makedirs(save_path, exist_ok=True)
        result_path = os.path.join(save_path, f"{timestamp}_{file_name}.png")
        cv2.imwrite(result_path, self.artifact_image)

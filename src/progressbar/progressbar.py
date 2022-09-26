import io
import sys
import unittest.mock


def progress_v1(max_number: int, current_number: int) -> None:
    """
    Prints following progress bar:
    Processing 100 [%] [####...#]
    """
    max_percent = 100
    current_percent = int(max_percent * current_number / max_number)
    end_line = '\r' if current_percent < max_percent else '\n'
    print(f"Processing {current_percent} [%] [{'#'*current_percent}{' '*(max_percent-current_percent)}]",
          end=end_line, flush=True)


def progress_v2(max_number: int, current_number: int, factor: float = 1) -> None:
    """Prints following progress bar:
    | 100 [%] [####...#]
    + spinner
    + factor allowing to modify length of the bar: 1 - 100 points, < 1 - shorter, > 1 - longer
    """
    max_percent = 100
    current_percent = int(max_percent * current_number / max_number)
    spinner = ['|', '/', '-', '\\']
    if current_percent < max_percent:
        show_spin = spinner[current_number % 4]
        end_line = '\r'
    else:
        show_spin = " "
        end_line = '\n'
    print(f"{show_spin} {current_percent} [%] "
          f"[{'#'*int(current_percent*factor)}{' '*int((max_percent-current_percent)*factor)}]",
          end=end_line, flush=True)


class Spinner(unittest.TestCase):
    """
    To run test simply execute in console: python progressbar.py
    """

    """
    Tests using the StringIO object to redirect and capture stdout.
    """
    def test_progress_v1_test(self) -> None:
        progress_completed = 100
        for progress in range(progress_completed + 1):
            # Each time create new StringIO object, just one for each line.
            self.string_to_capture = io.StringIO()
            sys.stdout = self.string_to_capture
            progress_v1(progress_completed, progress)
            printed_data = self.string_to_capture.getvalue()
            counter = printed_data.count("#")
            with self.subTest():
                self.assertEqual(counter, progress*(100/progress_completed),
                                 f"{counter} {progress} {printed_data}")
            # Delete the IO object as cleaning procedure before reading next progress status
            sys.stdout = sys.__stdout__

    def test_progress_v2_test(self) -> None:
        progress_completed = 100
        for progress in range(progress_completed + 1):
            # Each time create new StringIO object, just one for each line.
            self.string_to_capture = io.StringIO()
            sys.stdout = self.string_to_capture
            progress_v2(progress_completed, progress)
            printed_data = self.string_to_capture.getvalue()
            counter = printed_data.count("#")
            with self.subTest():
                self.assertEqual(counter, progress*(100/progress_completed),
                                 f"{counter} {progress} {printed_data}")
            # Delete the IO object as cleaning procedure before reading next progress status
            sys.stdout = sys.__stdout__

    """
    Tests using unittests mocks patch and StringIO.
    """
    @unittest.mock.patch('sys.stderr', new_callable=io.StringIO)
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_progress_v1_test_mock(self, mock_out, mock_err) -> None:
        progress_completed = 2
        for progress in range(progress_completed + 1):
            progress_v1(progress_completed, progress)
            printed_data_stdout = mock_out.getvalue()
            printed_data_stderr = mock_err.getvalue()
            counter = printed_data_stdout.count("#")
            with self.subTest():
                self.assertEqual(counter, progress*(100/progress_completed),
                                 f"{counter} {progress} {printed_data_stdout} {printed_data_stderr}")
            # Clear patched std out and err before each iteration.
            mock_out.truncate(0)
            mock_out.seek(0)
            mock_err.truncate(0)
            mock_err.seek(0)

    @unittest.mock.patch('sys.stderr', new_callable=io.StringIO)
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_progress_v2_test_mock(self, mock_out, mock_err) -> None:
        progress_completed = 2
        for progress in range(progress_completed + 1):
            progress_v2(progress_completed, progress)
            printed_data_stdout = mock_out.getvalue()
            printed_data_stderr = mock_err.getvalue()
            counter = printed_data_stdout.count("#")
            with self.subTest():
                self.assertEqual(counter, progress*(100/progress_completed),
                                 f"{counter} {progress} {printed_data_stdout} {printed_data_stderr}")
            # Clear patched std out and err before each iteration.
            mock_out.truncate(0)
            mock_out.seek(0)
            mock_err.truncate(0)
            mock_err.seek(0)


if __name__ == '__main__':
    unittest.main()

def progress_v1(max_number: int, current_number: int) -> None:
  """
  Prints following progress bar:
  Processing 100 [%] [####################################################################################################]
  """
  max_percent = 100
  current_percent = int(max_percent * current_number / max_number)
  end_line = '\r' if current_percent < max_percent else '\n'
  print(f"Processing {current_percent} [%] [{'#'*current_percent}{' '*(max_percent-current_percent)}]", end=end_line, flush=True)

  
def progress_v2(max_number: int, current_number: int, factor: float = 0.2) -> None:
  """
  Print following progress bar:
   | 100 [%] [####################]
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

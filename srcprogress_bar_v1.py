def progress(max_number: int, current_number: int) -> None:
  """
  Prints following progress bar:
  Processing 100 [%] [####################################################################################################]
  """
  max_percent = 100
  current_percent = int(max_percent * current_number / max_number)
  end_line = '\r' if current_percent < max_percent else '\n'
  print(f"Processing {current_percent} [%] [{'#'*current_percent}{' '*(max_percent-current_percent)}]", end=end_line, flush=True)
    

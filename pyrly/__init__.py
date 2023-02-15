"""Main file of the Python hourly stopwatch."""
from stopwatch import Stopwatch
from work_history import History


# Create the stopwatch.
stopwatch = Stopwatch()

# Create the history.
history = History("test.json")

worked_result = stopwatch.start()

description = input(">>> Describe what you did during work: ")

history.add_worked_hours(*worked_result, description)

history.print()

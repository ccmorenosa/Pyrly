"""Stopwatch class."""
from datetime import datetime


class Stopwatch:
    """Class to create a stopwatch that will be printed in the console."""

    init_time = None
    final_time = None

    def __init__(self):
        """Construct the stopwatch."""

    def start(self):
        """Initiate the stopwatch. It returns elapsed time when completed."""
        # Get initial time.
        self.init_time = datetime.now()

        print(
            "\nInitiating stopwatch\n"
            "(Type Ctrl+C/Ctrl+D to stop)\n"
        )

        # Catch Ctrl+c command.
        try:

            while True:
                # Print updated time elapsed.
                self.print_elapsed_time()

        except KeyboardInterrupt:
            print(end="\r")

            # Get final elapsed tine.
            elapsed_time = self.print_elapsed_time("\n")

            return self.init_time, self.final_time, elapsed_time

    def print_elapsed_time(self, end="\r"):
        r"""
        Print time since initial time.

        Parameters
        ----------
        end: Str.
            Option for the end of the print. Default: "\r".

        """
        # Get updated time.
        self.final_time = datetime.now()

        # Get elapsed time since initial time.
        elapsed_time = self.final_time - self.init_time

        # Print elapsed time.
        print(
            f"Time Worked: {(elapsed_time)}", end=end
        )
        return elapsed_time

"""Class that manage the history of worked hours and task."""
import json
from datetime import timedelta
import re


class History:
    """
    Class tha manages the worked hours of a project.

    Parameters
    ----------
    output_file: Str.
        File path of the table with the worked hours history. I should be a
        json file.

    project_name: Str. Default: None.
        Name of the working project.

    is_new: Bool. Default: False.
        Flag that indicates whether the history is new or not. If it is new,
        then a new dictionary is created. If it is not, it will read the file.

    """

    # Total time worked.
    total_time_worked = timedelta()

    def __init__(self, output_file, project_name=None, is_new=False):
        """Create the history object."""
        # Set the path of the table file.
        self.output_file = output_file

        if is_new:
            # Check if the project name is None.
            if project_name is None:
                raise TypeError(
                    "project_name must not be None if the history is new"
                )

            # Create the dictionary for the history.
            self.history = {
                "name": project_name,
                "worked_hours": [],
                "total_time_worked": f"{self.total_time_worked}"
            }

            # Save new file.
            self.save_history()

        else:
            # Read the json file.
            self.history = json.load(open(self.output_file))

            # Get total time worked.
            self.total_time_worked = self.parse_timedelta(
                self.history["total_time_worked"]
            )

        # Set the name of the project.
        self.project_name = self.history["name"]

    def parse_timedelta(self, timedelta_str):
        """
        Get a timedelta object from string.

        Parameters
        ----------
        timedelta_str: Str.
            String of the time difference.

        """
        # Get timedelta components.
        re_search = re.search(
            r"(\d{1,}|)( days?, |)(\d{1,}):(\d{2}):(\d{2})\.?(\d{6}|)",
            timedelta_str
        )

        # Schema for the timedelta arguments.
        schema = {
            "days": 0 if re_search[1] == "" else int(re_search[1]),
            "hours": 0 if re_search[3] == "" else int(re_search[3]),
            "minutes": 0 if re_search[4] == "" else int(re_search[4]),
            "seconds": 0 if re_search[5] == "" else int(re_search[5]),
            "microseconds": 0 if re_search[6] == "" else int(re_search[6])
        }

        return timedelta(**schema)

    def save_history(self):
        """Save the history to the JSON file."""
        with open(self.output_file, "w") as json_file:
            json_file.write(json.dumps(self.history, indent=4))

    def change_project_name(self, new_name):
        """
        Change the name of the project.

        Parameters
        ----------
        new_name: Str.
            Change the name of the project.

        """
        # Set the name of the project.
        self.project_name = self.history["name"] = new_name

        # Save new file.
        self.save_history()

    def add_worked_hours(
        self,
        init_time,
        final_time,
        elapsed_time,
        description
    ):
        """
        Change the name of the project.

        Parameters
        ----------
        init_time: Datetime.
            Initial time of work.

        final_time: Datetime.
            Final time of work.

        elapsed_time: Timedelta.
            Time difference between initial and final time.

        description: Str.
            Description of the task done during work.

        """
        # Create registry schema.
        schema = {
            "init_time": f"{init_time}",
            "final_time": f"{final_time}",
            "elapsed_time": f"{elapsed_time}",
            "task": f"{description}"
        }

        # Append registry.
        self.history["worked_hours"].append(schema)

        # Update total time worked.
        self.total_time_worked += elapsed_time

        self.history["total_time_worked"] = f"{self.total_time_worked}"

        # Save new file.
        self.save_history()

    def print(self):
        """Print the historial."""
        # Set table width.
        n_cols = 5 + 30 * 3 + 5

        # Print title.
        print(
            f"\n - Project name: {self.project_name}\n"
            "\n - Worked hours: \n"
        )

        print("-" * n_cols)
        print(
            f"|{'ID'.center(5)}"
            f"|{'Initial Time'.center(30)}"
            f"|{'Final Time'.center(30)}"
            f"|{'Elapsed Time'.center(30)}|"
        )
        print("-" * n_cols)

        for index in range(len(self.history["worked_hours"])):
            # Get the item.
            item = self.history["worked_hours"][index]

            print(
                f"|{f'{index}'.center(5)}"
                f"|{item['init_time'].center(30)}"
                f"|{item['final_time'].center(30)}"
                f"|{item['elapsed_time'].center(30)}|"
            )
            print("-" * n_cols)

        print(f"\n - Total time worked: {self.total_time_worked}")

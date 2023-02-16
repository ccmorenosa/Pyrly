"""Main file of the Python hourly stopwatch."""
from .stopwatch import Stopwatch
from .work_history import History

import re
from pathlib import Path


class main():
    """Main class for the admin."""

    # Create the stopwatch.
    stopwatch = Stopwatch()
    history = None

    def __init__(self):
        """Create the main menu of the working hours admin."""
        while True:
            # Display the welcome menu.
            try:
                self.welcome()
            except (KeyboardInterrupt, EOFError):
                self.exit()

            # Display the welcome menu.
            try:
                self.working_menu()
            except (KeyboardInterrupt, EOFError):
                print("\nGetting back to the main menu\n")

    def exit(self):
        """Exit the program."""
        print("\nExiting Pyrly...")
        exit()

    def welcome(self):
        """Welcome message and menu."""
        # Print welcome message.
        print(
            "Welcome to Pyrly\n"
            "----------------\n"
        )

        welcome_msg = (
            "What do you want to do?\n\n"
            "1: Create New Project\n"
            "2: Open a existing Project\n"
            "3: Exit\n"
        )

        while True:
            # Print welcome menu.
            print(welcome_msg)

            opt = input(">>> ")

            # Option for a new project.
            if opt == "1":
                new = True
                print("\nCreating a project\n")

                while True:
                    # Getting the project name.
                    name = input(
                        "Whats the name of the project?\n\n"
                        ">>> "
                    )

                    if name == "":
                        print("\nPlease enter a valid name\n")

                    else:
                        print(f"\nCreating '{name}' project\n")
                        break

            # Option for an existing project.
            elif opt == "2":
                new = False

                name = None

                print("\nOpening existing project\n")

            # Option to exit the program.
            elif opt == "3":
                self.exit()

            else:
                self.invalid_option(opt)
                continue

            try:
                self.file_select(new, name)
            except (KeyboardInterrupt, EOFError):
                print("\nCanceling operation.\n")
                pass

            break

    def file_select(self, new, name):
        """
        Select the file in which the table will be saved.

        Parameters
        ----------
        new: Bool.
            Flag that indicates whether is a new file or not.

        name: Str.
            Name of the project.

        """
        while True:
            # Getting file path.
            file = input(
                "Select the project file name (JSON file)\n\n"
                ">>> "
            )

            # Checking extension
            if re.match(r"[~:\w /\\-]+(\.json)", file) is None:
                file += ".json"

            # Resolving path.
            file_path = Path(file).resolve()

            if new:
                # Checking if path exists.
                if not file_path.parent.exists():
                    print(
                        f"\nPath {file_path.parent} does not exists\n"
                        "Please enter a valid path\n"
                    )
                    continue

                # Checking if file already exists.
                if file_path.exists():
                    print(
                        f"\nPath {file_path} already exists\n"
                        "Do you want to override it\n"
                    )

                    if not self.confirmation():
                        continue

                    else:
                        print(f"\nOverwriting {file_path}\n")

                else:
                    print(f"\nCreating {file_path}\n")

            else:
                # Checking if path exists.
                if not file_path.exists():
                    print(
                        f"\nPath {file_path} does not exists\n"
                        "Please enter a valid path\n"
                    )
                    continue

                print(f"\nOpening {file_path}\n")

            # Creating history object.
            self.history = History(file_path, name, new)

            break

    def working_menu(self):
        """Display the menu while a project is open."""
        working_msg = (
            f"\nWorking on '{self.history.project_name}' Project\n\n"
            "What do you want to do?\n\n"
            "1: Start working\n"
            "2: Print all the history\n"
            "3: Print some entries of the history\n"
            "4: Get all entires descriptions\n"
            "5: Get some entires descriptions\n"
            "6: Change project name\n"
            "7: Exit\n"
        )

        options = {
            "1": self.work,
            "2": self.history.print,
            "3": self.print_history,
            "4": self.history.print_descriptions,
            "5": self.get_descriptions,
            "6": self.change_project_name
        }

        while True:
            print(working_msg)

            opt = input(">>> ")

            if opt == "7":
                print(
                    "\nClosing '{self.history.project_name}' Project\n"
                    "Getting back to the main menu.\n"
                )
                break

            try:
                options.get(opt, self.invalid_option)()
            except (KeyboardInterrupt, EOFError):
                print("\nCancelling operation\n")

    def work(self):
        """Start stopwatch and save registry of the time worked."""
        worked_result = self.stopwatch.start()

        description = input(
            "\nDescribe what you did during work\n\n"
            ">>> "
        )

        self.history.add_worked_hours(*worked_result, description)

    def get_numbers_query(self):
        """Get query numbers for a print of the history."""
        # Get maximum number of entries.
        max_entries = self.history.get_history_len()

        while True:
            # Ask for entries.
            print(
                "\nEnter one or more entries to print\n"
                f"Number must be between 0 and {max_entries - 1}\n"
                "You can enter many numbers separated by commas like 2,4,7\n"
                "You can also enter ranges like 5-10, 33-39\n"
                "(Type Ctrl+C/Ctrl+D to exit)\n"
            )

            # Get asked rows.
            rows = input(">>> ")

            # Query array.
            query = set()

            # Parse rows
            arr_rows = re.findall(r",? *\d+-?\d*", rows)

            # Check the length of the result.
            if len(arr_rows) > 0:
                all_good = True

                for row in arr_rows:
                    # Get numbers
                    num = re.findall(r"\d+", row)

                    # Check if it is a single number.
                    if len(num) == 1 and int(num[0]) < max_entries:
                        query.update([int(num[0])])

                    # Check if it is a range.
                    elif (
                        len(num) == 2 and
                        int(num[1]) < max_entries and
                        int(num[0]) < int(num[1]) + 1
                    ):
                        query.update(range(int(num[0]), int(num[1]) + 1))

                    # Warning when neither of the above options is correct.
                    else:
                        print(
                            f"\nInvalid number or range: {row.strip(', ')}\n"
                            "Please enter valid values.\n"
                        )
                        all_good = False
                        break

                if not all_good:
                    continue

            # Warning if it does not pass the regular expression.
            else:
                print(
                    "\nInvalid entry\n"
                    "Please enter valid values.\n"
                )
                continue

            break

        return query

    def print_history(self):
        """Print given indexes of the worked hours history."""
        query = self.get_numbers_query()

        # Print asked indexes.
        self.history.print(query=query)

    def get_descriptions(self):
        """Print a warning when a invalid option is given."""
        query = self.get_numbers_query()

        # Print tasks descriptions.
        self.history.print_descriptions(query=query)

    def confirmation(self):
        """Return whether the action should be executed or not."""
        while True:
            opt = input("Confirm ([Y]/n): ")

            if re.fullmatch(r"(Y|y|yes|Yes|YES|)", opt):
                return True
            elif re.fullmatch(r"(N|n|no|No|NO)", opt):
                return False
            else:
                continue

    def change_project_name(self):
        """Change the project name."""
        # Get actual name.
        actual_name = self.history.project_name

        while True:
            # Ask for entries.
            print(
                f"\nEnter a new name for the project {actual_name}\n"
                "(Type Ctrl+C/Ctrl+D to exit)\n"
            )

            # Get asked rows.
            new_name = input(">>> ")

            # Ask for confirmation.
            print(
                "\nAre you sure you want to change the project name\n"
                f"from {actual_name}, to: {new_name}?\n"
            )

            if self.confirmation():
                print(f"Change name to {new_name}")

                # Change name.
                self.history.change_project_name(new_name)

            break

    def invalid_option(self, opt=""):
        """Print a warning when a invalid option is given."""
        print(
            f"\nUnrecognized option {opt}\n"
            "Please enter a valid option\n"
        )


if __name__ == "__main__":
    main()

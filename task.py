from collections import OrderedDict
from peewee import *
import datetime

db = SqliteDatabase("tasks.db")
short_separator_string = "\n{}".format("=" * 30)
long_separator_string = "{}".format("=" * 60)


class Task(Model):
    employee = TextField()
    task_name = TextField()
    time_worked = IntegerField(default=0)
    task_notes = TextField()
    timestamp = DateField(default=datetime.date.today)

    class Meta:
        database = db


class TaskManager:

    def __init__(self):
        """Create the database and the table if they don't exist"""
        db.connect(reuse_if_open=True)
        db.create_tables([Task], safe=True)
        while True:
            self.display_menu(self.main_menu, "\nWhat would you like to do?")

    def request_int(self, message="\nEnter selection: ", _max=-1):
        while True:
            try:
                input_value = input(message).lower()
                if input_value == "q":
                    exit()
                input_value = int(input_value)
                if _max != -1 and input_value > _max:
                    raise UserWarning("\nOnly numbers between 0 and {}".format(_max))
                else:
                    return input_value
            except ValueError:
                print("\nNumbers only")

    def find_tasks_with_employee_name(self) -> [Task]:
        """find by employee"""
        return self.display_menu(self.search_by_employee)

    def find_tasks_with_employee_name_from_list(self) -> [Task]:
        """choose from employee list"""
        employees = Task.select(Task.employee).distinct()
        print("\nSelect an employee:\n")
        for i, employee in enumerate(employees):
            print("[{}] {}".format(i, employee.employee))
        employee = self.request_int(_max=len(employees) - 1)
        return Task.select().where(Task.employee == employees[employee].employee)

    def find_tasks_with_employee_name_from_search(self) -> [Task]:
        """manually enter name"""
        employee_name = input("\nEnter employee name: ")
        return Task.select().where(Task.employee.contains(employee_name))

    def find_tasks_with_date(self) -> [Task]:
        """find by date"""
        tasks = Task.select(Task.timestamp).distinct()
        if tasks:
            print("{}\nDates available:\n".format(short_separator_string))
            for i, task in enumerate(tasks):
                print("[{}]: {}".format(i, task.timestamp))
            date = self.request_int(_max=len(tasks) - 1)
            tasks = Task.select().order_by(Task.timestamp.asc()).where(Task.timestamp == tasks[date].timestamp)
        return tasks

    def find_tasks_with_time_spent(self) -> [Task]:
        """find by time spent"""
        time_spent = self.request_int("{}\nEnter time spent in minutes: ".format(short_separator_string))
        return Task.select().where(Task.time_worked == time_spent)

    def find_tasks_with_search(self) -> [Task]:
        """find with search term"""
        query = input("{}\nEnter search query: ".format(short_separator_string))
        tasks = Task.select().where((Task.task_name.contains(query)) | (Task.task_notes.contains(query)))
        return tasks

    def add_task(self) -> bool:
        """add a task"""
        employee_name = input("\nEmployee name: ")
        task_name = input("Task name: ")
        time_worked = self.request_int("Time spent in minutes: ")
        task_notes = input("Task notes: ")
        if input("\nSave task? [Yn]: ").lower() != "n":
            return self.save_task(employee_name, task_name, time_worked, task_notes)
        return False

    def save_task(self, employee: str, task_name: str, time_worked: int, task_notes: str) -> bool:
        if isinstance(employee, str) and isinstance(task_name, str) \
                and isinstance(time_worked, int) and isinstance(task_notes, str):
            Task.create(employee=employee, task_name=task_name, time_worked=time_worked, task_notes=task_notes)
            print("\nSaved!\n")
            return True
        return False

    def lookup_tasks(self):
        """view previous tasks"""
        tasks = self.display_menu(self.search_menu)
        if not len(tasks):
            print("\nNo tasks available\n")
        else:
            self.print_tasks(tasks)

    def print_tasks(self, tasks):
        for task in tasks:
            print(self.generate_task_string(task))
        print("")

    @staticmethod
    def generate_task_string(task: Task) -> str:
        task_string = "\n{}\n{}\n" \
                      "Employee name:  {}\n" \
                      "Task name:      {}\n" \
                      "Time spent:     {}\n" \
                      "Task notes:     {}\n" \
                      "{}".format(task.timestamp, long_separator_string, task.employee, task.task_name,
                                  task.time_worked, task.task_notes, long_separator_string)
        return task_string

    @staticmethod
    def generate_menu_text(menu, menu_text) -> str:
        menu_text = menu_text + "\n"
        for key, value in menu.items():
            menu_text = menu_text + "\n[{}]: {}".format(key, value.__doc__)
        menu_text = menu_text + "\n\nEnter selection: "
        return menu_text

    def display_menu(self, menu, message="\nEnter a search method:"):
        menu_text = self.generate_menu_text(menu, message)
        selection = self.request_int(menu_text, _max=len(menu) - 1)
        return menu[selection](self)

    main_menu = OrderedDict([
        (0, add_task),
        (1, lookup_tasks),
    ])

    search_menu = OrderedDict([
        (0, find_tasks_with_employee_name),
        (1, find_tasks_with_date),
        (2, find_tasks_with_time_spent),
        (3, find_tasks_with_search),
    ])

    search_by_employee = OrderedDict([
        (0, find_tasks_with_employee_name_from_list),
        (1, find_tasks_with_employee_name_from_search),
    ])


if __name__ == '__main__':
    TaskManager()

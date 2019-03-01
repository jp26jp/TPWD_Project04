import datetime

from collections import OrderedDict
from peewee import *

db = SqliteDatabase("tasks.db")
short_separator_string = "\n{}".format("=" * 30)
long_separator_string = "{}".format("=" * 60)


class Task(Model):
    employee_name = TextField()
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
        menu_text = self.generate_menu_text(self.main_menu, "\nWhat would you like to do?")
        selection = None
        while selection != 'q':
            selection = self.request_int(menu_text, _max=len(self.main_menu))
            self.main_menu[selection](self)

    @staticmethod
    def request_int(message="\nEnter selection: ", _max=-1):
        while True:
            try:
                input_value = input(message)
                if input_value == "q":
                    break
                input_value = int(input_value)
                if _max != -1 and input_value > _max:
                    print("\nOnly numbers between 0 and {}".format(_max))
                else:
                    break
            except ValueError:
                print("\nNumbers only")
        return input_value

    def find_tasks_with_employee_name(self) -> [Task]:
        """find by employee"""
        menu_text = self.generate_menu_text(self.search_by_employee, "\nEnter a search method:")
        selection = self.request_int(menu_text, _max=len(self.search_by_employee))
        tasks = self.search_by_employee[selection](self)
        return tasks

    def find_tasks_with_employee_name_from_list(self) -> [Task]:
        """choose from employee list"""
        employees = Task.select(Task.employee_name).distinct()
        print("\nSelect an employee:\n")
        for i, employee in enumerate(employees):
            print("[{}] {}".format(i, employee.employee_name))
        employee = self.request_int(_max=len(employees))
        return Task.select().where(Task.employee_name == employees[employee].employee_name)

    def find_tasks_with_employee_name_from_search(self) -> [Task]:
        """manually enter name"""
        employee_name = input("\nEnter employee name: ")
        return Task.select().where(Task.employee_name.contains(employee_name))

    def find_tasks_with_date(self) -> [Task]:
        """find by date"""
        tasks = Task.select(Task.timestamp).distinct()
        if tasks:
            print(short_separator_string)
            print("\nDates available:\n")
            for i, task in enumerate(tasks):
                print("[{}]: {}".format(i, task.timestamp))
            date = self.request_int(_max=len(tasks))
            tasks = Task.select().order_by(Task.timestamp.asc()).where(
                Task.timestamp == tasks[date].timestamp)
        return tasks

    def find_tasks_with_time_spent(self) -> [Task]:
        """find by time spent"""
        print(short_separator_string)
        time_spent = self.request_int("\nEnter time spent in minutes: ")
        return Task.select().where(Task.time_worked == time_spent)

    def find_tasks_with_search(self) -> [Task]:
        """find with search term"""
        print(short_separator_string)
        query = input("\nEnter search query: ")
        tasks = Task.select().where(
            (Task.task_name.contains(query)) | (Task.task_notes.contains(query))
        )
        return tasks

    def add_task(self) -> bool:
        """add a task"""
        employee_name = input("\nEmployee name: ")
        task_name = input("Task name: ")
        time_worked = self.request_int("Time spent in minutes: ")
        task_notes = input("Task notes: ")

        if input("\nSave task? [Yn]: ").lower() != "n":
            return self.save_task(employee_name, task_name, time_worked,
                                  task_notes)
        return False

    @staticmethod
    def save_task(employee_name: str, task_name: str, time_worked: int,
                  task_notes: str) -> bool:
        if isinstance(employee_name, str) and \
                isinstance(task_name, str) and \
                isinstance(time_worked, int) and \
                isinstance(task_notes, str):
            Task.create(employee_name=employee_name,
                        time_worked=time_worked,
                        task_name=task_name,
                        task_notes=task_notes)
            print("\nSaved!\n")
            return True
        return False

    def lookup_tasks(self):
        """view previous tasks"""
        menu_text = self.generate_menu_text(self.search_menu, "\nEnter a search method:")
        selection = self.request_int(menu_text, _max=len(self.search_menu))
        tasks = self.search_menu[selection](self)
        if not len(tasks):
            print("\nNo tasks available\n")
        else:
            for task in tasks:
                print(long_separator_string)
                self.print_task(task)
            print("")

    def print_task(self, task):
        print("\n{}".format(task.timestamp))
        print(long_separator_string)
        print("Employee name:   {}\n"
              "Task name:       {}\n"
              "Time spent:      {}\n"
              "Task notes:      {}".format(task.employee_name, task.task_name,
                                           task.time_worked, task.task_notes))

    @staticmethod
    def generate_menu_text(menu, menu_text="\nEnter selection:") -> str:
        menu_text = menu_text + "\n"
        for key, value in menu.items():
            menu_text = menu_text + "\n[{}]: {}".format(key, value.__doc__)
        menu_text = menu_text + "\n\nEnter selection: "
        return menu_text

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

from collections import OrderedDict
from unittest.mock import patch
from task import TaskManager
from playhouse.sqlite_ext import *
import unittest
import string
import random
import task

test_db = SqliteDatabase(':memory:')


class TestTaskManager(unittest.TestCase):
    def test_request_int(self):
        inputs = [
            1,
            random.choice(string.ascii_lowercase).replace("q", ""),
            "q",
            5
        ]
        with patch("builtins.input", side_effects=inputs):
            # test 1
            value = task.TaskManager.request_int(task)
            self.assertTrue(isinstance(value, int))
            # test random letter
            TaskManager.request_int(task)
            self.assertRaises(ValueError)
            # test q
            TaskManager.request_int(task)
            self.assertRaises(SystemExit)
            # test value > _max
            TaskManager.request_int(task, 4)
            self.assertRaises(UserWarning)

    def test_save_task(self):
        self.assertTrue(TaskManager.save_task(task.TaskManager, "Bob", "Stuff", 10, "None"))

    def test_generate_menu_text(self):
        menu = OrderedDict([(0, self.dummy_method), (1, self.dummy_method2)])
        menu_text = TaskManager.generate_menu_text(menu, "")
        test_menu_text = "\n\n[0]: a super dumb method\n[1]: an even dumber method\n\nEnter selection: "
        self.assertEqual(menu_text, test_menu_text)

    def test_generate_task_string(self):
        expected_string = "\n2019-03-04\n" \
                          "============================================================\n" \
                          "Employee name:  Bob\n" \
                          "Task name:      Stuff\n" \
                          "Time spent:     10\n" \
                          "Task notes:     None\n" \
                          "============================================================"
        task_string = TaskManager.generate_task_string(task.Task(employee="Bob", task_name="Stuff", time_worked=10,
                                                                 task_notes="None", timestamp="2019-03-04"))
        self.assertEqual(expected_string, task_string)

    def test_isstr(self):
        self.assertTrue(TaskManager.isstr("string"))

    def test_isint(self):
        self.assertTrue(TaskManager.isint(1))

    def dummy_method(self):
        """a super dumb method"""

    def dummy_method2(self):
        """an even dumber method"""
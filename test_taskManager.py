from unittest import TestCase

import task


class TestTaskManager(TestCase):
    def test_request_int(self):
        input_value = task.TaskManager.request_int()
        self.assertIs(type(input_value), int)

    def test_add_task(self):
        new_task = task.TaskManager.add_task(task.TaskManager)
        self.assertTrue(new_task)

    def test_save_task(self):
        bad_task = task.TaskManager.save_task("", "", "", "")
        self.assertFalse(bad_task)
        good_task = task.TaskManager.save_task("John", "Work", 10, "Notes")
        self.assertTrue(good_task)

    def test_display_menu(self):
        from collections import OrderedDict
        menu = OrderedDict([(0, self.dummy_method)])
        menu_string = task.TaskManager.generate_menu_text(menu).replace('\n', '')
        test_result = 'Enter selection:[0]: dummy method for display_menu()Enter selection: '
        self.assertEqual(menu_string, test_result)

    def dummy_method(self):
        """dummy method for display_menu()"""
        pass

    def test_print_task(self):
        task.TaskManager.print_task(task.TaskManager, task.Task("Bob", "Did stuff", 10, "Notes", "2019-02-25"))
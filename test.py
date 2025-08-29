import unittest
from unittest.mock import patch, mock_open
import json
import os

# Импорт функций из проекта

from main import load_tasks, save_tasks, add_task, view_tasks, complete_task, delete_task

class TestTodoApp(unittest.TestCase):

    @patch('os.path.exists')
    def test_load_tasks_no_file(self, mock_exists):
        mock_exists.return_value = False
        tasks = load_tasks()
        self.assertEqual(tasks, [])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='[{"id": 1, "title": "test", "completed": false}]')
    def test_load_tasks_with_file(self, mock_file, mock_exists):
        mock_exists.return_value = True
        tasks = load_tasks()
        self.assertEqual(tasks, [{"id": 1, "title": "test", "completed": False}])

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_tasks(self, mock_dump, mock_file):
        tasks = [{"id": 1, "title": "test", "completed": False}]
        save_tasks(tasks)
        mock_file.assert_called_once_with("tasks.json", "w", encoding="utf-8")
        mock_dump.assert_called_once_with(tasks, mock_file(), ensure_ascii=False, indent=4)

    @patch('builtins.input', return_value='New task')
    @patch('builtins.print')
    def test_add_task(self, mock_print, mock_input):
        tasks = []
        add_task(tasks)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0], {"id": 1, "title": "New task", "completed": False})
        mock_print.assert_called_once_with("Задача 'New task' добавлена!")

    @patch('builtins.print')
    def test_view_tasks_empty(self, mock_print):
        view_tasks([])
        mock_print.assert_called_once_with("Список задач пуст!")

    @patch('builtins.print')
    def test_view_tasks_with_tasks(self, mock_print):
        tasks = [{"id": 1, "title": "test", "completed": False}]
        view_tasks(tasks)
        mock_print.assert_called_once_with("1. test - Не выполнено")

    @patch('builtins.input', return_value='1')
    @patch('builtins.print')
    def test_complete_task_success(self, mock_print, mock_input):
        tasks = [{"id": 1, "title": "test", "completed": False}]
        complete_task(tasks)
        self.assertTrue(tasks[0]["completed"])
        # Проверяем, что view_tasks вызван (print внутри), и успех
        self.assertGreater(len(mock_print.call_args_list), 1)  # view + success

    @patch('builtins.input', return_value='2')
    @patch('builtins.print')
    def test_complete_task_invalid_id(self, mock_print, mock_input):
        tasks = [{"id": 1, "title": "test", "completed": False}]
        complete_task(tasks)
        self.assertFalse(tasks[0]["completed"])
        # Проверяем print "not found"
        calls = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn("Задача с таким номером не найдена!", calls)

    @patch('builtins.input', return_value='abc')
    @patch('builtins.print')
    def test_complete_task_invalid_input(self, mock_print, mock_input):
        tasks = [{"id": 1, "title": "test", "completed": False}]
        complete_task(tasks)
        self.assertFalse(tasks[0]["completed"])
        # Проверяем print "please enter number"
        calls = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn("Пожалуйста, введите число!", calls)

    @patch('builtins.input', return_value='1')
    @patch('builtins.print')
    def test_delete_task_success(self, mock_print, mock_input):
        tasks = [{"id": 1, "title": "test", "completed": False}]
        delete_task(tasks)
        self.assertEqual(len(tasks), 0)
        # Проверяем успех
        self.assertGreater(len(mock_print.call_args_list), 1)  # view + success

if __name__ == '__main__':
    unittest.main()
import unittest
import os
import shutil
from shell.emulator import ShellEmulator


class TestVirtualFileSystem(unittest.TestCase):
    def setUp(self):
        # Копирование архива из папки data в рабочую директорию
        self.zip_path = 'test_vfs.zip'
        shutil.copy('../data/vfs.zip', self.zip_path)
        self.emulator = ShellEmulator(self.zip_path)
        self.vfs = self.emulator.vfs

    def tearDown(self):
        self.vfs.close()
        if os.path.exists(self.zip_path):
            os.remove(self.zip_path)

    def test_ls_root_directory(self):
        # Проверка содержимого корневой директории
        root_content = self.vfs.ls()
        self.assertIn("file1.txt", root_content)
        self.assertIn("file2.txt", root_content)
        self.assertIn("dir1", root_content)
        self.assertIn("dir2", root_content)

    def test_ls_dir1(self):
        # Проверка содержимого поддиректории dir1
        dir1_content = self.vfs.ls("dir1")
        self.assertIn("nested_file1.txt", dir1_content)
        self.assertIn("nested_file2.txt", dir1_content)

    def test_ls_nonexistent_directory(self):
        # Проверка попытки вывести содержимое несуществующей директории
        result = self.vfs.ls("nonexistent")
        self.assertEqual(result, set())

    def test_cd_to_existing_directory(self):
        # Переход в существующую директорию и проверка текущей директории
        self.assertTrue(self.vfs.cd("dir1"))
        self.assertEqual(self.vfs.current_dir, "~/root/dir1")

    def test_cd_to_parent_directory(self):
        # Переход в родительскую директорию
        self.assertTrue(self.vfs.cd(".."))
        self.assertEqual(self.vfs.current_dir, "~")

    def test_cd_to_nonexistent_directory(self):
        # Переход в несуществующую директорию
        self.assertFalse(self.vfs.cd("nonexistent"))

    def test_cd_to_subdir_and_back(self):
        # Переход в поддиректорию, а затем возвращение в корневую директорию
        self.assertTrue(self.vfs.cd("dir2"))
        self.assertTrue(self.vfs.cd(".."))
        self.assertEqual(self.vfs.current_dir, "~/root")

    def test_rm_existing_file(self):
        # Проверка удаления существующего файла
        self.assertIn("file1.txt", self.vfs.ls())
        result = self.vfs.rm("file1.txt")
        self.assertEqual(result, "File file1.txt removed.")
        self.assertNotIn("file1.txt", self.vfs.ls())

    def test_rm_nonexistent_file(self):
        # Попытка удалить несуществующий файл
        result = self.vfs.rm("nonexistent_file.txt")
        self.assertEqual(result, "File nonexistent_file.txt not found in the current directory.")

    def test_tac_file2(self):
        # Проверка вывода содержимого файла file2.txt в обратном порядке
        expected_output = "Всё ещё содержимое file3.txt\nЭто тоже содержимое file2.txt\nЭто содержимое file2.txt для тестирования команды tac"
        result = self.vfs.tac("file2.txt").strip()
        self.assertEqual(result, expected_output)

    def test_tac_nonexistent_file(self):
        # Попытка вывести содержимое несуществующего файла
        result = self.vfs.tac("nonexistent_file.txt")
        self.assertEqual(result, "File nonexistent_file.txt not found in the current directory.")

    def test_clear(self):
        # Проверка работы команды clear (не изменяет файловую систему)
        result = self.emulator.execute_command("clear")
        self.assertEqual(result, "clear")

    def test_exit(self):
        # Проверка корректности работы команды exit
        result = self.emulator.execute_command("exit")
        self.assertEqual(result, "exit")


if __name__ == "__main__":
    unittest.main()

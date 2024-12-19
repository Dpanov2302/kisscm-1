import os
import zipfile


class VirtualFileSystem:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.zip_file = zipfile.ZipFile(zip_path, 'a')
        self.current_dir = "~/root"

    def ls(self, path=None):
        content = set()
        if path is not None:
            if path[-1] == "/":
                path = path[:-1]
            full_path = self.current_dir + '/' + path if self.current_dir != "~" else "/" + path
        else:
            full_path = self.current_dir

        parts = full_path.split('/')[1:] if full_path != "~" else []
        all_items = self.zip_file.namelist()

        if parts:
            prefix = '/'.join(parts) + '/'
            for item in all_items:
                if item.startswith(prefix):
                    relative_path = item[len(prefix):].split('/')
                    if relative_path[0]:
                        content.add(relative_path[0])
        else:
            for item in all_items:
                item_parts = item.split('/')
                if item_parts[0]:
                    content.add(item_parts[0])

        return content

    def cd(self, path):
        if path == "..":
            if self.current_dir != "~":
                parts = self.current_dir.split('/')[1:-1]
                if not parts:
                    self.current_dir = "~"
                else:
                    self.current_dir = "~/" + "/".join(parts)
            return True

        if self.current_dir == "~":
            start = ""
        else:
            start = self.current_dir[2:] + "/"

        if any(item.startswith(start + path + '/') for item in self.zip_file.namelist()):
            self.current_dir += ("/" + path)
            return True

        return False

    def rm(self, filename):
        if self.current_dir == "~":
            full_path = filename
        else:
            full_path = f"{self.current_dir[2:]}/{filename}"

        archive_files = self.zip_file.namelist()

        if full_path not in archive_files:
            return f"File {filename} not found in the current directory."

        files_data = {item: self.zip_file.read(item) for item in archive_files}

        self.zip_file.close()

        temp_zip_path = self.zip_path + ".temp"
        with zipfile.ZipFile(temp_zip_path, 'w') as temp_zip:
            for item, data in files_data.items():
                if item != full_path:
                    temp_zip.writestr(item, data)

        os.remove(self.zip_path)
        os.rename(temp_zip_path, self.zip_path)

        self.zip_file = zipfile.ZipFile(self.zip_path, 'a')

        return f"File {filename} removed."

    def tac(self, filename):
        if self.current_dir == "~":
            full_path = filename
        else:
            full_path = f"{self.current_dir[2:]}/{filename}"

        if full_path not in self.zip_file.namelist():
            return f"File {filename} not found in the current directory."

        file_content = self.zip_file.read(full_path).decode('utf-8')
        reversed_lines = "\n".join(file_content.splitlines()[::-1])

        return reversed_lines

    def close(self):
        self.zip_file.close()

from shell.vfs import VirtualFileSystem


class ShellEmulator:
    def __init__(self, zip_path):
        self.vfs = VirtualFileSystem(zip_path)

    def execute_command(self, input):
        parts = input.split()
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        if command == "exit":
            return "exit"
        elif command == "cd":
            if len(args) == 1:
                if not self.vfs.cd(args[0]):
                    return "Directory not found"
            else:
                return "Usage: cd <directory_path>"
        elif command == "ls":
            if len(args) < 2:
                if len(args) == 1:
                    content = self.vfs.ls(args[0])
                else:
                    content = self.vfs.ls()
                return " ".join(content)
            else:
                return "Usage: ls <path> or nothing"
        elif command == "rm":
            if len(args) == 1:
                return self.vfs.rm(args[0])
            else:
                return "Usage: rm <filename>"
        elif command == "tac":
            if len(args) == 1:
                return self.vfs.tac(args[0])
            else:
                return "Usage: tac <filename>"
        elif command == "clear":
            return "clear"
        else:
            return "Unknown command"

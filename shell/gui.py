import tkinter as tk
from tkinter import scrolledtext
from shell.emulator import ShellEmulator


class ShellGUI:
    def __init__(self, zip_path):
        self.root = tk.Tk()
        self.root.title("Shell Emulator")
        self.emulator = ShellEmulator(zip_path)

        self.root.configure(bg='black')

        self.output_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20, bg='black', fg='white')
        self.output_area.grid(column=0, row=0, padx=10, pady=10, columnspan=2)
        self.output_area.config(state=tk.DISABLED)

        self.command_entry = tk.Entry(self.root, width=70, bg='black', fg='white', insertbackground='white')
        self.command_entry.grid(column=0, row=1, padx=10, pady=10)
        self.command_entry.bind('<Return>', self.send_command)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_command, bg='black', fg='white')
        self.send_button.grid(column=1, row=1, padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def start(self):
        self.root.mainloop()

    def send_command(self, event=None):
        command = self.command_entry.get()
        if command:
            result = self.emulator.execute_command(command)
            self.output_area.config(state=tk.NORMAL)
            if result == "clear":
                self.output_area.delete(1.0, tk.END)
            else:
                self.output_area.insert(tk.END, f"{self.emulator.vfs.current_dir}> {command}\n")
                if result == "exit":
                    self.root.destroy()
                    return "break"
                elif result:
                    self.output_area.insert(tk.END, f"{result}\n")

            self.output_area.config(state=tk.DISABLED)
            self.command_entry.delete(0, tk.END)

    def on_close(self):
        self.emulator.vfs.close()
        self.root.destroy()

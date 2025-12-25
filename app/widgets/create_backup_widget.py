import customtkinter
from core.backup import BackupCreator

class BackupWindow:
    def __init__(self, master, font_1):
        self.master = master
        self.font_1 = font_1
        self.top_level_add = None

    def cancel_backup_button(self):
        self.top_level_add.destroy()

    def create_backup_button(self):
        path = self.entry_path.get()
        time = int(self.entry_time.get())
        option = self.option_menu.get()
        if option == "hour(s)":
            index = "h"
        else:
            index = "d"
        BackupCreator().create_backup(path, time, index)
        self.cancel_backup_button()

    def create_backup(self):
        if self.top_level_add is None or not self.top_level_add.winfo_exists():
            self.top_level_add = customtkinter.CTkToplevel(self.master)
            self.top_level_add.title("Create a backup")
            self.top_level_add.geometry("700x200")
        else:
            self.top_level_add.focus()
            self.top_level_add.lift()

        label_path = customtkinter.CTkLabel(self.top_level_add, text="Full path to the file:", font=self.font_1)
        label_path.pack(side="top", anchor="n", padx=10, pady=(10, 5))

        self.entry_path = customtkinter.CTkEntry(self.top_level_add, placeholder_text="Path:", width=600)
        self.entry_path.pack(side="top", anchor="n", padx=10)

        label_time = customtkinter.CTkLabel(self.top_level_add, text="Time to store:", font=self.font_1)
        label_time.pack(side="top", anchor="n", padx=10, pady=(10, 5))

        time_frame = customtkinter.CTkFrame(self.top_level_add, fg_color="transparent")
        time_frame.pack(padx=10, pady=(10, 5))
        self.entry_time = customtkinter.CTkEntry(time_frame, placeholder_text="Time:", width=50)
        self.entry_time.pack(side="left", padx=10)

        self.option_menu = customtkinter.CTkOptionMenu(time_frame, values=["hour(s)", "day(s)"])
        self.option_menu.pack(side="left")

        button_frame = customtkinter.CTkFrame(self.top_level_add, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=(5, 10))
        create_button = customtkinter.CTkButton(button_frame, text="Create", command=self.create_backup_button,
                                                    width=100, height=50)
        create_button.pack(side="right")
        cancel_button = customtkinter.CTkButton(button_frame, text="Cancel", command=self.cancel_backup_button,
                                                    width=100, height=50, fg_color="gray")
        cancel_button.pack(side="left")
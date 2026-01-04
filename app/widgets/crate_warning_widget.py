import customtkinter
from customtkinter import CTkFont


class WarningWindow:
    def __init__(self, master, button_result=None):
        self.master = master
        self.top_level_warning = None
        self.button_result = button_result

    def confirm_button_pressed(self):
        self.button_result = True
        if self.top_level_warning:
            self.top_level_warning.destroy()
            self.top_level_warning = None

    def cancel_button_pressed(self):
        self.button_result = False
        if self.top_level_warning:
            self.top_level_warning.destroy()
            self.top_level_warning = None

    def create_warning(self, text):
        self.text = text
        if self.top_level_warning and self.top_level_warning.winfo_exists():
            self.top_level_warning.lift()
            self.top_level_warning.focus_force()
            self.top_level_warning.wait_window()
            return self.button_result

        self.top_level_warning = customtkinter.CTkToplevel(self.master)
        self.top_level_warning.title("Warning")
        self.top_level_warning.geometry("300x150")
        self.top_level_warning.resizable(False, False)

        label = customtkinter.CTkLabel(self.top_level_warning, text=self.text, font=CTkFont("Inter", 20), wraplength=300, justify="center", anchor="center")
        label.pack(side="top", padx=10, pady=10)
        frame = customtkinter.CTkFrame(self.top_level_warning)
        frame.pack(side="bottom", fill="x", padx=10, pady=10)
        button_confirm = customtkinter.CTkButton(frame, text="Confirm", command=self.confirm_button_pressed, height=30)
        button_confirm.pack(side="right", anchor="se", padx=10, pady=10)
        button_cancel = customtkinter.CTkButton(frame, text="Cancel", command=self.cancel_button_pressed, height=30)
        button_cancel.pack(side="left", anchor="sw", padx=10, pady=10)

        self.top_level_warning.update_idletasks()
        self.top_level_warning.transient(self.master)
        self.top_level_warning.grab_set()
        self.top_level_warning.focus_force()
        self.top_level_warning.wait_window()
        return self.button_result

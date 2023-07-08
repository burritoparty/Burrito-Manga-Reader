import customtkinter
from Database import *
from Functions import *


class TagFrame(customtkinter.CTkFrame):
    def __init__(self, bookframe, master, **kwargs):
        super().__init__(master, **kwargs)

        # make the label
        self.tag_label = customtkinter.CTkLabel(self,
                                                text="Sort by tag",
                                                text_color=light_pink,
                                                fg_color="transparent")

        # make the buttons
        self.tag_append = customtkinter.CTkButton(self,
                                                  text="Add tag",
                                                  fg_color=light_pink,
                                                  text_color=black,
                                                  hover_color=dark_pink)
        self.tag_delete = customtkinter.CTkButton(self,
                                                  text="Delete tag",
                                                  fg_color=light_pink,
                                                  text_color=black,
                                                  hover_color=dark_pink)
        self.tag_rename = customtkinter.CTkButton(self,
                                                  text="Rename tag",
                                                  fg_color=light_pink,
                                                  text_color=black,
                                                  hover_color=dark_pink)

        self.tag_label.grid(row=0, column=0, padx=20)
        self.tag_append.grid(row=2, column=0, padx=20, pady=20)
        self.tag_delete.grid(row=3, column=0, padx=20, pady=20)
        self.tag_rename.grid(row=4, column=0, padx=20, pady=20)

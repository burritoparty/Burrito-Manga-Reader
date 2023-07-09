import customtkinter

from Database import *
from Functions import *


class AuthorFrame(customtkinter.CTkFrame):

    def author_append_call(self, authors_json):
        print("add")

    def author_delete_call(self, authors_json, window):
        print("delete")

    def author_rename_call(self, authors_json, window):
        print("rename")

    def __init__(self, authors_json, bookframe, master, **kwargs):
        super().__init__(master, **kwargs)

        # make windows
        authors_sort_window = None
        authors_rename_window = None
        authors_delete_window = None

        # make the buttons
        self.author_sort = customtkinter.CTkButton(self,
                                                   text="Sort by author",
                                                   fg_color=light_pink,
                                                   text_color=black,
                                                   hover_color=dark_pink)
        self.author_append = customtkinter.CTkButton(self,
                                                     text="Add author",
                                                     fg_color=light_pink,
                                                     text_color=black,
                                                     hover_color=dark_pink,
                                                     command=lambda x=authors_json: self.author_append_call(x))
        self.author_delete = customtkinter.CTkButton(self,
                                                     text="Delete author",
                                                     fg_color=light_pink,
                                                     text_color=black,
                                                     hover_color=dark_pink,
                                                     command=lambda x=authors_json,
                                                     y=authors_delete_window: self.author_delete_call(x, y))
        self.author_rename = customtkinter.CTkButton(self,
                                                     text="Rename author",
                                                     fg_color=light_pink,
                                                     text_color=black,
                                                     hover_color=dark_pink,
                                                     command=lambda x=authors_json,
                                                     y=authors_rename_window: self.author_rename_call(x, y))

        self.author_sort.grid(row=0, column=0, padx=20, pady=20)
        self.author_append.grid(row=2, column=0, padx=20, pady=20)
        self.author_delete.grid(row=3, column=0, padx=20, pady=20)
        self.author_rename.grid(row=4, column=0, padx=20, pady=20)
import json
from os import path

import customtkinter

from Database import *
from Functions import *


class AuthorFrame(customtkinter.CTkFrame):

    def author_append_call(self, authors_json):
        print("add")
        authors = []
        if path.isfile(authors_json) is False:
            print("path dont exist")
        else:
            # create the dialogue box
            authors_append_dialogue = customtkinter.CTkInputDialog(text="New Author: ", title="Append a new author")
            authors_append_dialogue.geometry('0+0')

            # load the json
            with open(authors_json, 'r') as f:
                load_authors = json.load(f)

            # load the tag names from the json into an array
            for i in load_authors['authors']:
                authors.append(i['name'])

            # get the input from the user
            new_author = authors_append_dialogue.get_input()

            # check if the input is valid
            if new_author == '':
                # user hit the cancel button
                do_nothing = 0
            elif check_exists(new_author, authors, False) is False:
                error = customtkinter.CTkToplevel()
                error.geometry("0+0")
                label = customtkinter.CTkLabel(error,
                                               text="this tag already exists\n(not case sensitive)",
                                               font=("Roboto", 20))
                label.grid(padx=10, pady=10)
            else:
                # append the new tag to the array
                authors.append(new_author)
                authors.sort()

                # delete all the authors
                del load_authors['authors']

                # delete ['authors'] object from json
                with open(authors_json, 'w') as f:
                    json.dump(load_authors, f, indent=2)

                # load the ['authors'] object back into json
                with open(authors_json, 'w') as f:
                    t = {
                        "authors": [
                        ]
                    }
                    json.dump(t, f, indent=2)

                # load the json back in
                with open(authors_json, 'r') as f:
                    load_authors = json.load(f)

                # load them all back into load_authors
                for i in authors:
                    load_authors["authors"].append({
                        "name": i
                    })

                # finalize json
                with open(authors_json, 'w') as f:
                    json.dump(load_authors, f, indent=2)

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
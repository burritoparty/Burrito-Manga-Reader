import shutil
import time
import tkinter.ttk
from tkinter import ttk
import customtkinter
import json
import os
import sys
from os import path
import customtkinter

from Database import black, dark_pink, light_pink
from Functions import *
from Library_Reader import BookFrame


def close(self):
    if self.delete_window:
        # yeet the reader window
        self.delete_window.destroy()
        self.delete_window = None


def focus_delete(self):
    assert self
    self.lift()
    self.focus()


class DeleteFrame(customtkinter.CTkFrame):

    def delete_button_action(self, library_json, bookframe, tag_json, author_json):
        book_name: str
        book_name = self.combobox.get()
        book_path: str

        # time to open the json and remove the shit
        with open(library_json) as f:
            # load the library
            books_json = json.load(f)

            # make a new library
            new_books_json = {
                "book": [
                ]
            }
            for b in books_json['book']:
                # if b's name matches our current book's name
                if b['name'] == book_name:
                    shutil.rmtree(b['path'])
                    # print(b)
                else:
                    new_books_json['book'].append({
                        "path": b['path'],
                        "name": b['name'],
                        "author": b['author'],
                        "link": b['link'],
                        "read_later": b['read_later'],
                        "favorite": b['favorite'],
                        "tagged": b['tagged']
                    })

            # dump the new library in
            with open(library_json, 'w') as f:
                json.dump(new_books_json, f, indent=4)

            # reload the main window here
            bookframe.initialize_self()
            bookframe.load_tab(tag_json, author_json)

            close(self)

    def delete_button_callback(self, library_json, bookframe, tag_json, author_json):
        start_time = time.time()
        close(self) # TODO stupid code
        if self.delete_window is None:
            self.delete_window = customtkinter.CTkToplevel()
            self.delete_window.title("Delete a Book")
            self.delete_window.attributes('-topmost', 1)

            def check_input(event):
                value = event.widget.get()

                if value == '':
                    self.combobox['values'] = book_names
                else:
                    data = []
                    for item in book_names:
                        if value.lower() in item.lower():
                            data.append(item)

                    self.combobox['values'] = data

            self.combobox = ttk.Combobox(self.delete_window)

            self.delete_info_label = customtkinter.CTkLabel(self.delete_window,
                                                            font=("Roboto", 20),
                                                            text_color=light_pink,
                                                            text="Select the name of the book to delete:")
            book_names = []

            with open(library_json) as f:
                # load the library
                books_json = json.load(f)
                for b in books_json['book']:
                    # if b's name matches our current book's name
                    book_names.append(b['name'])

            self.combobox['values'] = book_names
            self.combobox.bind('<KeyRelease>', check_input)

            self.delete_window_button = customtkinter.CTkButton(self.delete_window,
                                                                fg_color=light_pink,
                                                                hover_color=dark_pink,
                                                                text_color=black,
                                                                text="Delete",
                                                                command=lambda x=library_json, b=bookframe,
                                                                               y=tag_json, z=author_json:
                                                                self.delete_button_action(x, b, y, z))

            self.combobox.grid(row=1, padx=20, pady=20)
            self.delete_info_label.grid(row=0, padx=20, pady=20)
            self.delete_window_button.grid(row=2, padx=20, pady=20)

            end_time = int(((time.time() - start_time) * 1000) + 10)
            end_time = end_time + 100
            self.after(end_time, focus_delete(self))

        else:
            close(self) # TODO for whatever fuckin' reason i cannot get this window to act right

    def __init__(self, library_json, authors_json, tag_json: str, bookframe, master: customtkinter.CTk, **kwargs):
        super().__init__(master, **kwargs)

        self.combobox = None
        self.delete_window = None

        delete = Image.open(resource(os.path.join('button_icons', 'remove_icon.png')))
        ctk_delete = customtkinter.CTkImage(dark_image=delete)

        self.delete_label = customtkinter.CTkLabel(self,
                                                   compound="left",
                                                   anchor="center",
                                                   font=("Roboto", 20),
                                                   text_color=light_pink,
                                                   text="Delete")

        self.delete_button = customtkinter.CTkButton(self,
                                                     image=ctk_delete,
                                                     compound="left",
                                                     anchor="center",
                                                     text="Delete Book",
                                                     fg_color=light_pink,
                                                     text_color=black,
                                                     hover_color=dark_pink,
                                                     command=lambda x=library_json, b=bookframe,
                                                                    y=tag_json, z=authors_json:
                                                     self.delete_button_callback(x, b, y, z))

        self.delete_label.grid(row=0, column=0, padx=20, pady=20)
        self.delete_button.grid(row=1, column=0, padx=20, pady=20)

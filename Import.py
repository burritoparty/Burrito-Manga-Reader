import json
import os
import shutil
import time
from tkinter.filedialog import askdirectory

import customtkinter
from PIL import Image

from Book import Book
from Database import black, dark_pink, light_pink
from Functions import *


class ImportFrame(customtkinter.CTkFrame):

    def open_import_window(self, library_frame, tag_json, authors_json):

        if self.import_window is None or not self.import_window.winfo_exists():
            # create window if its None or destroyed
            self.import_window = ImportWindow(
                library_json=self.library_json,
                library_path=self.library_path,
                tag_json=tag_json,
                authors_json=authors_json,
                book_frame=library_frame, master=self)
        else:
            self.import_window.focus()  # if window exists focus it

    def __init__(self, library_path, library_json, tag_json, authors_json, bookframe, master, **kwargs):
        super().__init__(master, **kwargs)
        self.library_path = library_path
        self.library_json = library_json

        self.label = customtkinter.CTkLabel(
            self, text="Library", text_color=light_pink)

        # add new book button
        self.import_book = customtkinter.CTkButton(self,
                                                   text="Import Book",
                                                   fg_color=light_pink,
                                                   text_color=black,
                                                   hover_color=dark_pink,
                                                   command=lambda
                                                       x=bookframe,
                                                       y=tag_json,
                                                       z=authors_json:
                                                   self.open_import_window(x, y, z))
        self.import_window = None

        self.import_library = customtkinter.CTkButton(self,
                                                      text="Import Library",
                                                      fg_color=light_pink,
                                                      text_color=black,
                                                      hover_color=dark_pink)

        self.export_library = customtkinter.CTkButton(self,
                                                      text="Export Library",
                                                      fg_color=light_pink,
                                                      text_color=black,
                                                      hover_color=dark_pink)
        self.label.grid(row=0, column=0)
        self.import_book.grid(row=1, column=0, padx=20, pady=20)
        self.import_library.grid(row=2, column=0, padx=20, pady=20)
        self.export_library.grid(row=3, column=0, padx=20, pady=20)


class ImportWindow(customtkinter.CTkToplevel):

    def input_path(self):
        # changed to pull the window back to the top after path is selected
        self.path = askdirectory()
        self.after(1, self.focus_import)

        images = []
        valid_images = [".jpg", ".png"]

        # IDK how to get the first image in this path so.... this works... :shrug:
        if self.path != '':
            for f in os.listdir(self.path):
                ext = os.path.splitext(f)[1]
                if ext.lower() not in valid_images:
                    continue
                images.append(Image.open(os.path.join(self.path, f)))

            cover = customtkinter.CTkImage(
                dark_image=add_corners(images[0], 25), size=(200, 275))
            cover = customtkinter.CTkLabel(self, image=cover, text=None)
            cover.grid(row=0, column=0, rowspan=3, padx=20, pady=20)

            if self.name_entry.get() == "":
                self.name_entry.insert(0, os.path.basename(self.path))

    def input_tag(self, tag):
        self.tagged.append(tag)

    def finalize_book(self, book_frame, tag_json):
        if self.path is not None and self.author_cbox.get() != "" and self.name_entry.get() != "" and self.link_entry.get() != "":
            if self.path != '':
                self.author = self.author_cbox.get()
                self.name = self.name_entry.get()
                self.link = self.link_entry.get()

                # now create and store book?
                # TODO get access to program files?
                library_path = self.library_path
                book = Book(self.path, self.name, self.author,
                            self.link, self.tagged)

                # TODO need to restrict how long the name is for formatting reasons
                # make new path based on name / .strip() to remove the whitespace from the end
                self.name = self.name.strip()
                # strip the path of all illegal characters
                strip_name = self.name
                strip_name = strip_name.replace('/', '')
                strip_name = strip_name.replace('\\', '')
                strip_name = strip_name.replace(':', '')
                strip_name = strip_name.replace('*', '')
                strip_name = strip_name.replace('?', '')
                strip_name = strip_name.replace('"', '')
                strip_name = strip_name.replace('<', '')
                strip_name = strip_name.replace('>', '')
                strip_name = strip_name.replace('|', '')
                strip_name = strip_name.strip()
                newpath = os.path.join(library_path, strip_name)
                os.mkdir(os.path.join(library_path, newpath))

            # copy from old path to new path

                files = os.listdir(self.path)
                for i in files:
                    shutil.copy(os.path.join(self.path, i),
                                os.path.join(newpath, i))

                # now update object's path
                book.path = newpath

                # import to JSON
                if os.path.isfile(self.library_json) is False:
                    print("FILE NOT FOUND")
                else:
                    with open(self.library_json) as f:
                        books_json = json.load(f)

                    books_json['book'].append({
                        "path": book.get_path(),
                        "name": book.get_name(),
                        "author": book.get_author(),
                        "link": book.get_link(),
                        "tagged": book.get_tags()
                    })

                    with open(self.library_json, 'w') as f:
                        json.dump(books_json, f, indent=4)

                    # update the library count here
                    book_frame.load_tab(tag_json)
                    book_frame.initialize_self()
                    book_frame.load_tab(tag_json)

                self.destroy()

            else:
                # this is for if the user presses the cancel button in the path entry
                self.lower()
                error_window = customtkinter.CTkToplevel()
                error_window.attributes('-topmost', 2)
                error_window.geometry('150x100+1275+720')
                error_window.grid_columnconfigure(0, weight=1)
                error_window.columnconfigure(0, weight=1)
                label = customtkinter.CTkLabel(
                    error_window, text="Path invalid")
                label.grid(row=0, column=0, padx=10, pady=10)

        else:
            self.lower()
            error_window = customtkinter.CTkToplevel()
            error_window.attributes('-topmost', 2)
            error_window.geometry('150x100+1275+720')
            error_window.grid_columnconfigure(0, weight=1)
            error_window.columnconfigure(0, weight=1)
            label = customtkinter.CTkLabel(
                error_window, text="Missing either: \nLink, \nName, \nAuthor")
            label.grid(row=0, column=0, padx=10, pady=10)




    def focus_import(self):
        assert self
        self.focus()

    def __init__(self, library_path, library_json, tag_json, authors_json, book_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # this is keeping the window at the top
        self.title("Import Book")
        # TODO not very centered :/
        # print("width: " + str(self.winfo_width()) + " screenwidth: " + str(self.winfo_screenwidth()))
        # print("height: " + str(self.winfo_height()) + " screenheight: " + str(self.winfo_screenheight()))
        # print("x: " + str(get_x_coordinates(self.winfo_width(), self.winfo_screenwidth())))
        # print("y: " + str(get_y_coordinates(self.winfo_height(), self.winfo_screenheight())))
        self.geometry('%d+%d' % (
            800, 400
        ))

        # make attributes for new book
        self.path = None
        self.name = None
        self.author = None
        self.link = None
        self.tagged: list[str] = []
        self.library_path = library_path
        self.library_json = library_json

        label = customtkinter.CTkLabel(self, text="placeholder image")
        label.grid(row=0, column=0, padx=20, pady=20, rowspan=3)

        self.link_entry = customtkinter.CTkEntry(
            self, placeholder_text="Enter Link", width=750)
        self.link_entry.grid(row=0, column=1, padx=20, pady=20)

        # TODO set string limit to 65 chars
        self.name_entry = customtkinter.CTkEntry(
            self, placeholder_text="Enter Name", width=750)
        self.name_entry.grid(row=1, column=1, padx=20, pady=20)

        # get from JSON
        # grab from the JSON and append to array
        # load the JSON
        authors = []
        with open(authors_json, 'r') as f:
            load_authors = json.load(f)

        # load the tag names from the JSON into an array
        for i in load_authors['authors']:
            authors.append(i['name'])

        print(authors)

        self.author_cbox = customtkinter.CTkComboBox(self,
                                                     values=authors,
                                                     fg_color=light_pink,
                                                     text_color=black,
                                                     dropdown_fg_color=light_pink,
                                                     dropdown_hover_color=dark_pink,
                                                     dropdown_text_color=black,
                                                     state="readonly")
        self.author_cbox.grid(row=2, column=1, padx=20, pady=20)

        # TODO long tag names do not fit
        self.tag_frame = customtkinter.CTkScrollableFrame(self, label_text="Select Tags",
                                                          width=1100, label_text_color=light_pink)
        # align checkbox columns
        self.tag_frame.columnconfigure(0, weight=1)
        self.tag_frame.columnconfigure(1, weight=1)
        self.tag_frame.columnconfigure(2, weight=1)
        self.tag_frame.columnconfigure(3, weight=1)
        self.tag_frame.columnconfigure(4, weight=1)
        self.tag_frame.columnconfigure(5, weight=1)
        self.tag_frame.columnconfigure(6, weight=1)
        self.tag_frame.grid(row=4, column=0, columnspan=4, padx=20, pady=20)

        num_loops = 0
        r = 0
        c = 0

        # grab from the JSON and append to array
        # load the JSON
        tags = []
        with open(tag_json, 'r') as f:
            load_tags = json.load(f)

        # load the tag names from the JSON into an array
        for i in load_tags['tags']:
            tags.append(i['name'])

        for i in tags:
            self.checkbox = customtkinter.CTkCheckBox(self.tag_frame, text=i,
                                                      command=lambda x=i: self.tagged.append(
                                                          x),
                                                      hover_color=light_pink, fg_color=dark_pink,
                                                      text_color=light_pink)
            self.checkbox.grid(row=r, column=c, pady=15, padx=15)

            if c == 7:
                c = 0
                r += 1
            else:
                c += 1
            num_loops += 1

        self.submit_button = customtkinter.CTkButton(self, text="Submit",
                                                     command=lambda x=book_frame, y=tag_json: self.finalize_book(
                                                         x, y),
                                                     fg_color=light_pink, hover_color=dark_pink, text_color=black)
        self.submit_button.grid(row=1, column=3, padx=20, pady=20)

        self.cancel_button = customtkinter.CTkButton(self, text="Cancel", command=self.destroy,
                                                     fg_color=light_pink, hover_color=dark_pink, text_color=black)
        self.cancel_button.grid(row=2, column=3, padx=20, pady=20)

        self.get_path_button = customtkinter.CTkButton(self, text="Select Book", command=self.input_path,
                                                       fg_color=light_pink, hover_color=dark_pink, text_color=black)
        self.get_path_button.grid(row=0, column=3)

        # pulls window to the front
        self.after(1, self.focus_import)
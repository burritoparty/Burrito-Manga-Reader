import json
import os
import shutil
from tkinter.filedialog import askdirectory
import customtkinter
from PIL import Image
from Book import Book
from Database import *
from Functions import *


class ImportFrame(customtkinter.CTkFrame):

    def open_import_window(self):

        if self.import_window is None or not self.import_window.winfo_exists():
            self.import_window = ImportWindow(self)  # create window if its None or destroyed
        else:
            self.import_window.focus()  # if window exists focus it

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = customtkinter.CTkLabel(self, text="Library", text_color=light_pink)

        # add new book button
        self.import_book = customtkinter.CTkButton(self,
                                                   text="Import Book",
                                                   fg_color=light_pink,
                                                   text_color=black,
                                                   hover_color=dark_pink,
                                                   command=self.open_import_window)
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
        self.path = askdirectory()

        images = []
        valid_images = [".jpg", ".png"]

        # idk how to get the first image in this path so.... this works... :shrug:
        for f in os.listdir(self.path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_images:
                continue
            images.append(Image.open(os.path.join(self.path, f)))

        cover = customtkinter.CTkImage(dark_image=images[0], size=(150, 250))
        cover = customtkinter.CTkLabel(self, image=cover, text=None)
        cover.grid(row=0, column=0, rowspan=3, padx=20, pady=20)

        if self.name_entry.get() == "":
            self.name_entry.insert(0, os.path.basename(self.path))

    def input_tag(self, tag):
        self.tagged.append(tag)

    def finalize_book(self):
        if self.path is not None and self.author_cbox.get() != "" and self.name_entry.get() != "" and self.link_entry.get() != "":
            self.author = self.author_cbox.get()
            self.name = self.name_entry.get()
            self.link = self.link_entry.get()

            # now create and store book?
            # TODO get access to program files?
            library_path = "D:\Burrito Manga Reader"
            book = Book(self.path, self.name, self.author, self.link, self.tagged)

            # make new path based on name
            newpath = (library_path + "\\" + self.name)
            os.mkdir(library_path + "\\" + self.name)

            # copy from old path to new path
            files = os.listdir(self.path)
            for i in files:
                shutil.copy(self.path + "\\" + i, newpath + "\\" + i)

            # now update object's path
            book.path = newpath

            # import to json
            if os.path.isfile("D:\Burrito Manga Reader\library.json") is False:
                print("FILE NOT FOUND")
            else:
                with open("D:\Burrito Manga Reader\library.json") as f:
                    books_json = json.load(f)

                books_json['book'].append({
                    "path": book.get_path(),
                    "name": book.get_name(),
                    "author": book.get_author(),
                    "link": book.get_link(),
                    "tagged": book.get_tags()
                })

                with open("D:\Burrito Manga Reader\library.json", 'w') as f:
                    json.dump(books_json, f, indent=4)

            self.destroy()

        else:
            self.lower()
            error_window = customtkinter.CTkToplevel()
            error_window.attributes('-topmost', 2)
            error_window.geometry('1275+720')
            label = customtkinter.CTkLabel(error_window, text="Missing an attribute")
            label.pack()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # this is keeping the window at the top
        self.attributes('-topmost', 1)
        self.title("Import Book")
        # TODO not very centered :/
        self.geometry('%d+%d' % (
            get_x_coordinates(self.winfo_width(), self.winfo_screenwidth()),
            get_y_coordinates(self.winfo_height(), self.winfo_screenheight())
        ))

        # make attributes for new book
        self.path = None
        self.name = None
        self.author = None
        self.link = None
        self.tagged = []

        label = customtkinter.CTkLabel(self, text="placeholder image")
        label.grid(row=0, column=0, padx=20, pady=20, rowspan=3)

        self.link_entry = customtkinter.CTkEntry(self, placeholder_text="Enter Link")
        self.link_entry.grid(row=0, column=1, padx=20, pady=20)

        # TODO set string limit to 65 chars
        self.name_entry = customtkinter.CTkEntry(self, placeholder_text="Enter Name")
        self.name_entry.grid(row=1, column=1, padx=20, pady=20)

        # TODO add autocomplete, https://github.com/TomSchimansky/CustomTkinter/issues/255
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
                                                          width=450, label_text_color=light_pink)
        self.tag_frame.grid(row=4, column=0, columnspan=4, padx=20, pady=20)

        num_loops = 0
        r = 0
        c = 0
        for i in tags:
            self.checkbox = customtkinter.CTkCheckBox(self.tag_frame, text=i,
                                                      command=lambda x=i: self.tagged.append(x),
                                                      hover_color=light_pink, fg_color=dark_pink,
                                                      text_color=light_pink)
            self.checkbox.grid(row=r, column=c, pady=(20, 0), padx=20)

            if c == 2:
                c = 0
                r += 1
            else:
                c += 1
            num_loops += 1

        self.submit_button = customtkinter.CTkButton(self, text="Submit", command=self.finalize_book,
                                                     fg_color=light_pink, hover_color=dark_pink, text_color=black)
        self.submit_button.grid(row=1, column=3, padx=20, pady=20)

        self.cancel_button = customtkinter.CTkButton(self, text="Cancel", command=self.destroy,
                                                     fg_color=light_pink, hover_color=dark_pink, text_color=black)
        self.cancel_button.grid(row=2, column=3, padx=20, pady=20)

        self.get_path_button = customtkinter.CTkButton(self, text="Select Book", command=self.input_path,
                                                       fg_color=light_pink, hover_color=dark_pink, text_color=black)
        self.get_path_button.grid(row=0, column=3)
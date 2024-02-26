import json
import os
import re
import shutil
import time
import tkinter
from tkinter.filedialog import askdirectory

from tkinter import *
from tkinter import ttk

import customtkinter
from PIL import Image

from Book import Book
from CTkScrollableDropdown import *
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

        import_icon = Image.open(resource(os.path.join('button_icons', 'import_icon.png')))
        ctk_import = customtkinter.CTkImage(dark_image=import_icon)

        # add new book button
        self.import_book = customtkinter.CTkButton(self,
                                                   image=ctk_import,
                                                   compound="left",
                                                   anchor="center",
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

        self.import_book.grid(row=0, column=0, padx=20, pady=20)


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
                break

            # checking if path is valid
            if len(images) > 0:
                w, h = images[0].size
                if w > h:
                    images[0].resize((275, 200))
                    cover = customtkinter.CTkImage(
                        dark_image=images[0], size=(275, 200))
                else:
                    images[0].resize((200, 275))
                    cover = customtkinter.CTkImage(
                        dark_image=images[0], size=(200, 275))

                cover = customtkinter.CTkLabel(self, image=cover, text="")
                cover.grid(row=0, column=3, rowspan=3, padx=20, pady=20)

                if self.name_entry.get() == "":
                    # format the string to remove brackets, parenthesis, curly brackets and their contents
                    format = re.sub("\\(.*?\\)", "", os.path.basename(self.path))
                    format = re.sub("\\[.*?\\]", "", format)
                    format = re.sub("\\{.*?\\}", "", format)
                    format = re.sub("\\=.*?\\=", "", format)
                    format = format.strip()
                    # removes characters before two spaces
                    format = re.sub(r'^.*?  ', '  ', format)
                    format = re.sub(r'^.*?｜', '｜', format)
                    format = re.sub(r'^.*? - ', ' - ', format)

                    format = format.replace('_', '')
                    format = format.replace(' - ', '')
                    format = format.replace('｜', '')
                    format = format.strip()
                    self.name_entry.insert(0, format)
            else:
                error_window = customtkinter.CTkToplevel()
                error_window.attributes('-topmost', 2)
                error_window.geometry('150x100+1275+720')
                error_window.grid_columnconfigure(0, weight=1)
                error_window.columnconfigure(0, weight=1)
                label = customtkinter.CTkLabel(
                    error_window, text="Path invalid")
                label.grid(row=0, column=0, padx=10, pady=10)
                self.after(100, self.focus_import)

    def input_tag(self, tag):
        self.tagged.append(tag)

    def finalize_book(self, book_frame, tag_json, authors_json):

        # making sure the author input is valid
        authors = []
        # load an array with current authors
        with open(authors_json, 'r') as f:
            load_authors = json.load(f)
        # load the author names from the JSON into an array
        for i in load_authors['authors']:
            authors.append(i['name'])

        # making sure the author input is valid
        author_exists = False
        for i in authors:
            if i == self.author_cbox.get():
                author_exists = True

        # making sure the author input is valid
        if author_exists is False:
            self.lower()
            error_window = customtkinter.CTkToplevel()
            error_window.attributes('-topmost', 2)
            error_window.geometry('1275+720')
            error_window.grid_columnconfigure(0, weight=1)
            error_window.columnconfigure(0, weight=1)
            label = customtkinter.CTkLabel(
                error_window, text="The author that was input\n is not in the library")
            label.grid(row=0, column=0, padx=10, pady=10)
        else:
            # making sure no inputs were left empty
            if self.path is not None and self.author_cbox.get() != "" and self.name_entry.get() != "":

                library_path = self.library_path

                # make new path based on name / .strip() to remove the whitespace from the end
                self.name = self.name_entry.get()
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
                strip_name = strip_name.replace('.', '')
                strip_name = strip_name.strip()
                new_path = os.path.join(library_path, strip_name)

                # check if the path exists
                if not os.path.exists(new_path):
                    if self.path != '':
                        os.mkdir(new_path)
                        self.author = self.author_cbox.get()
                        self.link = self.link_entry.get()

                        # now create and store book

                        book = Book(self.path, self.name, self.author,
                                    self.link, self.read_later, self.favorite, self.tagged)

                        # copy from old path to new path

                        files = os.listdir(self.path)
                        for i in files:
                            shutil.copy(os.path.join(self.path, i),
                                        os.path.join(new_path, i))

                        # now update object's path
                        book.path = new_path

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
                                "read_later": book.read_later,
                                "favorite": book.favorite,
                                "tagged": book.get_tags()
                            })

                            with open(self.library_json, 'w') as f:
                                json.dump(books_json, f, indent=4)

                            # update the library count here
                            book_frame.initialize_self()
                            book_frame.load_tab(tag_json, authors_json)

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
                        error_window, text="Filepath exists in library")
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

    def make_new_author(self, authors_json: str):
        authors = []
        authors_append_dialogue = customtkinter.CTkInputDialog(
            text="New Author: ", title="Append a new author",
            button_fg_color=light_pink,
            button_text_color=black,
            button_hover_color=dark_pink)
        authors_append_dialogue.geometry('340+220')

        # load the JSON
        with open(authors_json, 'r') as f:
            load_authors = json.load(f)

        # load the tag names from the JSON into an array
        for i in load_authors['authors']:
            authors.append(i['name'])

        # get the input from the user
        new_author = authors_append_dialogue.get_input()

        # check if the input is valid
        if new_author == '' or new_author is None:
            # user hit the cancel button
            pass
        elif check_exists(new_author, authors, False) is False:
            error = customtkinter.CTkToplevel()
            error.geometry("340+220")
            label = customtkinter.CTkLabel(error,
                                           text="this Author already exists",
                                           font=("Roboto", 20))
            label.grid(padx=10, pady=10)
        else:
            # append the new tag to the array
            authors.append(new_author)
            authors.sort()

            # delete all the authors
            del load_authors['authors']

            # delete ['authors'] object from JSON
            with open(authors_json, 'w') as f:
                json.dump(load_authors, f, indent=2)

            # load the ['authors'] object back into JSON
            with open(authors_json, 'w') as f:
                t = {
                    "authors": [
                    ]
                }
                json.dump(t, f, indent=2)

            # load the JSON back in
            with open(authors_json, 'r') as f:
                load_authors = json.load(f)

            # load them all back into load_authors
            for i in authors:
                load_authors["authors"].append({
                    "name": i
                })

            # finalize JSON
            with open(authors_json, 'w') as f:
                json.dump(load_authors, f, indent=2)

        # reload the cbox

        self.author_cbox['values'] = authors
        self.author_cbox.grid(row=2, column=0)


        # # reload the cbox
        # self.author_cbox = customtkinter.CTkComboBox(self, width=750)
        # self.author_cbox.grid(row=2, column=0)
        # if len(authors) != 0:
        #     CTkScrollableDropdown(self.author_cbox, values=authors, justify="left", button_color="transparent",
        #                           resize=False, autocomplete=True,
        #                           frame_border_color=light_pink, scrollbar_button_hover_color=light_pink)
        #
        #     self.author_cbox.set("")
        #
        # # set the new author into the combobox
        # self.author_cbox.set(new_author)
        #
        # # focus the import window
        # self.after(250, self.focus_import)

    def read_later_callback(self, unread, read):
        if self.read_later:
            self.read_later = False
            self.read_later_button.configure(image=unread)
        else:
            self.read_later = True
            self.read_later_button.configure(image=read)

    def favorite_callback(self, unfave, fave):
        if self.favorite:
            self.favorite = False
            self.favorite_button.configure(image=unfave)
        else:
            self.favorite = True
            self.favorite_button.configure(image=fave)

    def focus_import(self):
        assert self
        self.lift()
        self.focus_force()

    def __init__(self, library_path, library_json, tag_json, authors_json, book_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.combo_box = None
        start_time = time.time()

        self.title("Import Book")
        self.geometry('550+220')
        self.attributes('-topmost')

        # make attributes for new book
        self.path = None
        self.name = None
        self.author = None
        self.link = None
        self.read_later = False
        self.favorite = False
        self.tagged: list[str] = []
        self.library_path = library_path
        self.library_json = library_json

        self.link_entry = customtkinter.CTkEntry(
            self, placeholder_text="Enter Link", width=750)
        self.link_entry.grid(row=0, column=0, padx=20, pady=20)

        self.name_entry = customtkinter.CTkEntry(
            self, placeholder_text="Enter Name", width=750)
        self.name_entry.grid(row=1, column=0, padx=20, pady=20)

        # get from JSON
        # grab from the JSON and append to array
        # load the JSON
        # authors = []
        # with open(authors_json, 'r') as f:
        #     load_authors = json.load(f)
        #
        # # load the tag names from the JSON into an array
        # for i in load_authors['authors']:
        #     authors.append(i['name'])
        #
        # self.author_cbox = customtkinter.CTkComboBox(self, width=750)
        #
        # self.author_cbox.grid(row=2, column=0)
        #
        # if len(authors) != 0:
        #     CTkScrollableDropdown(self.author_cbox, values=authors, justify="left", button_color="transparent",
        #                           resize=False, autocomplete=True,
        #                           frame_border_color=light_pink, scrollbar_button_hover_color=light_pink)
        #
        #     self.author_cbox.set("")

        authors = []

        with open(authors_json, 'r') as f:
            load_authors = json.load(f)

        # load the tag names from the JSON into an array
        for i in load_authors['authors']:
            authors.append(i['name'])


        def check_input(event):
            value = event.widget.get()

            if value == '':
                self.author_cbox['values'] = authors
            else:
                data = []
                for item in authors:
                    if value.lower() in item.lower():
                        data.append(item)

                self.author_cbox['values'] = data

        self.author_cbox = ttk.Combobox(self)
        self.author_cbox['values'] = authors
        self.author_cbox.bind('<KeyRelease>', check_input)
        self.author_cbox.grid(row=2, column=0)



        self.tag_frame = customtkinter.CTkScrollableFrame(self, label_text="Select Tags",
                                                          width=1600, height=575, label_text_color=light_pink)
        # align checkbox columns
        self.tag_frame.columnconfigure(0, weight=1)
        self.tag_frame.columnconfigure(1, weight=1)
        self.tag_frame.columnconfigure(2, weight=1)
        self.tag_frame.columnconfigure(3, weight=1)
        self.tag_frame.columnconfigure(4, weight=1)
        self.tag_frame.columnconfigure(5, weight=1)
        self.tag_frame.columnconfigure(6, weight=1)
        self.tag_frame.grid(row=4, column=0, columnspan=5, padx=20, pady=20)

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
                                                      checkbox_height=35, checkbox_width=35, font=("Roboto", 16),
                                                      command=lambda x=i: self.tagged.append(x),
                                                      hover_color=light_pink, fg_color=dark_pink,
                                                      text_color=light_pink)
            self.checkbox.grid(row=r, column=c, pady=10, padx=10, sticky='w')

            if c == 9:
                c = 0
                r += 1
            else:
                c += 1
            num_loops += 1

        self.submit_button = customtkinter.CTkButton(self, text="Submit Book",
                                                     command=lambda x=book_frame, y=tag_json, z=authors_json:
                                                     self.finalize_book(x, y, z),
                                                     fg_color=light_pink, hover_color=dark_pink, text_color=black)
        self.submit_button.grid(row=1, column=1, padx=20, pady=20)

        self.add_author_button = customtkinter.CTkButton(self, text="Add an author",
                                                         command=lambda x=authors_json: self.make_new_author(x),
                                                         fg_color=light_pink, hover_color=dark_pink, text_color=black)
        self.add_author_button.grid(row=2, column=1, padx=20, pady=20)

        self.get_path_button = customtkinter.CTkButton(self, text="Select Book", command=self.input_path,
                                                       fg_color=light_pink, hover_color=dark_pink, text_color=black)
        self.get_path_button.grid(row=0, column=1)

        unread_later = Image.open(resource(os.path.join('button_icons', 'unread_later.png')))
        ctk_unread = customtkinter.CTkImage(dark_image=unread_later)
        read_later = Image.open(resource(os.path.join('button_icons', 'read_later.png')))
        ctk_read = customtkinter.CTkImage(dark_image=read_later)

        unfavorite = Image.open(resource(os.path.join('button_icons', 'unfavorite.png')))
        ctk_unfavorite = customtkinter.CTkImage(dark_image=unfavorite)
        favorite = Image.open(resource(os.path.join('button_icons', 'favorite.png')))
        ctk_favorite = customtkinter.CTkImage(dark_image=favorite)

        self.read_later_button = customtkinter.CTkButton(self, text="Read Later", compound="left",
                                                         command=lambda x=ctk_unread, y=ctk_read:
                                                         self.read_later_callback(x, y), image=ctk_unread,
                                                         fg_color=light_pink, hover_color=dark_pink, text_color=black)
        self.favorite_button = customtkinter.CTkButton(self, text="Favorite", compound="left",
                                                       command=lambda x=ctk_unfavorite, y=ctk_favorite:
                                                       self.favorite_callback(x, y), image=ctk_unfavorite,
                                                       fg_color=light_pink, hover_color=dark_pink, text_color=black)
        self.read_later_button.grid(row=0, column=2, rowspan=2, padx=20, pady=20)
        self.favorite_button.grid(row=1, column=2, rowspan=2, padx=20, pady=20)

        # get the time it takes function to run then wait that long until focus + 10
        end_time = int(((time.time() - start_time) * 1000) + 10)
        # print("--- %s seconds ---" % (end_time))

        # pulls window to the front
        self.after(end_time, self.focus_import)

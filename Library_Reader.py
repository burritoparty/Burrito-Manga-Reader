import gc
import json
import math
import os
import time
from os import path
from tkinter import ttk
import subprocess
from tkinter import filedialog
from tkinter import *

import customtkinter
from concurrent.futures import ThreadPoolExecutor

from Book import Book
from CTkScrollableDropdown import CTkScrollableDropdown
from Database import black, dark_pink, light_pink
from Functions import *


# test line

def _create_book(book_json_entry: dict) -> Book:
    return Book(
        book_json_entry["path"],
        book_json_entry["name"],
        book_json_entry["author"],
        book_json_entry["link"],
        book_json_entry["tagged"],
    )


def checking(tagged: list, check: str):
    if check not in tagged:
        tagged.append(check)
    else:
        tagged.remove(check)


def open_file_location(path):
    # r'explorer /select,"C:\"'
    final_path = r'explorer /open,"' + path
    subprocess.Popen(final_path)


class BookFrame(customtkinter.CTkScrollableFrame):

    def focus_reader(self):
        assert self.reader_window
        self.reader_window.focus()

    def close_reader(self):
        if self.reader_window:
            # yeet the reader window
            self.reader_window.destroy()
            self.reader_window = None

    def next_page(self):
        if self.current_page_num < len(self.page_list) - 1:

            if self.page:
                # destroy current items
                self.page.destroy()
            if self.pagenum_label:
                self.pagenum_label.destroy()

            # update page number
            self.current_page_num += 1

            # change
            self.page = customtkinter.CTkLabel(self.reader_window,
                                               image=self.page_list[self.current_page_num], text="")
            self.page.grid(row=0, column=0, columnspan=3)

            # update the user's page counter
            self.pagenum_text = str(
                str(self.current_page_num + 1) + " / " + str(len(self.page_list)))
            self.pagenum_label = customtkinter.CTkLabel(
                self.reader_window, text=self.pagenum_text, font=("Roboto", 20))
            self.pagenum_label.grid(row=1, column=1)

    def prev_page(self):
        if self.current_page_num != 0:
            assert self.page
            assert self.pagenum_label

            # destroy current items
            self.page.destroy()
            self.pagenum_label.destroy()

            # update page number
            self.current_page_num -= 1

            # change the page
            self.page = customtkinter.CTkLabel(self.reader_window,
                                               image=self.page_list[self.current_page_num], text="")
            self.page.grid(row=0, column=0, columnspan=3)

            # update the user's page counter
            self.pagenum_text = str(
                str(self.current_page_num + 1) + " / " + str(len(self.page_list)))
            self.pagenum_label = customtkinter.CTkLabel(
                self.reader_window, text=self.pagenum_text, font=("Roboto", 20))
            self.pagenum_label.grid(row=1, column=1)

    def open_reader(self, book: Book):
        if self.reader_window is None or not self.reader_window.winfo_exists():
            assert self.book_window

            self.reader_window = customtkinter.CTkToplevel()
            self.reader_window.attributes('-fullscreen', True)

            self.reader_window.bind('a', lambda _: self.prev_page())
            self.reader_window.bind('<Left>', lambda _: self.prev_page())
            self.reader_window.bind('d', lambda _: self.next_page())
            self.reader_window.bind('<Right>', lambda _: self.next_page())
            self.reader_window.bind('<Escape>', lambda _: self.close_reader())

            self.reader_window.grid_rowconfigure(0, weight=1)
            self.reader_window.grid_columnconfigure(0, weight=1)
            self.reader_window.grid_columnconfigure(1, weight=1)
            self.reader_window.grid_columnconfigure(2, weight=1)

            # get pages
            self.page_list = book.get_pages(False)

            # counting shit
            self.current_page_num = 0
            self.pagenum_text = str(
                str(self.current_page_num + 1) + " / " + str(len(self.page_list)))
            self.pagenum_label = customtkinter.CTkLabel(
                self.reader_window, text=self.pagenum_text, font=("Roboto", 20))

            next = Image.open(resource(os.path.join('button_icons', 'next_icon.png')))
            ctk_next = customtkinter.CTkImage(dark_image=next)
            prev = Image.open(resource(os.path.join('button_icons', 'prev_icon.png')))
            ctk_prev = customtkinter.CTkImage(dark_image=prev)
            exit = Image.open(resource(os.path.join('button_icons', 'remove_icon.png')))
            ctk_exit = customtkinter.CTkImage(dark_image=exit)

            # buttons
            next_page = customtkinter.CTkButton(self.reader_window, command=self.next_page, image=ctk_next, text="",
                                                hover_color=dark_pink, fg_color=light_pink, text_color=black)
            prev_page = customtkinter.CTkButton(self.reader_window, command=self.prev_page, image=ctk_prev, text="",
                                                hover_color=dark_pink, fg_color=light_pink, text_color=black)
            close = customtkinter.CTkButton(self.reader_window, command=self.close_reader, image=ctk_exit, text="",
                                            hover_color=dark_pink, fg_color=light_pink, text_color=black)

            # page
            self.page = customtkinter.CTkLabel(
                self.reader_window, text="", image=self.page_list[0], compound="n")

            # place all the shit
            pad = 5
            self.page.grid(row=0, column=0, columnspan=3, padx=pad, pady=pad)
            prev_page.grid(row=1, column=0, padx=pad, pady=pad)
            self.pagenum_label.grid(row=1, column=1, padx=pad, pady=pad)
            next_page.grid(row=1, column=2, padx=pad, pady=pad)
            close.grid(row=2, column=1, padx=pad, pady=10)

        # Focus the reader window, but wait 1ms.
        # On Windows machines, the window doesn't always get focus, so keyboard
        # shortcuts won't work. But waiting a 1ms seems to ensure focus is
        # obtained.
        self.reader_window.after(1, self.focus_reader)

    def close_book_description(self):
        assert self.book_window

        self.book_window.destroy()
        # yeet that memory into the stratosphere!
        gc.collect()

    def name_update(self, book: Book, tag_json: str, authors_json: str):

        # check if the name has actually been changed
        if book.get_name() != self.book_name_entry.get() and self.book_name_entry.get() != '':
            with open(self.library_json) as f:
                # load the library
                books_json = json.load(f)
                for b in books_json['book']:
                    # if b's name matches our current book's name
                    if b['name'] == book.get_name():
                        b['name'] = self.book_name_entry.get()
                        book.name = self.book_name_entry.get()

                # write to the JSON
                with open(self.library_json, 'w') as f:
                    json.dump(books_json, f, indent=2)

                # update the read button on the book reader
                self.read_button.configure(text=self.book_name_entry.get())

                # updates the tab to refresh tags when clicked again
                self.load_tab(tag_json, authors_json)

        else:
            pass

    def link_update(self, book: Book, tag_json: str, authors_json):

        # check if the name has actually been changed
        if book.get_link() != self.book_link_entry.get():
            with open(self.library_json) as f:
                # load the library
                books_json = json.load(f)
                for b in books_json['book']:
                    # if b's name matches our current book's name
                    if b['link'] == book.get_link():
                        b['link'] = self.book_link_entry.get()
                        book.link = self.book_link_entry.get()

                # write to the JSON
                with open(self.library_json, 'w') as f:
                    json.dump(books_json, f, indent=2)

                # updates the tab to refresh tags when clicked again
                self.load_tab(tag_json, authors_json)

        else:
            pass

    def author_update(self, book: Book, tag_json: str, authors_json: str, authors: list[str]):
        # making sure the author input is valid
        author_exists = False
        for i in authors:
            if i == self.book_author_cbox.get():
                author_exists = True

        with open(self.library_json) as f:
            # load the library
            books_json = json.load(f)
            for b in books_json['book']:
                # if b's name matches our current book's name
                if b['path'] == book.get_path():
                    b['author'] = self.book_author_cbox.get()
                    book.author = self.book_author_cbox.get()

            # write to the JSON
            with open(self.library_json, 'w') as f:
                json.dump(books_json, f, indent=2)

            # updates the tab to refresh tags when clicked again
            self.load_tab(tag_json, authors_json)

    def append_new_tags(self, book: Book, tag_json: str, authors_json, checked_tag: str):
        if os.path.isfile(self.library_json) is False:
            print("FILE NOT FOUND")
        else:
            with open(self.library_json) as f:
                # load the library
                books_json = json.load(f)

                if check_exists(checked_tag, book.get_tags(), False):
                    # loops through book's JSON elements
                    for b in books_json['book']:
                        # if b's path matches our current book's path
                        if b['path'] == book.get_path():
                            # append the tag to the JSON
                            b['tagged'].append(checked_tag)
                            # and update the current objects tags
                            book.get_tags().append(checked_tag)
                else:
                    # loops through book's_JSON elements
                    for b in books_json['book']:
                        # if b's path matches our current book's path
                        if b['path'] == book.get_path():
                            # remove the tag from the JSON
                            b['tagged'].remove(checked_tag)
                            # and update the current objects tags
                            book.get_tags().remove(checked_tag)

                # write to the JSON
                with open(self.library_json, 'w') as f:
                    json.dump(books_json, f, indent=2)

                # updates the tab to refresh tags when clicked again
                self.load_tab(tag_json, authors_json)

    def read_book_callback(self, book: Book, tag_json: str, authors_json, unread, read):
        with open(self.library_json) as f:
            # load the library
            books_json = json.load(f)
            # loops through book's JSON elements
            for b in books_json['book']:
                # if b's path matches our current book's path
                if b['path'] == book.get_path():
                    # update read later
                    if book.read_later:
                        book.read_later = False
                        b['read_later'] = False
                        self.book_read_later_button.configure(image=unread)
                    else:
                        book.read_later = True
                        b['read_later'] = True
                        self.book_read_later_button.configure(image=read)

            # write to the JSON
            with open(self.library_json, 'w') as f:
                json.dump(books_json, f, indent=2)

            # updates the tab to refresh tags when clicked again
            self.load_tab(tag_json, authors_json)

    def favorite_book_callback(self, book: Book, tag_json: str, authors_json, unfavorite, favorite):
        with open(self.library_json) as f:
            # load the library
            books_json = json.load(f)
            # loops through book's JSON elements
            for b in books_json['book']:
                # if b's path matches our current book's path
                if b['path'] == book.get_path():
                    # update read later
                    if book.favorite:
                        book.favorite = False
                        b['favorite'] = False
                        self.book_favorite_button.configure(image=unfavorite)
                    else:
                        book.favorite = True
                        b['favorite'] = True
                        self.book_favorite_button.configure(image=favorite)

            # write to the JSON
            with open(self.library_json, 'w') as f:
                json.dump(books_json, f, indent=2)

            # updates the tab to refresh tags when clicked again
            self.load_tab(tag_json, authors_json)

    def focus_description(self):
        assert self.book_window
        self.book_window.focus()

    def open_book_description(self, book: Book, tag_json: str, authors_json: str):
        if self.book_window is None or not self.book_window.winfo_exists():
            self.reader_window = None
            self.book_window = customtkinter.CTkToplevel()
            self.book_window.geometry(f"{1920}x{1080}")
            self.book_window.title(book.get_name())
            #  sets to the center of the screen
            # print("width: " + str(self.winfo_width()) + " screenwidth: " + str(self.winfo_screenwidth()))
            # print("height: " + str(self.winfo_height()) + " screenheight: " + str(self.winfo_screenheight()))
            self.book_window.geometry('%d+%d' % (
                340, 220
            ))

            # pass in the authors for the combobox
            authors = []
            with open(authors_json, 'r') as f:
                load_authors = json.load(f)

            # load the tag names from the JSON into an array
            for i in load_authors['authors']:
                authors.append(i['name'])

            # center shit
            self.book_window.grid_columnconfigure(0, weight=1)
            self.book_window.grid_columnconfigure(1, weight=1)
            self.book_window.grid_columnconfigure(2, weight=1)

            # make widgets
            # read button, making new cover to resize
            self.read_button = customtkinter.CTkButton(self.book_window, compound="top", fg_color="transparent",
                                                       hover_color=dark_pink, font=("Roboto", 16),
                                                       image=book.get_full_cover(),
                                                       command=lambda x=book: self.open_reader(x),
                                                       text=indent_string(book.get_name()))

            # labels
            book_link_label = customtkinter.CTkLabel(self.book_window, text="Link", font=("Roboto", 20),
                                                     text_color=light_pink)
            book_name_label = customtkinter.CTkLabel(self.book_window, text="Name", font=("Roboto", 20),
                                                     text_color=light_pink)
            book_author_label = customtkinter.CTkLabel(self.book_window, text="Author", font=("Roboto", 20),
                                                       text_color=light_pink)

            book_page_count_label = customtkinter.CTkLabel(self.book_window, text="0", font=("Roboto", 20),
                                                           text_color=light_pink)

            # icons
            update = Image.open(resource(os.path.join('button_icons', 'update_icon.png')))
            ctk_update = customtkinter.CTkImage(dark_image=update)

            unread_later = Image.open(resource(os.path.join('button_icons', 'unread_later.png')))
            ctk_unread = customtkinter.CTkImage(dark_image=unread_later)
            read_later = Image.open(resource(os.path.join('button_icons', 'read_later.png')))
            ctk_read = customtkinter.CTkImage(dark_image=read_later)

            unfavorite = Image.open(resource(os.path.join('button_icons', 'unfavorite.png')))
            ctk_unfavorite = customtkinter.CTkImage(dark_image=unfavorite)
            favorite = Image.open(resource(os.path.join('button_icons', 'favorite.png')))
            ctk_favorite = customtkinter.CTkImage(dark_image=favorite)

            file_explorer = Image.open(resource(os.path.join('button_icons', 'file.png')))
            ctk_explorer = customtkinter.CTkImage(dark_image=file_explorer)

            # buttons
            self.book_link_button = customtkinter.CTkButton(self.book_window, text="Update Link", height=50,
                                                            image=ctk_update,
                                                            fg_color=light_pink, hover_color=dark_pink,
                                                            text_color=black,
                                                            command=lambda x=book, y=tag_json, z=authors_json:
                                                            self.link_update(x, y, z))
            self.book_name_button = customtkinter.CTkButton(self.book_window, text="Update Name", height=50,
                                                            image=ctk_update,
                                                            fg_color=light_pink, hover_color=dark_pink,
                                                            text_color=black,
                                                            command=lambda x=book, y=tag_json, z=authors_json:
                                                            self.name_update(x, y, z))
            book_author_button = customtkinter.CTkButton(self.book_window, text="Update Author", height=50,
                                                         image=ctk_update,
                                                         fg_color=light_pink, hover_color=dark_pink, text_color=black,
                                                         command=lambda x=book, y=tag_json, z=authors_json, a=authors:
                                                         self.author_update(x, y, z, a))

            self.open_in_file_explorer_button = customtkinter.CTkButton(self.book_window, text="File Explorer",
                                                                        image=ctk_explorer,
                                                                        height=50,
                                                                        command=lambda
                                                                            a=book.get_path(): open_file_location(
                                                                            a),
                                                                        fg_color=light_pink, hover_color=dark_pink,
                                                                        text_color=black)

            self.book_read_later_button = customtkinter.CTkButton(self.book_window, text="Read Later", height=50,
                                                                  image=ctk_unread,
                                                                  command=lambda a=ctk_unread, b=ctk_read,
                                                                                 x=book, y=tag_json, z=authors_json:
                                                                  self.read_book_callback(x, y, z, a, b),
                                                                  fg_color=light_pink, hover_color=dark_pink,
                                                                  text_color=black)
            self.book_favorite_button = customtkinter.CTkButton(self.book_window, text="Favorite", height=50,
                                                                command=lambda a=ctk_unfavorite, b=ctk_favorite,
                                                                               x=book, y=tag_json, z=authors_json:
                                                                self.favorite_book_callback(x, y, z, a, b),
                                                                image=ctk_unfavorite,
                                                                fg_color=light_pink, hover_color=dark_pink,
                                                                text_color=black)

            # conditionals to set the favorite/readlater icons
            if book.read_later:
                self.book_read_later_button.configure(image=ctk_read)
            else:
                self.book_read_later_button.configure(image=ctk_unread)

            if book.favorite:
                self.book_favorite_button.configure(image=ctk_favorite)
            else:
                self.book_favorite_button.configure(image=ctk_unfavorite)

            # entry
            w = 800
            self.book_link_entry = customtkinter.CTkEntry(
                self.book_window, placeholder_text="LINK", width=w)
            self.book_name_entry = customtkinter.CTkEntry(
                self.book_window, placeholder_text="NAME", width=w)
            self.book_author_cbox = customtkinter.CTkComboBox(
                self.book_window, width=w, values=authors)
            self.book_link_entry.insert(0, book.get_link())
            self.book_name_entry.insert(0, book.get_name())
            self.book_author_cbox.set(book.get_author())

            # scrollable frame
            tag_scroller = customtkinter.CTkScrollableFrame(
                self.book_window, label_text="Tags", label_text_color=light_pink, width=500, height=410)
            page_scroller = customtkinter.CTkScrollableFrame(
                self.book_window, width=1850, height=420)

            # get pages
            page_thumbs = book.get_pages(True)

            tag_checks: list[customtkinter.CTkCheckBox] = []

            r = 0
            c = 0

            # grab from the JSON and append to array
            tags: list[str] = []
            with open(tag_json, 'r') as f:
                load_tags = json.load(f)

            # load the tag names from the JSON into an array
            for i in load_tags['tags']:
                tags.append(i['name'])

            for i in tags:
                check_box = customtkinter.CTkCheckBox(tag_scroller, text=i,
                                                      checkbox_height=35, checkbox_width=35, font=("Roboto", 14),
                                                      hover_color=light_pink, fg_color=dark_pink, text_color=light_pink,
                                                      command=lambda
                                                          x=book,
                                                          y=tag_json,
                                                          a=authors_json,
                                                          z=i:
                                                      self.append_new_tags(x, y, a, z))
                check_box.grid(row=r, column=c, padx=10, pady=5, sticky='w')
                if c == 2:
                    c = 0
                    r += 1
                else:
                    c += 1
                tag_checks.append(check_box)

            for i in book.get_tags():
                for j in tag_checks:
                    if str(i).lower() == str(j.cget("text")).lower():
                        j.select()

            r = 0
            c = 0

            for i in page_thumbs:
                label = customtkinter.CTkLabel(page_scroller, image=i, text="")
                label.grid(row=r, column=c, padx=5, pady=5)

                if c == 5:
                    c = 0
                    r += 1
                else:
                    c += 1

            # update the page count label

            book_page_count_label.configure(text="Page Count: " + str(len(page_thumbs)))

            # place widgets
            pad = 20
            self.read_button.grid(row=1, column=0, rowspan=5)

            book_page_count_label.grid(row=0, column=0, padx=pad, pady=pad)
            book_link_label.grid(row=0, column=1, padx=pad, pady=pad)
            book_name_label.grid(row=2, column=1, padx=pad, pady=pad)
            book_author_label.grid(row=4, column=1, padx=pad, pady=pad)

            self.book_link_entry.grid(
                row=1, column=1, columnspan=2, padx=pad, pady=pad)
            self.book_name_entry.grid(
                row=3, column=1, columnspan=2, padx=pad, pady=pad)
            self.book_author_cbox.grid(
                row=5, column=1, columnspan=2, padx=pad, pady=pad)

            self.book_link_button.grid(
                row=0, column=2, padx=pad, pady=pad)
            self.book_name_button.grid(
                row=2, column=2, padx=pad, pady=pad)
            book_author_button.grid(
                row=4, column=2, padx=pad, pady=pad)
            self.book_read_later_button.grid(row=0, column=3, padx=pad, pady=pad)
            self.book_favorite_button.grid(row=0, column=4, padx=pad, pady=pad)
            self.open_in_file_explorer_button.grid(row=0, column=5, padx=pad, pady=pad)

            # align checkbox columns
            tag_scroller.grid_columnconfigure(0, weight=1)
            tag_scroller.grid_columnconfigure(1, weight=1)
            tag_scroller.grid_columnconfigure(1, weight=1)
            tag_scroller.grid(row=1, column=3, columnspan=3, rowspan=5, padx=pad, pady=pad)
            page_scroller.grid(
                row=6, column=0, columnspan=6, padx=pad, pady=pad)

            self.book_window.protocol(
                'WM_DELETE_WINDOW', self.close_book_description)

            # focus the window
            self.after(1, self.focus_description)

        else:
            self.book_window.focus()  # if window exists focus it

    def next_tab(self, tag_json: str, authors_json):
        # print(str(self.current_tab) + " < " + str(math.ceil((self.book_count - 1) / 10)))
        if self.current_tab < math.ceil(self.book_count / self.books_per_page) - 1:
            self.current_tab += 1
            self.load_tab(tag_json, authors_json)

    def prev_tab(self, tag_json: str, authors_json):
        if self.current_tab != 0:
            self.current_tab -= 1
            self.load_tab(tag_json, authors_json)

    def load_tab(self, tag_json: str, authors_json: str):
        # if the library already has books, destroy them
        for i in self.book_buttons:
            i.destroy()
        self.book_buttons.clear()

        books_json = {}

        # load the JSON
        if path.isfile(self.library_json) is False:
            print("FILE NOT FOUND")
        else:
            with open(self.library_json) as f:
                books_json = json.load(f)

        # get the books
        books: list[Book] = []
        loopy = 0
        index_to_start_at = self.current_tab * self.books_per_page
        tab_count = math.ceil(self.book_count / self.books_per_page)

        if self.book_count != 0:
            # put the current books into the array
            if self.current_tab != self.get_tab_count() - 1:
                while loopy < self.books_per_page:
                    books.append(
                        Book(books_json['book'][index_to_start_at]['path'],
                             books_json['book'][index_to_start_at]['name'],
                             books_json['book'][index_to_start_at]['author'],
                             books_json['book'][index_to_start_at]['link'],
                             books_json['book'][index_to_start_at]['read_later'],
                             books_json['book'][index_to_start_at]['favorite'],
                             books_json['book'][index_to_start_at]['tagged']))
                    loopy += 1
                    index_to_start_at += 1
            else:
                while loopy < self.excess_books:
                    books.append(
                        Book(books_json['book'][index_to_start_at]['path'],
                             books_json['book'][index_to_start_at]['name'],
                             books_json['book'][index_to_start_at]['author'],
                             books_json['book'][index_to_start_at]['link'],
                             books_json['book'][index_to_start_at]['read_later'],
                             books_json['book'][index_to_start_at]['favorite'],
                             books_json['book'][index_to_start_at]['tagged']))
                    loopy += 1
                    index_to_start_at += 1

        # create the buttons
        counter = 0
        if self.book_count == 0:
            pass

        elif tab_count != self.current_tab + 1:
            # create the book objects
            while counter < self.books_per_page:
                button = customtkinter.CTkButton(self, compound="top",
                                                 image=books[counter].get_cover(
                                                 ),
                                                 command=lambda
                                                     x=books[counter], y=tag_json,
                                                     z=authors_json: self.open_book_description(
                                                     x, y, z),
                                                 fg_color="transparent", hover_color=dark_pink,
                                                 text=shorten_string(
                                                     books[counter].get_name()),
                                                 font=("Roboto", 18))

                self.book_buttons.append(button)
                index_to_start_at += 1
                counter += 1
        else:
            # create the book objects
            while counter < self.excess_books:
                button = customtkinter.CTkButton(self, compound="top",
                                                 image=books[counter].get_cover(
                                                 ),
                                                 command=lambda
                                                     x=books[counter], y=tag_json,
                                                     z=authors_json: self.open_book_description(
                                                     x, y, z),
                                                 fg_color="transparent", hover_color=dark_pink,
                                                 text=shorten_string(
                                                     books[counter].get_name()),
                                                 font=("Roboto", 18))

                self.book_buttons.append(button)
                index_to_start_at += 1
                counter += 1

        self.print_page()

    def print_page(self):
        r = 2
        c = 0
        # print(str(len(self.book_buttons)))
        for i in self.book_buttons:
            i.grid(row=r, column=c)
            if c == 5:
                c = 0
                r += 1
            else:
                c += 1

    def initialize_self(self):
        start_time = time.time()

        count = 0
        if path.isfile(self.library_json) is False:
            print("FILE NOT FOUND")
        else:
            with open(self.library_json) as f:
                books_json = json.load(f)
                # grab the metadata
                for i in books_json['book']:
                    count += 1

        self.book_count = count
        self.excess_books = self.books_per_page - (math.ceil(self.book_count / self.books_per_page)
                                                   * self.books_per_page - self.book_count)
        # start_time = time.time()
        # print("--- %s seconds ---" % (time.time() - start_time))

    def focus_filter_window(self):
        assert self.filter_window
        self.filter_window.focus()

    def focus_filter_library(self):
        assert self.filter_library
        self.filter_library.focus()

    def first_filtered_tab(self, tag_json: str, authors_json, filtered_result):
        self.current_filter_tab = 0
        self.load_filtered(tag_json, authors_json, filtered_result)
        self.filter_tab_tracker.configure(text=str(self.current_filter_tab + 1) + " / " +
                                               str(math.ceil(len(filtered_result) / self.books_per_page)))
        self.filter_tab_tracker.grid(row=0, column=2, padx=10, pady=10)

    def last_filtered_tab(self, tag_json: str, authors_json, filtered_result):
        self.current_filter_tab = math.ceil(len(filtered_result) / self.books_per_page) - 1
        self.load_filtered(tag_json, authors_json, filtered_result)
        self.filter_tab_tracker.configure(text=str(self.current_filter_tab + 1) + " / " +
                                               str(math.ceil(len(filtered_result) / self.books_per_page)))
        self.filter_tab_tracker.grid(row=0, column=2, padx=10, pady=10)

    def next_filtered_tab(self, tag_json: str, authors_json, filtered_result):
        # print(str(self.current_tab) + " < " + str(math.ceil((self.book_count - 1) / 10)))
        if self.current_filter_tab < math.ceil(len(filtered_result) / self.books_per_page) - 1:
            self.current_filter_tab += 1
            self.load_filtered(tag_json, authors_json, filtered_result)
            self.filter_tab_tracker.configure(text=str(self.current_filter_tab + 1) + " / " +
                                                   str(math.ceil(len(filtered_result) / self.books_per_page)))
            self.filter_tab_tracker.grid(row=0, column=2, padx=10, pady=10)

    def prev_filtered_tab(self, tag_json: str, authors_json, filtered_result):
        if self.current_filter_tab != 0:
            self.current_filter_tab -= 1
            self.load_filtered(tag_json, authors_json, filtered_result)
            self.filter_tab_tracker.configure(text=str(self.current_filter_tab + 1) + " / " +
                                                   str(math.ceil(len(filtered_result) / self.books_per_page)))
            self.filter_tab_tracker.grid(row=0, column=2, padx=10, pady=10)

    def print_filtered(self, tag_json: str, authors_json: str, books_to_print):

        # rid of buttons in memory
        for i in self.filter_buttons:
            i.destroy()
        self.filter_buttons.clear()

        # create book button objects
        count = 0
        # make the buttons
        for i in books_to_print:
            button = customtkinter.CTkButton(self.read_frame,
                                             fg_color="transparent", hover_color=dark_pink, compound="top",
                                             image=books_to_print[count].get_cover(),
                                             text=shorten_string(books_to_print[count].get_name()),
                                             font=("Roboto", 18),
                                             command=lambda
                                                 x=books_to_print[count], y=tag_json,
                                                 z=authors_json: self.open_book_description(x, y, z))
            count += 1
            self.filter_buttons.append(button)
        # print the buttons
        r = 2
        c = 0
        # print(str(len(self.book_buttons)))
        for i in self.filter_buttons:
            i.grid(row=r, column=c)
            if c == 5:
                c = 0
                r += 1
            else:
                c += 1

    def load_filtered(self, tag_json: str, authors_json: str, filtered_result):
        books_to_print = []
        index_to_start_at = self.current_filter_tab * self.books_per_page
        counter = 0
        if self.book_count == 0:
            pass
        elif self.filter_tab_count != self.current_filter_tab + 1:
            # create the books
            while counter < self.books_per_page:
                # create book objects
                book = Book(filtered_result[index_to_start_at].get('path'),
                            filtered_result[index_to_start_at].get('name'),
                            filtered_result[index_to_start_at].get('author'),
                            filtered_result[index_to_start_at].get('link'),
                            filtered_result[index_to_start_at].get('read_later'),
                            filtered_result[index_to_start_at].get('favorite'),
                            filtered_result[index_to_start_at].get('tagged'))
                books_to_print.append(book)
                counter += 1
                index_to_start_at += 1
        else:
            # calculate how many excess books there are
            excess_books = self.books_per_page - (math.ceil(len(filtered_result) / self.books_per_page)
                                                  * self.books_per_page - len(filtered_result))
            while counter < excess_books:
                # create book objects
                book = Book(filtered_result[index_to_start_at].get('path'),
                            filtered_result[index_to_start_at].get('name'),
                            filtered_result[index_to_start_at].get('author'),
                            filtered_result[index_to_start_at].get('link'),
                            filtered_result[index_to_start_at].get('read_later'),
                            filtered_result[index_to_start_at].get('favorite'),
                            filtered_result[index_to_start_at].get('tagged'))
                books_to_print.append(book)
                counter += 1
                index_to_start_at += 1

        self.print_filtered(tag_json, authors_json, books_to_print)

    def build_filter_window(self, tag_json: str, authors_json: str, filtered_result, filter_by):
        if self.filter_library is None or not self.filter_library.winfo_exists():

            # make sure books exist
            if len(filtered_result) != 0:
                # make the new window
                self.filter_library = customtkinter.CTkToplevel()
                self.filter_library.geometry('1750x1050+550+220')
                self.filter_buttons = []

                self.filter_library.title("Books")

                if filter_by == "tag":
                    self.filter_library.title("Filter by Tag")
                elif filter_by == "search":
                    self.filter_library.title("Search")
                elif filter_by == "author":
                    self.filter_library.title("Filter by Author")
                elif filter_by == "read_later":
                    self.filter_library.title("Read Later")
                elif filter_by == "favorite":
                    self.filter_library.title("Favorites")

                # build the UI
                self.read_frame = customtkinter.CTkScrollableFrame(self.filter_library, width=1700, height=950)
                self.read_frame.grid_columnconfigure(0, weight=1)
                self.read_frame.grid_columnconfigure(1, weight=1)
                self.read_frame.grid_columnconfigure(2, weight=1)
                self.read_frame.grid_columnconfigure(3, weight=1)
                self.read_frame.grid_columnconfigure(4, weight=1)
                self.read_frame.grid_columnconfigure(5, weight=1)
                self.read_frame.grid_rowconfigure(0, weight=1)
                self.read_frame.grid_rowconfigure(1, weight=1)

                next = Image.open(resource(os.path.join('button_icons', 'next_icon.png')))
                ctk_next = customtkinter.CTkImage(dark_image=next)

                prev = Image.open(resource(os.path.join('button_icons', 'prev_icon.png')))
                ctk_prev = customtkinter.CTkImage(dark_image=prev)

                jump_first = Image.open(resource(os.path.join('button_icons', 'jump_first_icon.png')))
                ctk_jump_first = customtkinter.CTkImage(dark_image=jump_first)

                jump_last = Image.open(resource(os.path.join('button_icons', 'jump_last_icon.png')))
                ctk_jump_last = customtkinter.CTkImage(dark_image=jump_last)

                w = 520
                button_frame = customtkinter.CTkFrame(self.filter_library)
                first_button = customtkinter.CTkButton(button_frame, text="First Tab",
                                                       image=ctk_jump_first,
                                                       fg_color=light_pink,
                                                       text_color=black,
                                                       hover_color=dark_pink,
                                                       command=lambda x=tag_json, y=authors_json, z=filtered_result:
                                                       self.first_filtered_tab(x, y, z))
                prev_button = customtkinter.CTkButton(button_frame, text="Previous Tab",
                                                      image=ctk_prev,
                                                      width=w,
                                                      fg_color=light_pink,
                                                      text_color=black,
                                                      hover_color=dark_pink,
                                                      command=lambda x=tag_json, y=authors_json, z=filtered_result:
                                                      self.prev_filtered_tab(x, y, z))
                next_button = customtkinter.CTkButton(button_frame, text="Next Tab",
                                                      compound='right',
                                                      image=ctk_next,
                                                      width=w,
                                                      fg_color=light_pink,
                                                      text_color=black,
                                                      hover_color=dark_pink,
                                                      command=lambda x=tag_json, y=authors_json, z=filtered_result:
                                                      self.next_filtered_tab(x, y, z))
                last_button = customtkinter.CTkButton(button_frame, text="Last Tab",
                                                      compound='right',
                                                      image=ctk_jump_last,
                                                      fg_color=light_pink,
                                                      text_color=black,
                                                      hover_color=dark_pink,
                                                      command=lambda x=tag_json, y=authors_json, z=filtered_result:
                                                      self.last_filtered_tab(x, y, z))

                pad = 10
                self.read_frame.grid(row=1, columnspan=2, padx=pad, pady=pad)
                button_frame.grid(row=2, columnspan=2)

                self.current_filter_tab = 0
                self.filter_tab_count = math.ceil(len(filtered_result) / self.books_per_page)

                self.filter_tab_tracker = customtkinter.CTkLabel(button_frame,
                                                                 text=("1 / " + str(self.filter_tab_count)),
                                                                 font=("Roboto", 20))

                first_button.grid(row=0, column=0, padx=pad, pady=pad)
                prev_button.grid(row=0, column=1, padx=pad, pady=pad)
                self.filter_tab_tracker.grid(row=0, column=2, padx=pad, pady=pad)
                next_button.grid(row=0, column=3, padx=pad, pady=pad)
                last_button.grid(row=0, column=4, padx=pad, pady=pad)

                # now load the first 12 books
                self.load_filtered(tag_json, authors_json, filtered_result)

                self.filter_library.after(100, self.focus_filter_library)

        else:
            self.filter_library.focus()

    def get_json(self, tag_json, author_json, find, filter_by: str):
        # this destroy is to remove the contents of the dict
        if self.filter_window is not None:
            self.filter_window.destroy()

        if filter_by == "tag":

            filtered_json = []
            # load the JSON
            if path.isfile(self.library_json) is False:
                print("FILE NOT FOUND")
            else:
                with open(self.library_json) as f:
                    books_json = json.load(f)

            tags_needed = len(find)

            # only search if tags are checked
            if len(find) != 0:

                for x in books_json['book']:
                    # reset the count
                    tags_that_match = 0
                    for y in find:
                        for z in x["tagged"]:
                            # if the tags match, add one to tags that match
                            if y == z:
                                tags_that_match += 1
                                # if the amount of tags that match is equal to the amount needed, add it filteredjson
                                if tags_that_match == tags_needed:
                                    filtered_json.append(x)

                # remove dupes
                final_filtered_json = []
                for i in range(len(filtered_json)):
                    if filtered_json[i] not in filtered_json[i + 1:]:
                        final_filtered_json.append(filtered_json[i])

                self.build_filter_window(tag_json, author_json, final_filtered_json, filter_by)

        elif filter_by == "search":
            filtered_json = []
            # load the JSON
            if path.isfile(self.library_json) is False:
                print("FILE NOT FOUND")
            else:
                with open(self.library_json) as f:
                    books_json = json.load(f)

            for x in books_json['book']:
                # if name matches
                if find.lower() in x['name'].lower():
                    # make book only if name matches
                    filtered_json.append(x)

            self.build_filter_window(tag_json, author_json, filtered_json, filter_by)

        elif filter_by == "author":
            filtered_json = []
            # load the JSON
            if path.isfile(self.library_json) is False:
                print("FILE NOT FOUND")
            else:
                with open(self.library_json) as f:
                    books_json = json.load(f)

            for x in books_json['book']:
                if find == x["author"]:
                    filtered_json.append(x)

            self.build_filter_window(tag_json, author_json, filtered_json, filter_by)

        elif filter_by == "read_later":
            filtered_json = []
            # load the JSON
            if path.isfile(self.library_json) is False:
                print("FILE NOT FOUND")
            else:
                with open(self.library_json) as f:
                    books_json = json.load(f)

            for x in books_json['book']:
                if x["read_later"]:
                    filtered_json.append(x)

            self.build_filter_window(tag_json, author_json, filtered_json, filter_by)
        elif filter_by == "favorite":
            filtered_json = []
            # load the JSON
            if path.isfile(self.library_json) is False:
                print("FILE NOT FOUND")
            else:
                with open(self.library_json) as f:
                    books_json = json.load(f)

            for x in books_json['book']:
                if x["favorite"]:
                    filtered_json.append(x)

            self.build_filter_window(tag_json, author_json, filtered_json, filter_by)

    def get_filter(self, tag_json, author_json, filter_by: str):
        if filter_by == "tag":
            if self.filter_window is None or not self.filter_window.winfo_exists():
                self.filter_window = customtkinter.CTkToplevel()
                self.filter_window.geometry("550+225")
                self.filter_window.title("Filter by Tags")

                tags = []
                tagged = []

                r = 0
                c = 0
                num_loops = 0
                scrollableframe = customtkinter.CTkScrollableFrame(self.filter_window, width=800, height=500)
                filter_button = customtkinter.CTkButton(self.filter_window, text="Filter",
                                                        fg_color=light_pink, hover_color=dark_pink, text_color=black,
                                                        font=("Roboto", 16),
                                                        command=lambda x=tag_json, y=author_json, a=tagged, b=filter_by:
                                                        self.get_json(x, y, a, b))

                filter_button.grid(padx=10, pady=10, sticky="ew")
                scrollableframe.grid(padx=10, pady=10)

                # load the JSON
                with open(tag_json, 'r') as f:
                    load_tags = json.load(f)

                # load the tag names from the JSON into an array
                for i in load_tags['tags']:
                    tags.append(i['name'])

                for i in tags:

                    if num_loops != 0:
                        if tags[num_loops - 1][0] < i[0]:
                            c = 0
                            r += 1
                            label = customtkinter.CTkLabel(scrollableframe, text=" " + i[0].upper() + " : ",
                                                           font=("Roboto", 35),
                                                           text_color=light_pink)
                            label.grid(row=r, column=c, padx=0, pady=10)
                            c += 1
                        else:
                            c += 1
                    else:
                        label = customtkinter.CTkLabel(scrollableframe, text=i[0].upper() + " : ", font=("Roboto", 35),
                                                       text_color=light_pink)
                        label.grid(row=0, column=0, padx=0, pady=10)
                        c += 1

                    num_loops += 1

                    checkbox = customtkinter.CTkCheckBox(scrollableframe, text=i,
                                                         checkbox_height=35, checkbox_width=35,
                                                         font=("Roboto", 16),
                                                         command=lambda
                                                             y=tagged, z=i: checking(y, z),
                                                         hover_color=light_pink, fg_color=dark_pink,
                                                         text_color=light_pink)
                    checkbox.grid(row=r, column=c, pady=10, padx=10, sticky='w')

                    if c == 4:
                        c = 0
                        r += 1

                self.filter_window.after(100, self.focus_filter_window)

            else:
                self.filter_window.focus()
        elif filter_by == "search":
            if self.filter_window is None or not self.filter_window.winfo_exists():
                self.filter_window = customtkinter.CTkToplevel()
                self.filter_window.geometry("550+225")
                self.filter_window.title("Search by name")
                authors = []
                with open(author_json, 'r') as f:
                    load_authors = json.load(f)

                # load the tag names from the JSON into an array
                for i in load_authors['authors']:
                    authors.append(i['name'])

                search = customtkinter.CTkEntry(self.filter_window, width=500)
                search.grid(padx=10, pady=10)

                # button to submit
                button = customtkinter.CTkButton(self.filter_window, text="Filter",
                                                 fg_color=light_pink,
                                                 text_color=black,
                                                 hover_color=dark_pink,
                                                 command=lambda x=tag_json, y=author_json, a=search, b=filter_by:
                                                 self.get_json(x, y, a.get(), b))
                button.grid(padx=10, pady=10)

                self.filter_window.after(100, self.focus_filter_window)
                search.after(100, search.focus)

            else:
                self.filter_window.focus()
        elif filter_by == "author":
            if self.filter_window is None or not self.filter_window.winfo_exists():
                self.filter_window = customtkinter.CTkToplevel()
                self.filter_window.geometry("550+225")
                self.filter_window.title("Filter by Author")
                # authors = []
                # with open(author_json, 'r') as f:
                #     load_authors = json.load(f)
                #
                # # load the tag names from the JSON into an array
                # for i in load_authors['authors']:
                #     authors.append(i['name'])
                #
                # author_cbox = customtkinter.CTkComboBox(self.filter_window, values=authors, width=300)
                # author_cbox.grid(padx=10, pady=10)
                # if len(authors) != 0:
                #     CTkScrollableDropdown(author_cbox, values=authors, justify="left",
                #                           button_color="transparent",
                #                           resize=False, autocomplete=True,
                #                           frame_border_color=light_pink,
                #                           scrollbar_button_hover_color=light_pink)
                # # button to submit
                # button = customtkinter.CTkButton(self.filter_window, text="Filter",
                #                                  fg_color=light_pink,
                #                                  text_color=black,
                #                                  hover_color=dark_pink,
                #                                  command=lambda x=tag_json, y=author_json, a=author_cbox, b=filter_by:
                #                                  self.get_json(x, y, a.get(), b))
                # button.grid(padx=10, pady=10)

                # self.filter_window.after(100, self.focus_filter_window)
                # author_cbox.after(100, author_cbox.focus)

                authors = []

                with open(author_json, 'r') as f:
                    load_authors = json.load(f)

                # load the tag names from the JSON into an array
                for i in load_authors['authors']:
                    authors.append(i['name'])

                def check_input(event):
                    value = event.widget.get()

                    if value == '':
                        self.filter_window.author_cbox['values'] = authors
                    else:
                        data = []
                        for item in authors:
                            if value.lower() in item.lower():
                                data.append(item)

                        self.filter_window.author_cbox['values'] = data

                self.filter_window.author_cbox = ttk.Combobox(self.filter_window)
                self.filter_window.author_cbox['values'] = authors
                self.filter_window.author_cbox.bind('<KeyRelease>', check_input)
                self.filter_window.author_cbox.grid(row=2, column=0, padx=60, pady=30)

                # button to submit
                button = customtkinter.CTkButton(self.filter_window, text="Filter",
                                                 fg_color=light_pink,
                                                 text_color=black,
                                                 hover_color=dark_pink,
                                                 command=lambda x=tag_json, y=author_json,
                                                                a=self.filter_window.author_cbox, b=filter_by:
                                                 self.get_json(x, y, a.get(), b))
                button.grid(padx=10, pady=10)

                self.filter_window.after(100, self.focus_filter_window)
                self.filter_window.author_cbox.after(100, self.filter_window.author_cbox.focus)

            else:
                self.filter_window.focus()

    def get_tab_count(self):
        # take the book count
        # divide by books per page
        # round up
        return math.ceil(self.book_count / self.books_per_page)

    def __init__(self, library_json: str, tag_json: str, authors_json: str, master: customtkinter.CTk, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)

        self.sort_by_tag_window = None
        self.sort_by_author_window = None
        self.search_by_name_dialogue = None

        self.filter_library = None
        self.filter_window = None

        # create frames
        button_frame = customtkinter.CTkFrame(self)
        read_favorite_frame = customtkinter.CTkFrame(self)

        # create icons

        filter = Image.open(resource(os.path.join('button_icons', 'filter_icon.png')))
        ctk_filter = customtkinter.CTkImage(dark_image=filter)

        search = Image.open(resource(os.path.join('button_icons', 'search_icon.png')))
        ctk_search = customtkinter.CTkImage(dark_image=search)

        read_later = Image.open(resource(os.path.join('button_icons', 'read_later.png')))
        ctk_read = customtkinter.CTkImage(dark_image=read_later)
        favorite = Image.open(resource(os.path.join('button_icons', 'favorite.png')))
        ctk_favorite = customtkinter.CTkImage(dark_image=favorite)

        sort_by_tag_button = customtkinter.CTkButton(button_frame, text="Filter by Tag", width=520,
                                                     image=ctk_filter,
                                                     compound="left",
                                                     fg_color=light_pink,
                                                     text_color=black,
                                                     hover_color=dark_pink,
                                                     command=lambda
                                                         y=tag_json, z=authors_json, a="tag": self.get_filter(y, z, a))

        search_button = customtkinter.CTkButton(button_frame, text="Search by Name", width=520,
                                                image=ctk_search,
                                                compound="left",
                                                fg_color=light_pink,
                                                text_color=black,
                                                hover_color=dark_pink,
                                                command=lambda
                                                    y=tag_json, z=authors_json, a="search": self.get_filter(y, z, a))

        sort_by_author_button = customtkinter.CTkButton(button_frame, text="Filter by Author", width=520,
                                                        image=ctk_filter,
                                                        compound="left",
                                                        fg_color=light_pink,
                                                        text_color=black,
                                                        hover_color=dark_pink,
                                                        command=lambda
                                                            y=tag_json, z=authors_json, a="author": self.get_filter(y,
                                                                                                                    z,
                                                                                                                    a))

        show_read_later = customtkinter.CTkButton(read_favorite_frame, text="Read Later", width=785,
                                                  command=lambda x=tag_json, y=authors_json, a="", z="read_later":
                                                  self.get_json(x, y, a, z),
                                                  image=ctk_read,
                                                  compound="left",
                                                  fg_color=light_pink,
                                                  text_color=black,
                                                  hover_color=dark_pink)
        show_favorite = customtkinter.CTkButton(read_favorite_frame, text="Favorites", width=785,
                                                command=lambda x=tag_json, y=authors_json, a="", z="favorite":
                                                self.get_json(x, y, a, z),
                                                image=ctk_favorite,
                                                compound="left",
                                                fg_color=light_pink,
                                                text_color=black,
                                                hover_color=dark_pink)

        sort_by_tag_button.grid(row=1, column=0, sticky="ew", padx=10)
        search_button.grid(row=1, column=1, sticky="ew", padx=10)
        sort_by_author_button.grid(row=1, column=2, sticky="ew", padx=10)
        show_read_later.grid(row=0, column=0, sticky="ew", padx=10)
        show_favorite.grid(row=0, column=2, sticky="ew", padx=10)

        read_favorite_frame.grid(row=0, column=0, columnspan=6, padx=5, pady=5)
        button_frame.grid(row=1, column=0, columnspan=6, padx=5, pady=5)

        # books_per_page should be divisible by 12
        self.books_per_page = 12
        self.book_window = None
        self.book_buttons: list[customtkinter.CTkButton] = []
        self.current_tab = 0
        self.library_json = library_json
        self.page: customtkinter.CTkLabel | None = None
        self.pagenum_label: customtkinter.CTkLabel | None = None
        self.reader_window: customtkinter.CTkToplevel | None = None
        self.book_window: customtkinter.CTkToplevel | None = None
        self.initialize_self()

        self.load_tab(tag_json, authors_json)


class TabNavigator(customtkinter.CTkFrame):

    def nav_first_tab(self, book_frame: BookFrame, tag_json, authors_json):
        book_frame.current_tab = 0
        book_frame.load_tab(tag_json, authors_json)
        if book_frame.current_tab + 1 < 10:
            self.tab_tracker.configure(
                text=("0" + str(book_frame.current_tab + 1) + " / " + str(book_frame.get_tab_count())))
        else:
            self.tab_tracker.configure(
                text=(str(book_frame.current_tab + 1) + " / " + str(book_frame.get_tab_count())))

    def nav_last_tab(self, book_frame: BookFrame, tag_json, authors_json):
        book_frame.current_tab = book_frame.get_tab_count() - 1
        book_frame.load_tab(tag_json, authors_json)
        if book_frame.current_tab + 1 < 10:
            self.tab_tracker.configure(
                text=("0" + str(book_frame.current_tab + 1) + " / " + str(book_frame.get_tab_count())))
        else:
            self.tab_tracker.configure(
                text=(str(book_frame.current_tab + 1) + " / " + str(book_frame.get_tab_count())))

    def nav_next_tab(self, book_frame: BookFrame, tag_json, authors_json):
        book_frame.next_tab(tag_json, authors_json)
        if book_frame.current_tab + 1 < 10:
            self.tab_tracker.configure(
                text=("0" + str(book_frame.current_tab + 1) + " / " + str(book_frame.get_tab_count())))
        else:
            self.tab_tracker.configure(
                text=(str(book_frame.current_tab + 1) + " / " + str(book_frame.get_tab_count())))

    def nav_prev_tab(self, book_frame: BookFrame, tag_json, authors_json):
        book_frame.prev_tab(tag_json, authors_json)
        if book_frame.current_tab + 1 < 10:
            self.tab_tracker.configure(
                text=("0" + str(book_frame.current_tab + 1) + " / " + str(book_frame.get_tab_count())))
        else:
            self.tab_tracker.configure(
                text=(str(book_frame.current_tab + 1) + " / " + str(book_frame.get_tab_count())))

    def __init__(self, bookframe: BookFrame, tag_json: str, authors_json: str, master: customtkinter.CTk, **kwargs):
        super().__init__(master, **kwargs)

        next = Image.open(resource(os.path.join('button_icons', 'next_icon.png')))
        ctk_next = customtkinter.CTkImage(dark_image=next)

        prev = Image.open(resource(os.path.join('button_icons', 'prev_icon.png')))
        ctk_prev = customtkinter.CTkImage(dark_image=prev)

        jump_first = Image.open(resource(os.path.join('button_icons', 'jump_first_icon.png')))
        ctk_jump_first = customtkinter.CTkImage(dark_image=jump_first)

        jump_last = Image.open(resource(os.path.join('button_icons', 'jump_last_icon.png')))
        ctk_jump_last = customtkinter.CTkImage(dark_image=jump_last)

        self.tab_tracker = customtkinter.CTkLabel(self,
                                                  text=("01 / " + str(bookframe.get_tab_count())),
                                                  font=("Roboto", 20))

        first_tab = customtkinter.CTkButton(self, text="First Tab",
                                            image=ctk_jump_first,
                                            command=lambda b=bookframe, x=tag_json, z=authors_json:
                                            self.nav_first_tab(b, x, z),
                                            fg_color=light_pink,
                                            text_color=black,
                                            hover_color=dark_pink)

        last_tab = customtkinter.CTkButton(self, text="Last Tab",
                                           compound="right",
                                           image=ctk_jump_last,
                                           command=lambda b=bookframe, x=tag_json, z=authors_json:
                                           self.nav_last_tab(b, x, z),
                                           fg_color=light_pink,
                                           text_color=black,
                                           hover_color=dark_pink)

        next_tab = customtkinter.CTkButton(self, text="Next Tab",
                                           image=ctk_next,
                                           compound='right',
                                           command=lambda b=bookframe, x=tag_json, z=authors_json:
                                           self.nav_next_tab(b, x, z),
                                           width=520,
                                           fg_color=light_pink,
                                           text_color=black,
                                           hover_color=dark_pink)
        prev_tab = customtkinter.CTkButton(self, text="Previous Tab",
                                           image=ctk_prev,
                                           compound='left',
                                           command=lambda b=bookframe, x=tag_json, z=authors_json:
                                           self.nav_prev_tab(b, x, z),
                                           width=520,
                                           fg_color=light_pink,
                                           text_color=black,
                                           hover_color=dark_pink)

        first_tab.grid(row=0, column=0, padx=10, pady=10)
        prev_tab.grid(row=0, column=1, padx=10, pady=10)
        self.tab_tracker.grid(row=0, column=2)
        next_tab.grid(row=0, column=3, padx=10, pady=10)
        last_tab.grid(row=0, column=4, padx=10, pady=10)

import gc
import json
import math
import os
import time
from os import path
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
                                                       hover_color=dark_pink, font=(
                    "Roboto", 16),
                                                       image=book.get_full_cover(),
                                                       command=lambda x=book: self.open_reader(
                                                           x),
                                                       text=indent_string(book.get_name()))

            # labels
            book_link_label = customtkinter.CTkLabel(self.book_window, text="Link", font=("Roboto", 20),
                                                     text_color=light_pink)
            book_name_label = customtkinter.CTkLabel(self.book_window, text="Name", font=("Roboto", 20),
                                                     text_color=light_pink)
            book_author_label = customtkinter.CTkLabel(self.book_window, text="Author", font=("Roboto", 20),
                                                       text_color=light_pink)

            update = Image.open(resource(os.path.join('button_icons', 'update_icon.png')))
            ctk_update = customtkinter.CTkImage(dark_image=update)

            # buttons
            self.book_link_button = customtkinter.CTkButton(self.book_window, text="Update Link",
                                                            image=ctk_update,
                                                            fg_color=light_pink, hover_color=dark_pink,
                                                            text_color=black,
                                                            command=lambda x=book, y=tag_json, z=authors_json:
                                                            self.link_update(x, y, z))
            self.book_name_button = customtkinter.CTkButton(self.book_window, text="Update Name",
                                                            image=ctk_update,
                                                            fg_color=light_pink, hover_color=dark_pink,
                                                            text_color=black,
                                                            command=lambda x=book, y=tag_json, z=authors_json:
                                                            self.name_update(x, y, z))
            book_author_button = customtkinter.CTkButton(self.book_window, text="Update Author",
                                                         image=ctk_update,
                                                         fg_color=light_pink, hover_color=dark_pink, text_color=black,
                                                         command=lambda x=book, y=tag_json, z=authors_json, a=authors:
                                                         self.author_update(x, y, z, a))

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
                self.book_window, label_text="Tags", label_text_color=light_pink, width=500, height=500)
            page_scroller = customtkinter.CTkScrollableFrame(
                self.book_window, width=1850, height=440)

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

                if c == 9:
                    c = 0
                    r += 1
                else:
                    c += 1

            # place widgets
            pad = 20
            self.read_button.grid(row=0, column=0, rowspan=6)

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
                row=0, column=2, sticky="ns", padx=pad, pady=pad)
            self.book_name_button.grid(
                row=2, column=2, sticky="ns", padx=pad, pady=pad)
            book_author_button.grid(
                row=4, column=2, sticky="ns", padx=pad, pady=pad)
            # align checkbox columns
            tag_scroller.grid_columnconfigure(0, weight=1)
            tag_scroller.grid_columnconfigure(1, weight=1)
            tag_scroller.grid_columnconfigure(1, weight=1)
            tag_scroller.grid(row=0, column=3, rowspan=6, padx=pad, pady=pad)
            page_scroller.grid(
                row=6, column=0, columnspan=4, padx=pad, pady=pad)

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
                                                 text=indent_string(
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
                                                 text=indent_string(
                                                     books[counter].get_name()),
                                                 font=("Roboto", 18))

                self.book_buttons.append(button)
                index_to_start_at += 1
                counter += 1

        self.print_page()

    def print_page(self):
        r = 1
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

    def focus_sort_by_tag_call(self):
        assert self.sort_by_tag_window
        self.sort_by_tag_window.focus()

    def load_tab_tag(self, tag_cbox, tag_json, authors_json):
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

        # iterate through the json
        for i in books_json['book']:
            # load current book's tagged
            tags = i['tagged']
            if tag_cbox.get() in tags:
                # make book only if tag matches
                book = (Book(i['path'], i['name'],
                             i['author'], i['link'], i['tagged']))
                # make the button
                button = customtkinter.CTkButton(self, compound="top", image=book.get_cover(),
                                                 command=lambda
                                                     x=book, y=tag_json, z=authors_json:
                                                 self.open_book_description(x, y, z),
                                                 text=indent_string(book.get_name()),
                                                 fg_color="transparent", hover_color=dark_pink,
                                                 font=("Roboto", 18))
                # append to the buttons
                self.book_buttons.append(button)

        self.print_page()

    def sort_by_tag_call(self, tag_json: str, authors_json: str):
        if self.sort_by_tag_window is None or not self.sort_by_tag_window.winfo_exists():
            self.sort_by_tag_window = customtkinter.CTkToplevel()
            self.sort_by_tag_window.geometry('1275+720')
            self.sort_by_tag_window.title("Filter by tag")
            tags = []
            with open(tag_json, 'r') as f:
                load_tags = json.load(f)

            # load the tag names from the JSON into an array
            for i in load_tags['tags']:
                tags.append(i['name'])

            tag_cbox = customtkinter.CTkComboBox(self.sort_by_tag_window, values=tags, width=300)
            tag_cbox.grid(padx=10, pady=10)
            if len(tags) != 0:
                CTkScrollableDropdown(tag_cbox, values=tags, justify="left", button_color="transparent",
                                      resize=False, autocomplete=True,
                                      frame_border_color=light_pink, scrollbar_button_hover_color=light_pink)

            # button to submit
            tag_button = customtkinter.CTkButton(self.sort_by_tag_window, text="Filter",
                                                 fg_color=light_pink,
                                                 text_color=black,
                                                 hover_color=dark_pink,
                                                 command=lambda x=tag_cbox,
                                                                y=tag_json, z=authors_json: self.load_tab_tag(x, y, z))
            tag_button.grid(padx=10, pady=10)

            # focus it
            self.after(100, self.focus_sort_by_tag_call)

        else:
            self.sort_by_tag_window.focus()

    def focus_sort_by_author_call(self):
        assert self.sort_by_author_window
        self.sort_by_author_window.focus()

    def load_tab_author(self, author_cbox, tag_json: str, authors_json: str):
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

        # iterate through the json
        for i in books_json['book']:
            if author_cbox.get() == i['author']:
                # make book only if tag matches
                book = (Book(i['path'], i['name'],
                             i['author'], i['link'], i['tagged']))
                # make the button
                button = customtkinter.CTkButton(self, compound="top", image=book.get_cover(),
                                                 command=lambda
                                                     x=book, y=tag_json, z=authors_json:
                                                 self.open_book_description(x, y, z),
                                                 text=indent_string(book.get_name()),
                                                 fg_color="transparent", hover_color=dark_pink,
                                                 font=("Roboto", 18))
                # append to the buttons
                self.book_buttons.append(button)

        self.print_page()

    def sort_by_author_call(self, tag_json: str, authors_json: str):
        if self.sort_by_author_window is None or not self.sort_by_author_window.winfo_exists():
            self.sort_by_author_window = customtkinter.CTkToplevel()
            self.sort_by_author_window.geometry('1275+720')
            self.sort_by_author_window.title("Filter by author")
            authors = []
            with open(authors_json, 'r') as f:
                load_authors = json.load(f)

            # load the tag names from the JSON into an array
            for i in load_authors['authors']:
                authors.append(i['name'])

            author_cbox = customtkinter.CTkComboBox(self.sort_by_author_window, values=authors, width=300)
            author_cbox.grid(padx=10, pady=10)
            if len(authors) != 0:
                CTkScrollableDropdown(author_cbox, values=authors, justify="left", button_color="transparent",
                                      resize=False, autocomplete=True,
                                      frame_border_color=light_pink, scrollbar_button_hover_color=light_pink)

            # button to submit
            tag_button = customtkinter.CTkButton(self.sort_by_author_window, text="Filter",
                                                 fg_color=light_pink,
                                                 text_color=black,
                                                 hover_color=dark_pink,
                                                 command=lambda
                                                     x=author_cbox,
                                                     y=tag_json,
                                                     z=authors_json: self.load_tab_author(x, y, z))
            tag_button.grid(padx=10, pady=10)

            # focus it
            self.after(100, self.focus_sort_by_author_call)

        else:
            self.sort_by_author_window.focus()

    def search_by_name_call(self, tag_json: str, authors_json: str):
        if self.search_by_name_dialogue is None or not self.search_by_name_dialogue.winfo_exists():
            self.search_by_name_dialogue = customtkinter.CTkInputDialog(button_fg_color=light_pink,
                                                                        button_hover_color=dark_pink,
                                                                        button_text_color=black,
                                                                        text="Search by book name")
            self.search_by_name_dialogue.title("Search by book name")
            # get the string to search for
            search_for = self.search_by_name_dialogue.get_input()

            # make sure input is not empty, and they didn't press the close button
            if search_for != '' and search_for is not None:

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

                # iterate through the json
                for i in books_json['book']:
                    # if name matches
                    if search_for.lower() in i['name'].lower():
                        # make book only if name matches
                        book = (Book(i['path'], i['name'],
                                     i['author'], i['link'], i['tagged']))
                        # make the button
                        button = customtkinter.CTkButton(self, compound="top", image=book.get_cover(),
                                                         command=lambda
                                                             x=book, y=tag_json, z=authors_json:
                                                         self.open_book_description(x, y, z),
                                                         text=indent_string(book.get_name()),
                                                         fg_color="transparent", hover_color=dark_pink,
                                                         font=("Roboto", 18))
                        # append to the buttons
                        self.book_buttons.append(button)

                # print it
                self.print_page()

        else:
            self.search_by_name_dialogue.focus()

    def get_tab_count(self):
        # take the book count
        # divide by books per page
        # round up
        return math.ceil(self.book_count / self.books_per_page)

    def __init__(self, library_json: str, tag_json: str, authors_json: str, master: customtkinter.CTk, **kwargs):
        super().__init__(master, **kwargs)

        # keyboard.clear_all_hotkeys()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)

        self.sort_by_tag_window = None
        self.sort_by_author_window = None
        self.search_by_name_dialogue = None

        button_frame = customtkinter.CTkFrame(self)

        filter = Image.open(resource(os.path.join('button_icons', 'filter_icon.png')))
        ctk_filter = customtkinter.CTkImage(dark_image=filter)

        search = Image.open(resource(os.path.join('button_icons', 'search_icon.png')))
        ctk_search = customtkinter.CTkImage(dark_image=search)

        sort_by_tag_button = customtkinter.CTkButton(button_frame, text="Filter by tag", width=520,
                                                     image=ctk_filter,
                                                     compound="left",
                                                     fg_color=light_pink,
                                                     text_color=black,
                                                     hover_color=dark_pink,
                                                     command=lambda
                                                         y=tag_json, z=authors_json: self.sort_by_tag_call(y, z))

        search_button = customtkinter.CTkButton(button_frame, text="Search by name", width=520,
                                                image=ctk_search,
                                                compound="left",
                                                fg_color=light_pink,
                                                text_color=black,
                                                hover_color=dark_pink,
                                                command=lambda
                                                    y=tag_json, z=authors_json: self.search_by_name_call(y, z))

        sort_by_author_button = customtkinter.CTkButton(button_frame, text="Filter by author", width=520,
                                                        image=ctk_filter,
                                                        compound="left",
                                                        fg_color=light_pink,
                                                        text_color=black,
                                                        hover_color=dark_pink,
                                                        command=lambda
                                                            y=tag_json, z=authors_json: self.sort_by_author_call(y, z))

        sort_by_tag_button.grid(row=0, column=0, sticky="ew", padx=10)
        search_button.grid(row=0, column=1, sticky="ew", padx=10)
        sort_by_author_button.grid(row=0, column=2, sticky="ew", padx=10)

        button_frame.grid(row=0, column=0, columnspan=6, padx=10, pady=10)

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

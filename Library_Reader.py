import gc
import json
import math
import os
from os import path

import customtkinter
import keyboard

from Book import Book
from Database import black, dark_pink, light_pink
from Functions import *

# test line


class BookFrame(customtkinter.CTkScrollableFrame):

    def focus_reader(self):
        assert self.reader_window
        self.reader_window.focus()
    
    def close_reader(self):
        # clear windows hotkeys
        keyboard.clear_all_hotkeys()
        if self.reader_window:
            # yeet the reader window
            self.reader_window.destroy()
            self.reader_window = None
        if self.book_window:
            # lift description window back up
            self.book_window.attributes('-topmost', 1)

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
            self.reader_window.attributes('-topmost', 3)

            # make windows hoykeys
            keyboard.add_hotkey('a', self.prev_page)
            keyboard.add_hotkey('left arrow', self.prev_page)
            keyboard.add_hotkey('d', self.next_page)
            keyboard.add_hotkey('right arrow', self.next_page)
            # FIXME close reader with esc key throws error
            # keyboard.on_press('esc', self.close_reader)

            # make mac hoykeys
            self.reader_window.bind('a', lambda _: self.prev_page())
            self.reader_window.bind('<Left>', lambda _: self.prev_page())
            self.reader_window.bind('d', lambda _: self.next_page())
            self.reader_window.bind('<Right>', lambda _: self.next_page())
            self.reader_window.bind('<Escape>', lambda _: self.close_reader())

            # push description window down
            self.book_window.attributes('-topmost', 0)

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

            # buttons
            next_page = customtkinter.CTkButton(self.reader_window, text="->", command=self.next_page,
                                                hover_color=dark_pink, fg_color=light_pink, text_color=black)
            prev_page = customtkinter.CTkButton(self.reader_window, text="<-", command=self.prev_page,
                                                hover_color=dark_pink, fg_color=light_pink, text_color=black)
            close = customtkinter.CTkButton(self.reader_window, text="EXIT", command=self.close_reader,
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

    def append_new_tags(self, book: Book, tag_json: str, checked_tag: str):
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
                self.load_tab(tag_json)

    def open_book_description(self, book: Book, tag_json: str):
        if self.book_window is None or not self.book_window.winfo_exists():
            self.reader_window = None
            self.book_window = customtkinter.CTkToplevel()
            self.book_window.geometry(f"{1920}x{1080}")
            #  sets to the center of the screen
            # print("width: " + str(self.winfo_width()) + " screenwidth: " + str(self.winfo_screenwidth()))
            # print("height: " + str(self.winfo_height()) + " screenheight: " + str(self.winfo_screenheight()))
            self.book_window.geometry('%d+%d' % (
                340, 220
            ))
            # FIXME for fucks sake for the life of me i cannot center this fucking window i'm losing my mind

            # center shit
            self.book_window.grid_columnconfigure(0, weight=1)
            self.book_window.grid_columnconfigure(1, weight=1)
            self.book_window.grid_columnconfigure(2, weight=1)

            # make widgets
            # read button, making new cover to resize
            read_button = customtkinter.CTkButton(self.book_window, compound="top", fg_color="transparent",
                                                  hover_color=dark_pink, font=(
                                                      "Roboto", 16),
                                                  image=book.get_full_cover(),
                                                  command=lambda x=book: self.open_reader(
                                                      x),
                                                  text=indent_string(book.get_name()))

            # labels
            book_link_label = customtkinter.CTkLabel(self.book_window, text="Book Link", font=("Roboto", 20),
                                                     text_color=light_pink)
            book_name_label = customtkinter.CTkLabel(self.book_window, text="Book Name", font=("Roboto", 20),
                                                     text_color=light_pink)
            book_author_label = customtkinter.CTkLabel(self.book_window, text="Book Author", font=("Roboto", 20),
                                                       text_color=light_pink)

            # buttons
            book_link_button = customtkinter.CTkButton(self.book_window, text="Update Link",
                                                       fg_color=light_pink, hover_color=dark_pink, text_color=black)
            book_name_button = customtkinter.CTkButton(self.book_window, text="Update Name",
                                                       fg_color=light_pink, hover_color=dark_pink, text_color=black)
            book_author_button = customtkinter.CTkButton(self.book_window, text="Update Author",
                                                         fg_color=light_pink, hover_color=dark_pink, text_color=black)

            # entry
            w = 925
            book_link_entry = customtkinter.CTkEntry(
                self.book_window, placeholder_text="LINK", width=w)
            book_name_entry = customtkinter.CTkEntry(
                self.book_window, placeholder_text="NAME", width=w)
            book_author_entry = customtkinter.CTkEntry(
                self.book_window, placeholder_text="AUTHOR", width=w)
            book_link_entry.insert(0, book.get_link())
            book_name_entry.insert(0, book.get_name())
            book_author_entry.insert(0, book.get_author())

            # scrollable frame
            tag_scroller = customtkinter.CTkScrollableFrame(
                self.book_window, width=400, height=300)
            page_scroller = customtkinter.CTkScrollableFrame(
                self.book_window, width=1850, height=440)

            # get pages
            page_thumbs = book.get_pages(True)

            tag_checks: list[customtkinter.CTkCheckBox] = []

            r = 0
            c = 0

            # TODO pull from a JSON

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
                                                      z=i:
                                                      self.append_new_tags(x, y, z))
                check_box.grid(row=r, column=c, padx=10, pady=10)
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
            read_button.grid(row=0, column=0, rowspan=6)

            book_link_label.grid(row=0, column=1, padx=pad, pady=pad)
            book_name_label.grid(row=2, column=1, padx=pad, pady=pad)
            book_author_label.grid(row=4, column=1, padx=pad, pady=pad)

            book_link_entry.grid(
                row=1, column=1, columnspan=2, padx=pad, pady=pad)
            book_name_entry.grid(
                row=3, column=1, columnspan=2, padx=pad, pady=pad)
            book_author_entry.grid(
                row=5, column=1, columnspan=2, padx=pad, pady=pad)

            book_link_button.grid(
                row=0, column=2, sticky="ns", padx=pad, pady=pad)
            book_name_button.grid(
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

            # FIXME for some reason, if this isn't here then after you close the window and try to reopen the book,
            #  it crashes, seems like book's data gets fucked, it is also taking some memory
            self.load_tab(tag_json)

            # the reason this is all the way down here is cause
            # it keeps it on the bottom so the user doesn't see till done
            self.book_window.attributes('-topmost', 1)

        else:
            self.book_window.focus()  # if window exists focus it

    def next_tab(self, tag_json: str):
        # print(str(self.current_tab) + " < " + str(math.ceil((self.book_count - 1) / 10)))
        if self.current_tab < math.ceil(self.book_count / self.books_per_page) - 1:
            self.current_tab += 1
            self.load_tab(tag_json)

    def prev_tab(self, tag_json: str):
        if self.current_tab != 0:
            self.current_tab -= 1
            self.load_tab(tag_json)

    def load_tab(self, tag_json: str):

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

        books: list[Book] = []
        # load all the books (metadata) into memory
        for i in books_json['book']:
            books.append(Book(i['path'], i['name'],
                              i['author'], i['link'], i['tagged']))

        # TODO
        #  call sorting tags or authors functions here maybe?
        #  maybe i'll need to make a library loading function inside the tab or author class to do this

        # multiply number of books per page by the current page number
        # to find the starting index to grab the books
        # print("index to start at: " + str(self.current_tab * self.books_per_page))
        index_to_start_at = self.current_tab * self.books_per_page

        # print(str(len(books)))
        # print("tab count: " + str(math.ceil(len(books) / self.books_per_page)))
        tab_count = math.ceil(len(books) / self.books_per_page)
        # excess books so say the library is 35, then this comes to 5 to grab the last few for the last page

        counter = 0
        # print("current tab: " + str(self.current_tab))
        # print("books per page: " + str(self.books_per_page))
        # print(str(tab_count) + " != " + str(self.current_tab+1))
        if self.book_count == 0:
            # TODO  works but, make the conditional be less shit
            pass

        elif tab_count != self.current_tab + 1:
            # create the book objects
            while counter < self.books_per_page:
                button = customtkinter.CTkButton(self, compound="top",
                                                 image=books[index_to_start_at].get_cover(
                                                 ),
                                                 command=lambda
                                                 x=books[index_to_start_at], y=tag_json: self.open_book_description(
                                                     x, y),
                                                 fg_color="transparent", hover_color=dark_pink,
                                                 text=indent_string(
                                                     books[index_to_start_at].get_name()),
                                                 font=("Roboto", 18))

                self.book_buttons.append(button)
                index_to_start_at += 1
                counter += 1
        else:
            # create the book objects
            while counter < self.excess_books:
                button = customtkinter.CTkButton(self, compound="top",
                                                 image=books[index_to_start_at].get_cover(
                                                 ),
                                                 command=lambda
                                                 x=books[index_to_start_at], y=tag_json: self.open_book_description(
                                                     x, y),
                                                 fg_color="transparent", hover_color=dark_pink,
                                                 text=indent_string(
                                                     books[index_to_start_at].get_name()),
                                                 font=("Roboto", 18))

                self.book_buttons.append(button)
                index_to_start_at += 1
                counter += 1

        self.print_page()

        gc.collect()

    def print_page(self):
        r = 0
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
        book: list[Book] = []

        if path.isfile(self.library_json) is False:
            print("FILE NOT FOUND")
        else:
            with open(self.library_json) as f:
                books_json = json.load(f)
                # grab the metadata
                for i in books_json['book']:
                    book.append(Book(i['path'], i['name'],
                                     i['author'], i['link'], i['tagged']))

        self.book_count = len(book)
        self.excess_books = self.books_per_page - (math.ceil(len(book) / self.books_per_page)
                                                   * self.books_per_page - len(book))

    def get_current_tab(self):
        return self.current_tab

    def __init__(self, library_json: str, tag_json: str, master: customtkinter.CTk, **kwargs):
        super().__init__(master, **kwargs)

        # keyboard.clear_all_hotkeys()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)

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

        self.load_tab(tag_json)


class TabNavigator(customtkinter.CTkFrame):
    def __init__(self, bookframe: BookFrame, tag_json: str, master: customtkinter.CTk, **kwargs):
        super().__init__(master, **kwargs)
        next_tab = customtkinter.CTkButton(self, text="Next Page", command=lambda x=tag_json: bookframe.next_tab(x), width=400,
                                           fg_color=light_pink,
                                           text_color=black,
                                           hover_color=dark_pink)
        prev_tab = customtkinter.CTkButton(self, text="Last Page", command=lambda x=tag_json: bookframe.prev_tab(x), width=400,
                                           fg_color=light_pink,
                                           text_color=black,
                                           hover_color=dark_pink)

        prev_tab.grid(row=0, column=0, padx=100, pady=10)
        next_tab.grid(row=0, column=2, padx=100, pady=10)

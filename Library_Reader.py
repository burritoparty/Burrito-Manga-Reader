import copy
import gc
import json
from os import path
import customtkinter
import keyboard
from Book import Book
from Database import *
from Functions import *
# test line

class BookFrame(customtkinter.CTkScrollableFrame):

    def close_reader(self):
        # lift description window back up
        self.reader_window.destroy()
        self.book_window.attributes('-topmost', 1)

    def next_page_call(self):
        if self.current_page_num < len(self.page_list) - 1:
            # destroy current items
            self.page.destroy()
            self.pagenum_label.destroy()

            # update page nymber
            self.current_page_num += 1

            # change the page
            self.page = customtkinter.CTkLabel(self.reader_window,
                                               image=self.page_list[self.current_page_num], text=None)
            self.page.grid(row=0, column=0, columnspan=3)

            # update the user's page counter
            self.pagenum_text = str(str(self.current_page_num + 1) + " / " + str(len(self.page_list)))
            self.pagenum_label = customtkinter.CTkLabel(self.reader_window, text=self.pagenum_text, font=("Roboto", 20))
            self.pagenum_label.grid(row=1, column=1)

    def prev_page_call(self):
        if self.current_page_num != 0:
            # destroy current items
            self.page.destroy()
            self.pagenum_label.destroy()

            # update page nymber
            self.current_page_num -= 1

            # change the page
            self.page = customtkinter.CTkLabel(self.reader_window,
                                               image=self.page_list[self.current_page_num], text=None)
            self.page.grid(row=0, column=0, columnspan=3)

            # update the user's page counter
            self.pagenum_text = str(str(self.current_page_num + 1) + " / " + str(len(self.page_list)))
            self.pagenum_label = customtkinter.CTkLabel(self.reader_window, text=self.pagenum_text, font=("Roboto", 20))
            self.pagenum_label.grid(row=1, column=1)

    def open_reader(self, book):
        if self.reader_window is None or not self.reader_window.winfo_exists():

            # make hotkeys
            keyboard.add_hotkey('a', self.prev_page_call)
            keyboard.add_hotkey('left arrow', self.prev_page_call)
            keyboard.add_hotkey('d', self.next_page_call)
            keyboard.add_hotkey('right arrow', self.next_page_call)
            keyboard.add_hotkey('esc', self.close_reader)

            self.reader_window = customtkinter.CTkToplevel()
            self.reader_window.attributes('-fullscreen', True)
            self.reader_window.attributes('-topmost', 3)

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
            self.pagenum_text = str(str(self.current_page_num + 1) + " / " + str(len(self.page_list)))
            self.pagenum_label = customtkinter.CTkLabel(self.reader_window, text=self.pagenum_text, font=("Roboto", 20))

            # buttons
            next_page = customtkinter.CTkButton(self.reader_window, text="->", command=self.next_page_call,
                                                hover_color=dark_pink, fg_color=light_pink, text_color=black)
            prev_page = customtkinter.CTkButton(self.reader_window, text="<-", command=self.prev_page_call,
                                                hover_color=dark_pink, fg_color=light_pink, text_color=black)
            close = customtkinter.CTkButton(self.reader_window, text="EXIT", command=self.close_reader,
                                            hover_color=dark_pink, fg_color=light_pink, text_color=black)

            # page
            self.page = customtkinter.CTkLabel(self.reader_window, text=None, image=self.page_list[0], compound="n")

            # place all the shit
            pad = 5
            self.page.grid(row=0, column=0, columnspan=3, padx=pad, pady=pad)
            prev_page.grid(row=1, column=0, padx=pad, pady=pad)
            self.pagenum_label.grid(row=1, column=1, padx=pad, pady=pad)
            next_page.grid(row=1, column=2, padx=pad, pady=pad)
            close.grid(row=2, column=1, padx=pad, pady=10)



        else:
            self.reader_window.focus()

    def close_book_description(self):
        self.book_window.destroy()
        # yeet that memory into the stratosphere!
        gc.collect()

    def open_book_description(self, book, json_index):
        if self.book_window is None or not self.book_window.winfo_exists():
            self.reader_window = None
            self.book_window = customtkinter.CTkToplevel()
            self.book_window.geometry(f"{1920}x{1080}")
            # FIXME for fucks sake for the life of me i cannot center this fucking window i'm losing my mind

            # center shit
            self.book_window.grid_columnconfigure(0, weight=1)
            self.book_window.grid_columnconfigure(1, weight=1)
            self.book_window.grid_columnconfigure(2, weight=1)

            # make widgets
            # read button, making new cover to resize
            cover = copy.copy(book.get_cover())
            cover.configure(size=(400, 550))
            read_button = customtkinter.CTkButton(self.book_window, compound="top", fg_color="transparent",
                                                  hover_color=dark_pink, text_color=light_pink,
                                                  image=cover, command=lambda x=book: self.open_reader(x),
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
            book_link_entry = customtkinter.CTkEntry(self.book_window, placeholder_text="LINK", width=w)
            book_name_entry = customtkinter.CTkEntry(self.book_window, placeholder_text="NAME", width=w)
            book_author_entry = customtkinter.CTkEntry(self.book_window, placeholder_text="AUTHOR", width=w)
            book_link_entry.insert(0, book.get_link())
            book_name_entry.insert(0, book.get_name())
            book_author_entry.insert(0, book.get_author())

            # scrollable frame
            tag_scroller = customtkinter.CTkScrollableFrame(self.book_window, width=400, height=300)
            page_scroller = customtkinter.CTkScrollableFrame(self.book_window, width=1850, height=440)

            # get pages
            page_thumbs = book.get_pages(True)

            tag_checks = []

            r = 0
            c = 0

            # TODO pull from a json
            for i in tags:
                check_box = customtkinter.CTkCheckBox(tag_scroller, text=i,
                                                      hover_color=light_pink, fg_color=dark_pink, text_color=light_pink)
                check_box.grid(row=r, column=c, padx=20, pady=20)
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

            book_link_entry.grid(row=1, column=1, columnspan=2, padx=pad, pady=pad)
            book_name_entry.grid(row=3, column=1, columnspan=2, padx=pad, pady=pad)
            book_author_entry.grid(row=5, column=1, columnspan=2, padx=pad, pady=pad)

            book_link_button.grid(row=0, column=2, sticky="ns", padx=pad, pady=pad)
            book_name_button.grid(row=2, column=2, sticky="ns", padx=pad, pady=pad)
            book_author_button.grid(row=4, column=2, sticky="ns", padx=pad, pady=pad)

            tag_scroller.grid(row=0, column=3, rowspan=6, padx=pad, pady=pad)
            page_scroller.grid(row=6, column=0, columnspan=4, padx=pad, pady=pad)

            self.book_window.protocol('WM_DELETE_WINDOW', self.close_book_description)

            # FIXME for some reason, if this isn't here then after you close the window and try to reopen the book,
            #  it crashes, seems like book's data gets fucked, it is also taking some memory
            self.refresh_library()

            # the reason this is all the way down here is cause
            # it keeps it on the bottom so the user doesn't see till done
            self.book_window.attributes('-topmost', 1)

        else:
            self.book_window.focus()  # if window exists focus it

    def refresh_library(self):
        # import from json
        book = []
        if path.isfile("D:\Burrito Manga Reader\library.json") is False:
            print("FILE NOT FOUND")
        else:
            with open("D:\Burrito Manga Reader\library.json") as f:
                books_json = json.load(f)

                # grab the metadata
                for i in books_json['book']:
                    book.append(Book(i['path'], i['name'], i['author'], i['link'], i['tagged']))

                for i in self.book_buttons:
                    i.destroy()
                self.book_buttons.clear()

                num_loops = 0
                r = 1
                c = 0

                for i in book:
                    book_button = customtkinter.CTkButton(self, compound="top", image=i.get_cover(),
                                                          command=lambda
                                                              x=i, y=num_loops: self.open_book_description(x, y),
                                                          fg_color="transparent", hover_color=dark_pink,
                                                          text=indent_string(i.get_name()), text_color=light_pink,
                                                          font=("Roboto", 16))
                    book_button.grid(row=r, column=c, padx=15, pady=10)
                    self.book_buttons.append(book_button)

                    if c == 5:
                        c = 0
                        r += 1
                    else:
                        c += 1
                    num_loops += 1

        # FIXME i need to fix something about this function to take less memory

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.book_window = None

        self.book_buttons = []

        refresh_library = customtkinter.CTkButton(self, text="Refresh Library", command=self.refresh_library,
                                                  hover_color=dark_pink, fg_color=light_pink, text_color=black)

        refresh_library.grid(row=0, column=0)

        self.refresh_library()

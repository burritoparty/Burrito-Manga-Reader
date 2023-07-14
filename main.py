import argparse
import pathlib

from Author import *
from Database import *
from Import import *
from Library_Reader import *
from Tag import *

arg_parser = argparse.ArgumentParser(prog='Burrito-Manga-Reader')
arg_parser.add_argument('mangaloc', type=pathlib.Path,
                        default="D:\\Burrito Manga Reader Library",
                        nargs='?')
args = arg_parser.parse_args()

# create database
library_json = os.path.join(args.mangaloc, "library.json")
if os.path.exists(library_json) is False:
    file = open(library_json, "x")
    with open(library_json, "w") as f:
        books_json = {
            "book": [
            ]
        }
        json.dump(books_json, f, indent=2)
    file.close()

# create tag database
tags_json = os.path.join(args.mangaloc, "tags.json")
if os.path.exists(tags_json) is False:
    file = open(tags_json, "x")
    with open(tags_json, "w") as f:
        books_json = {
            "tags": [
            ]
        }
        json.dump(books_json, f, indent=2)
    file.close()

# create author database
authors_json = os.path.join(args.mangaloc, "authors.json")
if os.path.exists(authors_json) is False:
    file = open(authors_json, "x")
    with open(authors_json, "w") as f:
        books_json = {
            "authors": [
            ]
        }
        json.dump(books_json, f, indent=2)
        file.close()

customtkinter.set_appearance_mode("dark")
root = customtkinter.CTk()  # main window
root.title("Burrito Manga Reader")  # name of program
# set dimensions and center window
root.geometry('%dx%d+%d+%d' % (1920, 1080,
                               get_x_coordinates(
                                   1920, root.winfo_screenwidth()),
                               get_y_coordinates(1080, root.winfo_screenheight())))

# make frames
root.bookDisplayTabs = BookFrame(
    library_json=library_json, tag_json=tags_json, authors_json=authors_json, master=root, width=1650, height=1000)
root.tagFrame = TagFrame(
    library_json=library_json, authors_json=authors_json, tag_json=tags_json, bookframe=root.bookDisplayTabs, master=root)
root.authorFrame = AuthorFrame(
    library_json=library_json, authors_json=authors_json, tag_json=tags_json, bookframe=root.bookDisplayTabs, master=root)
root.importFrame = ImportFrame(
    library_json=library_json, library_path=args.mangaloc, tag_json=tags_json, authors_json=authors_json,
    bookframe=root.bookDisplayTabs, master=root)
root.tab_nav = TabNavigator(
    bookframe=root.bookDisplayTabs, tag_json=tags_json, authors_json=authors_json, master=root)

# place frames
root.tagFrame.grid(row=0, column=0, padx=20, pady=20, rowspan=2)
root.authorFrame.grid(row=2, column=0, padx=20, pady=20)
root.importFrame.grid(row=3, column=0, padx=20, pady=0)
root.bookDisplayTabs.grid(row=0, column=1, rowspan=10,
                          sticky="nsew", padx=5, pady=5)
root.tab_nav.grid(row=10, column=1, padx=5, pady=5)

root.mainloop()

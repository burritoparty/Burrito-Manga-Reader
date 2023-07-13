import json
from os import path

import customtkinter

from Database import *
from Functions import *
from Library_Reader import BookFrame


class AuthorFrame(customtkinter.CTkFrame):

    def author_append_call(self, authors_json: str):
        authors: list[str] = []
        if path.isfile(authors_json) is False:
            print("path dont exist")
        else:
            # create the dialog box
            authors_append_dialogue = customtkinter.CTkInputDialog(
                text="New Author: ", title="Append a new author",
                button_fg_color=light_pink,
                button_text_color=black,
                button_hover_color=dark_pink)
            authors_append_dialogue.geometry('0+0')

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

    def author_rename_call(self, authors_json: str, window: customtkinter.CTkToplevel | None,
                           tag_json: str, library_json: str, bookframe):
        authors: list[str] = []
        buttons: list[customtkinter.CTkButton] = []
        index = 0
        num_loops = 0
        r = 0
        c = 0
        if path.isfile(authors_json) is False:
            print("path dont exist")
        else:
            if window is None or not window.winfo_exists():

                # make the window
                window = customtkinter.CTkToplevel()
                window.attributes('-topmost', 1)
                window.title("Rename author")
                window.geometry("0+0")

                # load the JSON
                with open(authors_json, 'r') as f:
                    load_authors = json.load(f)

                # load the author names from the JSON into an array
                for i in load_authors['authors']:
                    authors.append(i['name'])

                # make button objects and place them in the window
                if len(authors) != 0:
                    # make the buttons
                    for i in authors:
                        button = customtkinter.CTkButton(window, text=i,
                                                         fg_color=light_pink,
                                                         text_color=black,
                                                         hover_color=dark_pink,
                                                         command=lambda
                                                         w=window,
                                                         x=tag_json,
                                                         y=i,
                                                         z=authors,
                                                         a=load_authors,
                                                         b=library_json,
                                                         c=authors_json,
                                                         d=bookframe:
                                                         self.author_rename_dialogue(w, x, y, z, a, b, c, d))
                        buttons.append(button)
                        buttons[index].grid(row=r, column=c, padx=20, pady=20)

                        if c == 2:
                            c = 0
                            r += 1
                        else:
                            c += 1
                        num_loops += 1
                        index += 1
                else:
                    label = customtkinter.CTkLabel(
                        window, text="There are no authors to rename")
                    label.grid(padx=10, pady=10)

            else:
                window.focus()

    def author_rename_dialogue(self, window: customtkinter.CTkToplevel, tags_json: str,
            author_to_rename: str, author_array: list[str], author_loader: dict,
            library_json: str, authors_json: str, bookframe):
        # create dialogue entry
        text = "Rename author: " + author_to_rename
        author_rename_dialogue = customtkinter.CTkInputDialog(
            text=text, title="Rename an author",
        button_text_color=black, button_fg_color=light_pink, button_hover_color=dark_pink)
        author_rename_dialogue.geometry('0+0')

        # get the author's new name
        new_name = author_rename_dialogue.get_input() or ""

        # check if the input is valid
        if not check_exists(new_name, author_array, True):
            error = customtkinter.CTkToplevel()
            error.attributes('-topmost', 2)
            error.geometry("0+0")
            label = customtkinter.CTkLabel(error,
                                           text="Please enter a new name for the author",
                                           font=("Roboto", 20))
            label.grid(padx=10, pady=10)
        else:
            # remove the old author and append the new author to the array
            author_array.remove(author_to_rename)
            author_array.append(new_name)
            author_array.sort()

            # delete all the authors
            del author_loader['authors']

            # delete ['authors'] object from JSON
            with open(authors_json, 'w') as f:
                json.dump(author_loader, f, indent=2)

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
            for i in author_array:
                load_authors["authors"].append({
                    "name": i
                })

            # finalize JSON
            with open(authors_json, 'w') as f:
                json.dump(load_authors, f, indent=2)

            # rename the authors in the library
            with open(library_json) as f:
                # load the library
                books_json = json.load(f)
                for b in books_json['book']:
                    if author_to_rename in b['author']:
                        b['author'] = new_name

            # now dump the library
            with open(library_json, 'w') as f:
                json.dump(books_json, f, indent=2)

            # reload the library
            bookframe.load_tab(tags_json, authors_json)

            window.destroy()

    def __init__(self, library_json: str, authors_json: str, tag_json: str, bookframe: BookFrame, master: customtkinter.CTk, **kwargs):
        super().__init__(master, **kwargs)

        # make windows
        authors_rename_window = None

        add = Image.open(resource(os.path.join('button_icons', 'add_icon.png')))
        ctk_add = customtkinter.CTkImage(dark_image=add)
        rename = Image.open(resource(os.path.join('button_icons', 'rename_icon.png')))
        ctk_rename = customtkinter.CTkImage(dark_image=rename)

        # make the buttons
        self.author_append = customtkinter.CTkButton(self,
                                                     image=ctk_add,
                                                     compound="left",
                                                     anchor="center",
                                                     text="Add Author",
                                                     fg_color=light_pink,
                                                     text_color=black,
                                                     hover_color=dark_pink,
                                                     command=lambda x=authors_json: self.author_append_call(x))
        self.author_rename = customtkinter.CTkButton(self,
                                                     image=ctk_rename,
                                                     compound="left",
                                                     anchor="center",
                                                     text="Edit Author",
                                                     fg_color=light_pink,
                                                     text_color=black,
                                                     hover_color=dark_pink,
                                                     command=lambda
                                                     x=authors_json,
                                                     y=authors_rename_window,
                                                     z=tag_json,
                                                     a=library_json,
                                                     b=bookframe: self.author_rename_call(x, y, z, a, b))
        self.author_append.grid(row=0, column=0, padx=20, pady=20)
        self.author_rename.grid(row=1, column=0, padx=20, pady=20)

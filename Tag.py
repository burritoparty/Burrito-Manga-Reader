import json
from os import path

import customtkinter

from Database import black, dark_pink, light_pink
from Functions import *
from Library_Reader import BookFrame


class TagFrame(customtkinter.CTkFrame):

    def tag_append_call(self, tags_json: str):
        tags: list[str] = []
        if path.isfile(tags_json) is False:
            print("path dont exist")
        else:
            # create the dialogue box
            tags_append_dialogue = customtkinter.CTkInputDialog(
                text="New tag: ", title="Append a new tag")
            tags_append_dialogue.geometry('0+0')

            # load the JSON
            with open(tags_json, 'r') as f:
                load_tags = json.load(f)

            # load the tag names from the JSON into an array
            for i in load_tags['tags']:
                tags.append(i['name'])

            # get the input from the user
            new_tag = tags_append_dialogue.get_input()

            # check if the input is valid
            if new_tag == '' or new_tag is None:
                # user hit the cancel button
                pass
            elif check_exists(new_tag, tags, False) is False:
                error = customtkinter.CTkToplevel()
                error.geometry("0+0")
                label = customtkinter.CTkLabel(error,
                                               text="this tag already exists\n(not case sensitive)",
                                               font=("Roboto", 20))
                label.grid(padx=10, pady=10)
            else:
                # append the new tag to the array
                tags.append(new_tag)
                tags.sort()

                # delete all the tags
                del load_tags['tags']

                # delete ['tags'] object from JSON
                with open(tags_json, 'w') as f:
                    json.dump(load_tags, f, indent=2)

                # load the ['tags'] object back into JSON
                with open(tags_json, 'w') as f:
                    t = {
                        "tags": [

                        ]
                    }
                    json.dump(t, f, indent=2)

                # load the JSON back in
                with open(tags_json, 'r') as f:
                    load_tags = json.load(f)

                # load them all back into load_tags
                for i in tags:
                    load_tags["tags"].append({
                        "name": i
                    })

                # finalize JSON
                with open(tags_json, 'w') as f:
                    json.dump(load_tags, f, indent=2)

    def tag_delete_call(self, library_json: str, tags_json: str, window: customtkinter.CTkToplevel | None):
        # TODO need to remove this tag from all entries in the library that have it
        tags: list[str] = []
        buttons: list[customtkinter.CTkButton] = []
        index = 0
        num_loops = 0
        r = 0
        c = 0
        if path.isfile(tags_json) is False:
            print("path dont exist")
        else:
            if window is None or not window.toplevel_window.winfo_exists():

                # make the window
                window = customtkinter.CTkToplevel()
                window.attributes('-topmost', 1)
                window.title("Delete tag")
                window.geometry("0+0")

                # load the JSON
                with open(tags_json, 'r') as f:
                    load_tags = json.load(f)

                # load the tag names from the JSON into an array
                for i in load_tags['tags']:
                    tags.append(i['name'])

                # make button objects and place them in the window
                if len(tags) != 0:
                    # make the buttons
                    for i in tags:
                        button = customtkinter.CTkButton(window, text=i,
                                                         command=lambda
                                                         w=window,
                                                         x=tags_json,
                                                         y=i,
                                                         z=tags,
                                                         a=load_tags,
                                                         b=library_json: self.tag_deleter(w, x, y, z, a, b))
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
                        window, text="There are no tags to delete")
                    label.grid(padx=10, pady=10)

            else:
                window.focus()

    def tag_deleter(
            self, window: customtkinter.CTkToplevel, tags_json: str,
            tag_to_delete: str, tag_array: list[str], tag_loader: dict,
            library_json: str):

        # remove the tags from the library
        with open(library_json) as f:
            # load the library
            books_json = json.load(f)
            for b in books_json['book']:
                b['tagged'].remove(tag_to_delete)

        # now dump the library
        with open(library_json, 'w') as f:
            json.dump(books_json, f, indent=2)

        # remove tag
        tag_array.remove(tag_to_delete)
        tag_array.sort()

        # delete all the tags
        del tag_loader['tags']

        # delete ['tags'] object from JSON
        with open(tags_json, 'w') as f:
            json.dump(tag_loader, f, indent=2)

        # load the ['tags'] object back into JSON
        with open(tags_json, 'w') as f:
            t = {
                "tags": [

                ]
            }
            json.dump(t, f, indent=2)

        # load the JSON back in
        with open(tags_json, 'r') as f:
            load_tags = json.load(f)

        # load them all back into load_tags
        for i in tag_array:
            load_tags["tags"].append({
                "name": i
            })

        # finalize JSON
        with open(tags_json, 'w') as f:
            json.dump(load_tags, f, indent=2)

        window.destroy()

    def tag_rename_call(self, tags_json: str, window: customtkinter.CTkToplevel | None):
        # TODO need to rename this tag in all entries in the library that have it
        tags: list[str] = []
        buttons: list[customtkinter.CTkButton] = []
        index = 0
        num_loops = 0
        r = 0
        c = 0
        if path.isfile(tags_json) is False:
            print("path dont exist")
        else:
            if window is None or not window.toplevel_window.winfo_exists():

                # make the window
                window = customtkinter.CTkToplevel()
                window.attributes('-topmost', 1)
                window.title("Rename tag")
                window.geometry("0+0")

                # load the JSON
                with open(tags_json, 'r') as f:
                    load_tags = json.load(f)

                # load the tag names from the JSON into an array
                for i in load_tags['tags']:
                    tags.append(i['name'])

                # make button objects and place them in the window
                if len(tags) != 0:
                    # make the buttons
                    for i in tags:
                        button = customtkinter.CTkButton(window, text=i,
                                                         command=lambda
                                                         w=window,
                                                         x=tags_json,
                                                         y=i,
                                                         z=tags,
                                                         a=load_tags:
                                                         self.tag_rename_dialogue(w, x, y, z, a))
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
                        window, text="There are no tags to rename")
                    label.grid(padx=10, pady=10)

            else:
                window.focus()

    def tag_rename_dialogue(
            self, window: customtkinter.CTkToplevel, tags_json: str,
            tag_to_rename: str, tag_array: list[str], tag_loader: dict):

        # create dialogue entry
        text = "Rename tag: " + tag_to_rename
        tags_rename_dialogue = customtkinter.CTkInputDialog(
            text=text, title="Rename a tag")
        tags_rename_dialogue.geometry('0+0')

        # get the tag's new name
        new_name = tags_rename_dialogue.get_input() or ""

        # check if the input is valid
        if not check_exists(new_name, tag_array, True):
            error = customtkinter.CTkToplevel()
            error.attributes('-topmost', 2)
            error.geometry("0+0")
            label = customtkinter.CTkLabel(error,
                                           text="Please enter a new name for the tag",
                                           font=("Roboto", 20))
            label.grid(padx=10, pady=10)
        else:
            # remove the old tag and append the new tag to the array
            print(tag_to_rename)
            print(tag_array)
            tag_array.remove(tag_to_rename)
            tag_array.append(new_name)
            tag_array.sort()

            # delete all the tags
            del tag_loader['tags']

            # delete ['tags'] object from JSON
            with open(tags_json, 'w') as f:
                json.dump(tag_loader, f, indent=2)

            # load the ['tags'] object back into JSON
            with open(tags_json, 'w') as f:
                t = {
                    "tags": [

                    ]
                }
                json.dump(t, f, indent=2)

            # load the JSON back in
            with open(tags_json, 'r') as f:
                load_tags = json.load(f)

            # load them all back into load_tags
            for i in tag_array:
                load_tags["tags"].append({
                    "name": i
                })

            # finalize JSON
            with open(tags_json, 'w') as f:
                json.dump(load_tags, f, indent=2)

            window.destroy()

    def __init__(self, library_json, tag_json: str, bookframe: BookFrame, master: customtkinter.CTk, **kwargs):
        super().__init__(master, **kwargs)

        # make windows
        tag_sort_window = None
        tags_rename_window = None
        tags_delete_window = None

        # make the label
        self.tag_sort = customtkinter.CTkButton(self,
                                                text="Sort by tag",
                                                fg_color=light_pink,
                                                text_color=black,
                                                hover_color=dark_pink)

        # make the buttons
        self.tag_append = customtkinter.CTkButton(self,
                                                  text="Add tag",
                                                  fg_color=light_pink,
                                                  text_color=black,
                                                  hover_color=dark_pink,
                                                  command=lambda x=tag_json: self.tag_append_call(x))
        self.tag_delete = customtkinter.CTkButton(self,
                                                  text="Delete tag",
                                                  fg_color=light_pink,
                                                  text_color=black,
                                                  hover_color=dark_pink,
                                                  command=lambda w=library_json, x=tag_json, y=tags_delete_window:
                                                  self.tag_delete_call(w, x, y))
        self.tag_rename = customtkinter.CTkButton(self,
                                                  text="Rename tag",
                                                  fg_color=light_pink,
                                                  text_color=black,
                                                  hover_color=dark_pink,
                                                  command=lambda x=tag_json, y=tags_rename_window:
                                                  self.tag_rename_call(x, y))

        self.tag_sort.grid(row=0, column=0, padx=20, pady=20)
        self.tag_append.grid(row=2, column=0, padx=20, pady=20)
        self.tag_delete.grid(row=3, column=0, padx=20, pady=20)
        self.tag_rename.grid(row=4, column=0, padx=20, pady=20)

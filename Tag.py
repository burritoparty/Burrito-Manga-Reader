import json
import os
import sys
from os import path

import customtkinter
from PIL import Image

from Database import black, dark_pink, light_pink
from Functions import check_exists, resource
from Library_Reader import BookFrame


class TagFrame(customtkinter.CTkFrame):
    def tag_append_call(self, tags_json: str, authors_json: str, bookframe):
        tags: list[str] = []
        if path.isfile(tags_json) is False:
            print("path dont exist")
        else:
            # create the dialogue box
            tags_append_dialogue = customtkinter.CTkInputDialog(
                text="New tag: ",
                title="Append a new tag",
                button_fg_color=light_pink,
                button_text_color=black,
                button_hover_color=dark_pink,
            )
            tags_append_dialogue.geometry("0+0")

            # load the JSON
            with open(tags_json, "r") as f:
                load_tags = json.load(f)

            # load the tag names from the JSON into an array
            for i in load_tags["tags"]:
                tags.append(i["name"])

            # get the input from the user
            new_tag = tags_append_dialogue.get_input()

            # check if the input is valid
            if new_tag == "" or new_tag is None:
                # user hit the cancel button
                pass
            elif check_exists(new_tag, tags, False) is False:
                error = customtkinter.CTkToplevel()
                error.geometry("0+0")
                label = customtkinter.CTkLabel(
                    error,
                    text="this tag already exists\n(not case sensitive)",
                    font=("Roboto", 20),
                )
                label.grid(padx=10, pady=10)
            else:
                # append the new tag to the array
                tags.append(new_tag)
                tags.sort()

                # delete all the tags
                del load_tags["tags"]

                # delete ['tags'] object from JSON
                with open(tags_json, "w") as f:
                    json.dump(load_tags, f, indent=2)

                # load the ['tags'] object back into JSON
                with open(tags_json, "w") as f:
                    t = {"tags": []}
                    json.dump(t, f, indent=2)

                # load the JSON back in
                with open(tags_json, "r") as f:
                    load_tags = json.load(f)

                # load them all back into load_tags
                for i in tags:
                    load_tags["tags"].append({"name": i})

                # finalize JSON
                with open(tags_json, "w") as f:
                    json.dump(load_tags, f, indent=2)

    def tag_delete_call(
        self,
        library_json: str,
        tags_json: str,
        window: customtkinter.CTkToplevel | None,
        authors_json: str,
        bookframe,
    ):
        tags: list[str] = []
        buttons: list[customtkinter.CTkButton] = []
        index = 0
        num_loops = 0
        r = 0
        c = 0
        if path.isfile(tags_json) is False:
            print("path dont exist")
        else:
            if window is None or not window.winfo_exists():
                # make the window
                window = customtkinter.CTkToplevel()
                window.attributes("-topmost", 1)
                window.title("Delete tag")
                window.geometry("0+0")

                # load the JSON
                with open(tags_json, "r") as f:
                    load_tags = json.load(f)

                # load the tag names from the JSON into an array
                for i in load_tags["tags"]:
                    tags.append(i["name"])

                # make button objects and place them in the window
                if len(tags) != 0:
                    # make the buttons
                    for i in tags:
                        button = customtkinter.CTkButton(
                            window,
                            text=i,
                            fg_color=light_pink,
                            text_color=black,
                            hover_color=dark_pink,
                            command=lambda i=i: self.tag_deleter(
                                window,
                                tags_json,
                                i,
                                tags,
                                load_tags,
                                library_json,
                                authors_json,
                                bookframe,
                            ),
                        )
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
                        window, text="There are no tags to delete"
                    )
                    label.grid(padx=10, pady=10)

            else:
                window.focus()

    def tag_deleter(
        self,
        window: customtkinter.CTkToplevel,
        tags_json: str,
        tag_to_delete: str,
        tag_array: list[str],
        tag_loader: dict,
        library_json: str,
        authors_json,
        bookframe,
    ):
        # remove the tags from the library
        with open(library_json) as f:
            # load the library
            books_json = json.load(f)
            for b in books_json["book"]:
                if tag_to_delete in b["tagged"]:
                    b["tagged"].remove(tag_to_delete)

        # now dump the library
        with open(library_json, "w") as f:
            json.dump(books_json, f, indent=2)

        # remove tag
        tag_array.remove(tag_to_delete)
        tag_array.sort()

        # delete all the tags
        del tag_loader["tags"]

        # delete ['tags'] object from JSON
        with open(tags_json, "w") as f:
            json.dump(tag_loader, f, indent=2)

        # load the ['tags'] object back into JSON
        with open(tags_json, "w") as f:
            t = {"tags": []}
            json.dump(t, f, indent=2)

        # load the JSON back in
        with open(tags_json, "r") as f:
            load_tags = json.load(f)

        # load them all back into load_tags
        for i in tag_array:
            load_tags["tags"].append({"name": i})

        # finalize JSON
        with open(tags_json, "w") as f:
            json.dump(load_tags, f, indent=2)

        bookframe.load_tab(tags_json, authors_json)

        window.destroy()

    def tag_rename_call(
        self,
        library_json: str,
        tags_json: str,
        window: customtkinter.CTkToplevel | None,
        authors_json: str,
        bookframe,
    ):
        tags: list[str] = []
        buttons: list[customtkinter.CTkButton] = []
        index = 0
        num_loops = 0
        r = 0
        c = 0
        if path.isfile(tags_json) is False:
            print("path dont exist")
        else:
            if window is None or not window.winfo_exists():
                # make the window
                window = customtkinter.CTkToplevel()
                window.attributes("-topmost", 1)
                window.title("Rename tag")
                window.geometry("0+0")

                # load the JSON
                with open(tags_json, "r") as f:
                    load_tags = json.load(f)

                # load the tag names from the JSON into an array
                for i in load_tags["tags"]:
                    tags.append(i["name"])

                # make button objects and place them in the window
                if len(tags) != 0:
                    # make the buttons
                    for i in tags:
                        button = customtkinter.CTkButton(
                            window,
                            text=i,
                            fg_color=light_pink,
                            text_color=black,
                            hover_color=dark_pink,
                            command=lambda i=i: self.tag_rename_dialogue(
                                window,
                                tags_json,
                                i,
                                tags,
                                load_tags,
                                library_json,
                                authors_json,
                                bookframe,
                            ),
                        )
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
                        window, text="There are no tags to rename"
                    )
                    label.grid(padx=10, pady=10)

            else:
                window.focus()

    def tag_rename_dialogue(
        self,
        window: customtkinter.CTkToplevel,
        tags_json: str,
        tag_to_rename: str,
        tag_array: list[str],
        tag_loader: dict,
        library_json: str,
        authors_json: str,
        bookframe,
    ):
        # create dialogue entry
        text = "Rename tag: " + tag_to_rename
        tags_rename_dialogue = customtkinter.CTkInputDialog(
            text=text,
            title="Rename a tag",
            button_text_color=black,
            button_fg_color=light_pink,
            button_hover_color=dark_pink,
        )
        tags_rename_dialogue.geometry("0+0")

        # get the tag's new name
        new_name = tags_rename_dialogue.get_input() or ""

        # check if the input is valid
        if not check_exists(new_name, tag_array, True):
            error = customtkinter.CTkToplevel()
            error.attributes("-topmost", 2)
            error.geometry("0+0")
            label = customtkinter.CTkLabel(
                error, text="Please enter a new name for the tag", font=("Roboto", 20)
            )
            label.grid(padx=10, pady=10)
        else:
            # remove the old tag and append the new tag to the array
            tag_array.remove(tag_to_rename)
            tag_array.append(new_name)
            tag_array.sort()

            # delete all the tags
            del tag_loader["tags"]

            # delete ['tags'] object from JSON
            with open(tags_json, "w") as f:
                json.dump(tag_loader, f, indent=2)

            # load the ['tags'] object back into JSON
            with open(tags_json, "w") as f:
                t = {"tags": []}
                json.dump(t, f, indent=2)

            # load the JSON back in
            with open(tags_json, "r") as f:
                load_tags = json.load(f)

            # load them all back into load_tags
            for i in tag_array:
                load_tags["tags"].append({"name": i})

            # finalize JSON
            with open(tags_json, "w") as f:
                json.dump(load_tags, f, indent=2)

            # rename the tags in the library
            with open(library_json) as f:
                # load the library
                books_json = json.load(f)
                for b in books_json["book"]:
                    if tag_to_rename in b["tagged"]:
                        b["tagged"].remove(tag_to_rename)
                        b["tagged"].append(new_name)

            # now dump the library
            with open(library_json, "w") as f:
                json.dump(books_json, f, indent=2)

            # reload the library
            bookframe.load_tab(tags_json, authors_json)

            window.destroy()

    def __init__(
        self,
        library_json,
        authors_json,
        tag_json: str,
        bookframe: BookFrame,
        master: customtkinter.CTk,
        **kwargs
    ):
        super().__init__(master, **kwargs)

        # make windows
        tags_rename_window = None
        tags_delete_window = None

        add = Image.open(
            resource(os.path.join("button_icons", "add_icon.png")))
        ctk_add = customtkinter.CTkImage(dark_image=add)
        delete = Image.open(
            resource(os.path.join("button_icons", "remove_icon.png")))
        ctk_delete = customtkinter.CTkImage(dark_image=delete)
        rename = Image.open(
            resource(os.path.join("button_icons", "rename_icon.png")))
        ctk_rename = customtkinter.CTkImage(dark_image=rename)

        # make the buttons
        self.tag_append = customtkinter.CTkButton(
            self,
            image=ctk_add,
            compound="left",
            anchor="center",
            text="Add Tag",
            fg_color=light_pink,
            text_color=black,
            hover_color=dark_pink,
            command=lambda: self.tag_append_call(
                tag_json, authors_json, bookframe),
        )
        self.tag_delete = customtkinter.CTkButton(
            self,
            image=ctk_delete,
            compound="left",
            anchor="center",
            text="Delete Tag",
            fg_color=light_pink,
            text_color=black,
            hover_color=dark_pink,
            command=lambda: self.tag_delete_call(
                library_json, tag_json, tags_delete_window, authors_json, bookframe
            ),
        )
        self.tag_rename = customtkinter.CTkButton(
            self,
            image=ctk_rename,
            compound="left",
            anchor="center",
            text="Edit Tag",
            fg_color=light_pink,
            text_color=black,
            hover_color=dark_pink,
            command=lambda: self.tag_rename_call(
                library_json, tag_json, tags_rename_window, authors_json, bookframe
            ),
        )

        self.tag_append.grid(row=0, column=0, padx=20, pady=20)
        self.tag_delete.grid(row=1, column=0, padx=20, pady=20)
        self.tag_rename.grid(row=2, column=0, padx=20, pady=20)

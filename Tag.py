import customtkinter
from Database import *
from Functions import *


class TagFrame(customtkinter.CTkFrame):

    # FIXME use this to refresh the combobox?
    def refresh_tag_combobox(self):
        self.tagCombobox.configure(values=tags)

    def tag_dialogue_window(self):
        dialog = customtkinter.CTkInputDialog(text="Name your new tag: ", title="Tag creation",
                                              button_fg_color=light_pink, button_text_color=black)
        dialog.geometry('%d+%d' % (
            get_x_coordinates(self.winfo_width(), self.winfo_screenwidth()),
            get_y_coordinates(self.winfo_height(), self.winfo_screenheight())
        ))

        # FIXME check input | fix if user presses X button
        #  also restrict to 15 or less characters

        new_tag = dialog.get_input()
        if check_exists(new_tag, tags, False) is True:
            tags.append(new_tag)

        tags.sort()
        self.refresh_tag_combobox()

    def delete_tag(self):
        if self.delete_tag is None or not self.delete_tag.winfo_exists():
            self.delete_tag = DeleteTag(self)  # create window if its None or destroyed
        else:
            self.delete_tag.focus()  # if window exists focus it

    def rename_tag(self):
        if self.rename_tag is None or not self.rename_tag.winfo_exists():
            self.rename_tag = RenameTag(self)  # create window if its None or destroyed
        else:
            self.rename_tag.focus()  # if window exists focus it

    def __init__(self, bookframe, master, **kwargs):
        super().__init__(master, **kwargs)

        # adding labels combobox and button
        self.tagLabel = customtkinter.CTkLabel(self,
                                               text="Sort by tag",
                                               text_color=light_pink,
                                               fg_color="transparent")
        self.tagLabel.grid(row=0, column=0, padx=20)

        self.tagCombobox = customtkinter.CTkComboBox(self,
                                                     values=tags,
                                                     fg_color=light_pink,
                                                     text_color=black,
                                                     dropdown_fg_color=light_pink,
                                                     dropdown_hover_color=dark_pink,
                                                     dropdown_text_color=black,
                                                     state="readonly",
                                                     command=self.refresh_tag_combobox)
        # FIXME this isn't running the function "refresh_tag_combobox"
        self.tagCombobox.grid(row=1, column=0, padx=10, pady=10)

        # buttons
        self.tagAddButton = customtkinter.CTkButton(self,
                                                    text="Add tag",
                                                    fg_color=light_pink,
                                                    text_color=black,
                                                    hover_color=dark_pink,
                                                    command=self.tag_dialogue_window)
        self.tagAddButton.grid(row=2, column=0, padx=20, pady=20)

        self.tagDeleteButton = customtkinter.CTkButton(self,
                                                       text="Delete tag",
                                                       fg_color=light_pink,
                                                       text_color=black,
                                                       hover_color=dark_pink,
                                                       command=self.delete_tag)
        self.tagDeleteButton.grid(row=3, column=0, padx=20, pady=20)
        self.delete_tag = None

        self.tagRenameButton = customtkinter.CTkButton(self,
                                                       text="Rename tag",
                                                       fg_color=light_pink,
                                                       text_color=black,
                                                       hover_color=dark_pink,
                                                       command=self.rename_tag)
        self.tagRenameButton.grid(row=4, column=0, padx=20, pady=20)
        self.rename_tag = None

class DeleteTag(customtkinter.CTkToplevel):

    def removal(self, name_of_tag):
        # remove from tags
        tags.remove(name_of_tag)
        self.destroy()

        # FIXME i need to update the combobox somehow too

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attributes('-topmost', 1)
        self.title("Delete Tag")
        self.geometry('%d+%d' % (
            get_x_coordinates(self.winfo_width(), self.winfo_screenwidth()),
            get_y_coordinates(self.winfo_height(), self.winfo_screenheight())
        ))

        labels = []
        buttons = []
        index = 0

        num_loops = 0
        r = 0
        c = 0

        if len(tags) != 0:

            for i in tags:
                # create labels and buttons
                self.button = customtkinter.CTkButton(self,
                                                      text=i,
                                                      fg_color=light_pink,
                                                      text_color=black,
                                                      hover_color=dark_pink,
                                                      command=lambda x=i: self.removal(x))
                buttons.append(self.button)
                buttons[index].grid(row=r, column=c, padx=20, pady=20)
                if c == 2:
                    c = 0
                    r += 1
                else:
                    c += 1
                num_loops += 1
                index += 1

        else:
            self.label = customtkinter.CTkLabel(self, text="There are no existing tags.")
            self.label.grid(row=0, column=0, padx=20, pady=20)


class RenameTag(customtkinter.CTkToplevel):

    def rename(self, name_of_tag):
        dialog = customtkinter.CTkInputDialog(text="Rename tag: ", title="Rename tag",
                                              button_fg_color=light_pink, button_text_color=black)
        new_tag = dialog.get_input()

        if check_exists(new_tag, tags, True) is True:
            tags.remove(name_of_tag)
            tags.append(new_tag)
            tags.sort()

        self.destroy()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attributes('-topmost', 1)
        self.title("Rename tag")
        self.geometry('%d+%d' % (
            get_x_coordinates(self.winfo_width(), self.winfo_screenwidth()),
            get_y_coordinates(self.winfo_height(), self.winfo_screenheight())
        ))

        buttons = []
        index = 0

        num_loops = 0
        r = 0
        c = 0

        if len(tags) != 0:

            for i in tags:
                # create labels and buttons
                self.button = customtkinter.CTkButton(self,
                                                      text=i,
                                                      fg_color=light_pink,
                                                      text_color=black,
                                                      hover_color=dark_pink,
                                                      command=lambda x=i: self.rename(x))
                buttons.append(self.button)

                # display labels and buttons
                buttons[index].grid(row=r, column=c, padx=20, pady=20)
                if c == 2:
                    c = 0
                    r += 1
                else:
                    c += 1
                num_loops += 1
                index += 1

        else:
            self.label = customtkinter.CTkLabel(self, text="There are no existing tags.")
            self.label.grid(row=0, column=0, padx=20, pady=20)
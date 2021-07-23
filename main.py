import json
import os
import tkinter as tk
import webbrowser as wb


class BookmarkLister(object):
    def __init__(self, window, user_data_path):
        with open(user_data_path, 'r') as data:
            self.user_data = json.load(data)
        self.user_data_path = user_data_path
        self.curr_selected_index = 0

        # Create the main entry, "Add", "Search", and "Delete" bookmarks buttons in a frame.
        controls_frame = tk.Frame(window)
        controls_frame.grid(row=0, column=0, columnspan=5)
        url_label = tk.Label(controls_frame, text="Bookmark")
        url_label.grid(row=0, column=0)
        self.url_entry = tk.Entry(controls_frame, text="Bookmark", width=40)
        self.url_entry.grid(row=0, column=1)
        add_btn = tk.Button(controls_frame, text="Add",
                            command=self.add_command)
        add_btn.grid(row=0, column=2)
        search_btn = tk.Button(
            controls_frame, text="Search", command=self.search_command)
        search_btn.grid(row=0, column=3)
        delete_btn = tk.Button(
            controls_frame, text="Delete", command=self.delete_command)
        delete_btn.grid(row=0, column=4)

        # Create the main listbox that displays a user's saved bookmarks
        bookmarks_list_frame = tk.Frame(window)
        bookmarks_list_frame.grid(row=2, column=0)
        self.bookmark_listbox = tk.Listbox(
            bookmarks_list_frame, width=80, height=20)
        self.bookmark_listbox.grid(row=0, column=0)
        self.bookmark_listbox.bind('<Double-1>', self.double_click_event)
        self.bookmark_listbox.bind(
            '<<ListboxSelect>>', self.get_selected_index)
        bookmark_xscroll = tk.Scrollbar(
            bookmarks_list_frame, orient="horizontal")
        bookmark_xscroll.grid(row=1, column=0)
        bookmark_yscroll = tk.Scrollbar(bookmarks_list_frame)
        bookmark_yscroll.grid(row=0, column=1, pady=20)
        self.bookmark_listbox.config(xscrollcommand=bookmark_xscroll.set,
                                     yscrollcommand=bookmark_yscroll.set)
        bookmark_xscroll.config(command=self.bookmark_listbox.xview)
        bookmark_yscroll.config(command=self.bookmark_listbox.yview)
        self.view_bookmarks()

    # Add the new url to the current bookmark_listbox and update the json file.
    def add_command(self):
        if len(self.url_entry.get()) > 0:
            self.user_data["bookmarks"].append(self.url_entry.get())
            self.url_entry.delete(0, tk.END)
            self.view_bookmarks()
            self.update_json_file()

    # Open the url in a new tab when it is double clicked from the bookmark_listbox.
    def double_click_event(self, event):
        url_index = self.bookmark_listbox.curselection()[0]
        if 'http://' in self.user_data["bookmarks"][url_index]:
            wb.get().open(self.user_data["bookmarks"][url_index])
        elif 'https://' in self.user_data["bookmarks"][url_index]:
            wb.get().open(self.user_data["bookmarks"][url_index])
        else:
            url = 'http://' + self.user_data["bookmarks"][url_index]
            wb.get().open(url)

    # Set curr_selected_index with the index value of the currently selected url.
    def get_selected_index(self, event):
        # print(self.bookmark_listbox.curselection()[0])
        self.curr_selected_index = self.bookmark_listbox.curselection()[0]

    # Fill the bookmark_listbox with bookmarks matching part or all of the string in the url_entry entry box.
    def search_command(self):
        self.bookmark_listbox.delete(0, tk.END)
        if len(self.url_entry.get()) == 0:
            self.view_bookmarks()
        else:
            for bookmark in self.user_data["bookmarks"]:
                if self.url_entry.get() in bookmark:
                    self.bookmark_listbox.insert(tk.END, bookmark)

    # Delete a bookmark from user_data variable and update the json file.
    def delete_command(self):
        if len(self.user_data["bookmarks"]) > 0:
            del self.user_data["bookmarks"][self.curr_selected_index]
            self.view_bookmarks()
            self.update_json_file()

    # Overwrite the json file with the new information in user_data
    def update_json_file(self):
        with open(self.user_data_path, 'w') as user_datajson:
            json.dump(self.user_data, user_datajson)

    # Inserts all of the bookmarks in user_data into the bookmark_listbox.
    def view_bookmarks(self):
        self.bookmark_listbox.delete(0, tk.END)
        for bookmark in self.user_data["bookmarks"]:
            self.bookmark_listbox.insert(tk.END, bookmark)


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Bookmark Lister")
    if not os.path.exists('bldata.json') and not os.access('bldata.json', os.R_OK):
        # BookmarkLister class can only work if there exists a dictionary with
        # a key of 'bookmarks' set to an array of empty value or containing strings of urls.
        data = {
            'bookmarks': []
        }
        with open('bldata.json', 'w') as user_data_json:
            json.dump(data, user_data_json)
    app = BookmarkLister(window, 'bldata.json')
    window.mainloop()

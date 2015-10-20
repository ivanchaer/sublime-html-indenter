import sublime, os, sys
import re

from .. import bs4
import bs4.builder._html5lib
print (bs4.builder.builder_registry.builders)

class DoIndent():

    def perform_replacement(self, view, edit):

        # define all the file as the region
        reg = sublime.Region(0, view.size())
        
        # get file contents
        file_str = view.substr(sublime.Region(0, view.size()))

        new_file_str = bs4.BeautifulSoup(file_str, "html.parser").prettify()

        if new_file_str != file_str:
            # replace old contents with new ones
            view.replace(edit, reg, new_file_str)
            print(view.file_name())



    def run(self, edit):

        # use this loop to indent all views on active window
        # for index, window_view in enumerate(sublime.active_window().views()):
        window_view = sublime.Window.active_view(sublime.active_window())
        self.perform_replacement(window_view, edit)

        
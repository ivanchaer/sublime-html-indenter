import sublime, os, sys
import re

from os.path import join
lib_path = join(sublime.packages_path(), 'indenter')
sys.path.append(lib_path)

from .. import bs4
import bs4.builder._html5lib


# Monkeypatch prettify_2space in place of prettify in the class. 
# Make the indent width a parameter.
orig_prettify = bs4.BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)
def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))
bs4.BeautifulSoup.prettify = prettify


class DoIndent():

    def indent(self, markup):

        # Double curly brackets to avoid problems with .format()
        stripped_markup = markup.replace('{','{{').replace('}','}}')

        stripped_markup = bs4.BeautifulSoup(stripped_markup, "html.parser")

        # Avoid breaking textareas and pre tags. 
        # Replace ['span', 'a'] with the tags on which you want to prevent indentation.
        unformatted_tag_list = []

        for i, tag in enumerate(stripped_markup.find_all(['span', 'a', 'p'])):
            unformatted_tag_list.append(str(tag))
            tag.replace_with('{' + 'unformatted_tag_list[{0}]'.format(i) + '}')

        pretty_markup = stripped_markup.prettify().format(unformatted_tag_list=unformatted_tag_list)

        return pretty_markup

    def perform_replacement(self, view, edit):

        # define all the file as the region
        reg = sublime.Region(0, view.size())
        
        # get file contents
        file_str = view.substr(sublime.Region(0, view.size()))

        new_file_str = self.indent(file_str)

        if new_file_str != file_str:
            # replace old contents with new ones
            view.replace(edit, reg, new_file_str)
            # print(view.file_name())



    def run(self, edit):

        # use this loop to indent all views on active window
        # for index, window_view in enumerate(sublime.active_window().views()):
        window_view = sublime.Window.active_view(sublime.active_window())
        self.perform_replacement(window_view, edit)

        
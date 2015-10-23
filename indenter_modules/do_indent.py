import sublime, os, sys
import re

from os.path import join
lib_path = join(sublime.packages_path(), 'indenter/indenter_modules')
sys.path.append(lib_path)

import bs4
import bs4.builder._html5lib

# Monkeypatch prettify_2space in place of prettify in the class. 
# Make the indent width a parameter.
# orig_prettify = bs4.BeautifulSoup.prettify
# r = re.compile(r'^(\s*)', re.MULTILINE)
# def prettify(self, encoding=None, formatter="minimal", indent_width=4):
#     string = orig_prettify(self, encoding, formatter)
#     lines = string.splitlines(True)
#     return '\n'.join([r.sub(r'\1' * indent_width, line) for line in lines])
# bs4.BeautifulSoup.prettify = prettify

indentations = re.compile(r'^(\s*)', re.MULTILINE)
indent_width = 4

def prettify(self, encoding=None, formatter="minimal"):
    if encoding is None:
        return self.decode(True, formatter=formatter)
    else:
        return self.encode(encoding, True, formatter=formatter)

class DoIndent():

    def indent(self, markup):

        soup = bs4.BeautifulSoup(markup, "html.parser")

        # Prevent indentation inside certain tags.
        unformatted_tag_list = []

        for i, tag in enumerate(soup.find_all(['span', 'a', 'strong', 'em', 'b', 'i', 'input', 'button', 'script', 'option', 'label', 'p', 'textarea', 'pre'])):
            
            unformatted_tag_list.append(str(tag))
            
            tag.replace_with('{' + 'unformatted_tag_list[{0}]'.format(i) + '}')

        pretty_markup = soup.prettify().format(unformatted_tag_list=unformatted_tag_list)

        pretty_markup = indentations.sub(r'\1' * indent_width, pretty_markup)

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

        
import sublime, sublime_plugin, sys, imp, os




# Make sure all dependencies are reloaded on upgrade
st_version = 2
if sublime.version() == '' or int(sublime.version()) > 3000:
  st_version = 3



class Indenter(sublime_plugin.TextCommand):

  def run(self, edit):

    reloader_name = 'indenter_modules.reloader'
    if st_version == 3:
      reloader_name = 'indenter.' + reloader_name
      from imp import reload

    if reloader_name in sys.modules:
      reload(sys.modules[reloader_name])

    from indenter.indenter_modules.do_indent import DoIndent

    try:
      # Python 3
      from indenter.indenter_modules.do_indent import DoIndent
      from indenter.indenter_modules import reloader
    except (ImportError):
      # Python 2
      from indenter_modules.do_indent import DoIndent
      import indenter_modules.reloader
    
   
    DoIndent().run(edit)
    
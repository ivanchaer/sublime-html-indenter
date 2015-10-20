import sublime
import sys
from imp import reload

reload_mods = []
for mod in sys.modules:
    if mod.startswith('indenter') and sys.modules[mod] != None:
        reload_mods.append(mod)


mod_prefix = 'indenter.indenter_modules'

mods_load_order = [
    '',

    '.replacements',
    '.do_indent'
]

for suffix in mods_load_order:
    mod = mod_prefix + suffix
    
    if mod in reload_mods:
        reload(sys.modules[mod])

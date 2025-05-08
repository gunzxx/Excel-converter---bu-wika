from function.core import importModules, uninstallModule, checkModules

modules = ['termcolor']
subModules = {}
sinonims = {}

# importModules(modules=modules, subModules=subModules, sinonims=sinonims)
checkModules(modules)
# uninstallModule('termcolor')
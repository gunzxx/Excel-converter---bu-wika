from subprocess import check_call, run, PIPE
from sys import executable

def importModules(modules:list[object], subModules: object={}, sinonims: object={}):
    for module in modules:
        if module in subModules:
            if module in sinonims:
                exec_stmt = f"from {module} import {subModules[module]} as {sinonims[module]}"
            else:
                exec_stmt = f"from {module} import {subModules[module]}"
        else:
            if module in sinonims:
                exec_stmt = f"import {module} as {sinonims[module]}"
            else:
                exec_stmt = f"import {module}"
        
        try:
            exec(exec_stmt, globals())
        except ImportError:
            print(f"Module {module} tidak ditemukan, menginstall...")
            installModule(module)
            print(f"Module {module} berhasil diinstall.")
            exec(exec_stmt, globals())

def installModule(module:str):
    try:
        check_call([executable, "-m", "pip", "install", module])
    except Exception as e:
        print(f"Gagal menginstall module '{module}'. \nError: {e}")

def uninstallModule(module:str):
    try:
        result = run([executable, "-m", "pip", "show", module], stdout= PIPE, stderr=PIPE)
        if result.returncode == 0:
            check_call([executable, "-m", "pip", "uninstall", "-y", module])
            print(f"Module '{module}' berhasil diuninstall.")
        else:
            print(f"Module {module} belum diinstall.")
    except Exception as e:
        print(f"Gagal menghapus module '{module}': {e}")

def checkModules(modules=[]):
    for module in modules:
        result = run([executable, "-m", "pip", "show", module], stdout= PIPE, stderr=PIPE)
        if result.returncode == 0:
            print(f"Module '{module}' terinstall \u2714")
        else:
            print(f"Module {module} belum diinstall. Menginstall module...")
            installModule(module)
        # try:
        #     __import__(module)
        # except ImportError:
        #     print(f"Module {module} belum diinstall. Menginstall module...")
        #     check_call([executable, "-m", "pip", "install", module])
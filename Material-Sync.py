from . import commands
from .lib import fusionAddInUtils as futil
from .config import MATERIAL_SYNC_FILE
import adsk.core, adsk.fusion
import threading, time, os
app = adsk.core.Application.get()

global thread_state

def run(context):
    try:
        global thread_state
        thread_state = True

        poll = threading.Thread(target=pollMaterialLibrary, daemon=True)
        poll.start()

        commands.start()

    except:
        futil.handle_error('run')

def stop(context):
    try:
        futil.clear_handlers()

        global thread_state
        thread_state = False

        commands.stop()

    except:
        futil.handle_error('stop')

def pollMaterialLibrary():
    local_mtime = os.stat(MATERIAL_SYNC_FILE).st_mtime
    global thread_state
    while thread_state is True:
        time.sleep(0.5)
        local_mtime = refreshMaterialLibrary(local_mtime)

def refreshMaterialLibrary(mtime: float):
    poll_mtime = os.stat(MATERIAL_SYNC_FILE).st_mtime
    if poll_mtime != mtime:
        material_library = app.materialLibraries.itemByName('Material-Sync')
        if material_library:
            _res = material_library.unload()
        material_library = app.materialLibraries.load(MATERIAL_SYNC_FILE)
    return poll_mtime
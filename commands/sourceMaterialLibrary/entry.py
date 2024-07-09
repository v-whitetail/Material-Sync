import adsk.core
import os, json, pathlib
from ...lib import fusionAddInUtils as futil
from ... import config
app = adsk.core.Application.get()
ui = app.userInterface


CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_cmdDialog'
CMD_NAME = 'Source Material Library'
CMD_Description = 'Find the Path to the Source Material Library'

IS_PROMOTED = True

WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_ID = 'SolidScriptsAddinsPanel'
COMMAND_BESIDE_ID = 'ScriptsManagerCommand'

ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

local_handlers = []

def start():
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)
    futil.add_handler(cmd_def.commandCreated, command_created)
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    control = panel.controls.addCommand(cmd_def, COMMAND_BESIDE_ID, False)
    control.isPromoted = IS_PROMOTED

def stop():
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)
    if command_control:
        command_control.deleteMe()
    if command_definition:
        command_definition.deleteMe()

def command_created(args: adsk.core.CommandCreatedEventArgs):
    futil.log(f'{CMD_NAME} Command Created Event')
    inputs = args.command.commandInputs

    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.inputChanged, command_input_changed, local_handlers=local_handlers)
    futil.add_handler(args.command.executePreview, command_preview, local_handlers=local_handlers)
    futil.add_handler(args.command.validateInputs, command_validate_input, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)

    _material_file_button = inputs.addBoolValueInput(
        'material_file_button_input',
        'Material File',
        False,
        os.path.join(ICON_FOLDER, 'button'),
        False,
    )
    _material_file_display = inputs.addTextBoxCommandInput(
        'material_file_display_input',
        'Selected File Path',
        config.MATERIAL_SYNC_FILE,
        1,
        True,
    )

def command_execute(args: adsk.core.CommandEventArgs):
    futil.log(f'{CMD_NAME} Command Execute Event')
    inputs = args.command.commandInputs

def command_preview(args: adsk.core.CommandEventArgs):
    futil.log(f'{CMD_NAME} Command Preview Event')
    inputs = args.command.commandInputs

def command_input_changed(args: adsk.core.InputChangedEventArgs):
    changed_input = args.input
    inputs = args.inputs

    if changed_input.id == 'material_file_button_input':
        material_file_dialog = ui.createFileDialog()
        material_file_dialog.filter = '*.adsklib'
        material_file_dialog.title = 'Select Material Library'
        material_file_dialog.isMultiSelectEnabled = False
        material_file_dialog.initialDirectory = os.path.join(os.path.abspath(pathlib.Path.home()), 'Desktop')
        if material_file_dialog.showOpen() == adsk.core.DialogResults.DialogOK:
            material_file = adsk.core.TextBoxCommandInput.cast(args.inputs.itemById('material_file_display_input'))
            material_file.formattedText = material_file_dialog.filename
            with open(config.LOCAL_CONFIG, 'wt+') as local_config:
                file_content = {'filepath': material_file_dialog.filename}
                json.dump(file_content, local_config)
                config.MATERIAL_SYNC_FILE = material_file_dialog.filename

def command_validate_input(args: adsk.core.ValidateInputsEventArgs):
    futil.log(f'{CMD_NAME} Validate Input Event')
    inputs = args.inputs

def command_destroy(args: adsk.core.CommandEventArgs):
    futil.log(f'{CMD_NAME} Command Destroy Event')
    global local_handlers
    local_handlers = []

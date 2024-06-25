import ipywidgets as widgets
from IPython.display import display, clear_output
from app.contract_utils import highlight_changes
from app.openai_setup import update_contract

# Function to approve contract
def approve_contract(b):
    with output:
        clear_output()
        output.append_stdout("Contract approved and finalized.\n")
        approved_textarea.value = edit_textarea.value

# Function to edit contract
def edit_contract(b):
    with output:
        clear_output()
        output.append_stdout("Please edit the updated contract manually.\n")
        edit_textarea.value = updated_textarea.value

# Function to handle contract update based on user input
def handle_update_contract(b):
    instructions = instructions_textarea.value
    updated_contract = update_contract(original_contract, instructions)
    highlighted_contract = highlight_changes(original_contract, updated_contract)
    updated_textarea.value = updated_contract
    updated_html.value = highlighted_contract
    with output:
        clear_output()
        output.append_stdout("Contract has been updated based on the provided instructions.\n")

# Function to save manually edited contract
def save_edits(b):
    with output:
        clear_output()
        output.append_stdout("Manual edits have been saved.\n")

def display_ui():
    global updated_contract

    header = widgets.HTML("<h2>Contract Modification Assistant</h2>")
    instructions_label = widgets.HTML("<b>Instructions:</b> Provide detailed instructions to modify the contract below.")
    instructions_textarea = widgets.Textarea(placeholder='Enter instructions here...', layout=widgets.Layout(width='100%', height='150px'))

    original_label = widgets.HTML("<b>Original Contract:</b>")
    original_textarea = widgets.Textarea(value=original_contract, layout=widgets.Layout(width='100%', height='150px'), disabled=True)

    update_button = widgets.Button(description="Update Contract", button_style='primary')
    update_button.on_click(handle_update_contract)

    updated_label = widgets.HTML("<b>Updated Contract:</b>")
    updated_textarea = widgets.Textarea(layout=widgets.Layout(width='100%', height='150px'), disabled=True)

    updated_html = widgets.HTML()

    approval_button = widgets.Button(description="Approve", button_style='success')
    edit_button = widgets.Button(description="Edit Manually", button_style='warning')
    save_edits_button = widgets.Button(description="Save Edits", button_style='info')

    approval_button.on_click(approve_contract)
    edit_button.on_click(edit_contract)
    save_edits_button.on_click(save_edits)

    approved_label = widgets.HTML("<b>Approved Contract after Editing:</b>")
    approved_textarea = widgets.Textarea(layout=widgets.Layout(width='100%', height='150px'), disabled=True)

    edit_label = widgets.HTML("<b>Edited Contract:</b>")
    edit_textarea = widgets.Textarea(layout=widgets.Layout(width='100%', height='150px'))

    output = widgets.Output()

    layout = widgets.VBox([
        header,
        widgets.VBox([
            instructions_label,
            instructions_textarea,
            original_label,
            original_textarea,
            update_button,
            updated_label,
            updated_textarea,
            updated_html,
            widgets.HBox([edit_button, save_edits_button, approval_button]),
            output,
            approved_label,
            approved_textarea,
            edit_label,
            edit_textarea
        ], layout=widgets.Layout(border='1px solid lightgray', padding='10px', border_radius='10px'))
    ])

    display(layout)

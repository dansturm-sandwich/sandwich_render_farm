import nuke
import os
from datetime import datetime
import re

def sandwich_render_panel():
    # Create a new panel
    panel = nuke.Panel('Sandwich Render')

    now = datetime.now()

    date_time_stamp = now.strftime("%d%m%y_%H%M%S")

    script_path = nuke.root().name()
    try:
        script_path = re.sub(r'^.*(?=\/Volumes\/sandwich-post)', '', script_path)
    except:
        pass
    script_name = os.path.basename(script_path)
    script_name = os.path.splitext(script_name)[0]

    first_frame = nuke.root().firstFrame()
    last_frame = nuke.root().lastFrame()

    # Retrieve all write nodes in the script
    write_nodes = [node.name() for node in nuke.allNodes('Write')]

    # Add text input fields, with the current first and last frames as default values
    panel.addSingleLineInput('first frame', first_frame)
    panel.addSingleLineInput('last frame', last_frame)

    # Add a dropdown list to the panel with the names of the write nodes
    panel.addEnumerationPulldown('Write Node', ' '.join(write_nodes))

    # Add a checkbox to the panel
    panel.addBooleanCheckBox('Render All (Enabled)', False)

    panel.addNotepad('Submission Note', '')

    # Add the 'OK' and 'Cancel' buttons. The panel will return True if 'OK' is pressed.
    result = panel.show()

    if result:  # If the user presses 'OK'
        # Retrieve values from the panel
        first_frame_input = panel.value('first frame')
        last_frame_input = panel.value('last frame')
        submission_note_input = panel.value('Submission Note')
        selected_write_node = panel.value('Write Node')
        render_all_active = panel.value('Render All (Enabled)')


        try:
            # Convert the input to integers
            first_frame_input = int(first_frame_input)
            last_frame_input = int(last_frame_input)

            submission_details = f'{script_path}\n{first_frame_input}\n{last_frame_input}\n{script_name}\nrender all:\n{render_all_active}\n{selected_write_node}\n{submission_note_input}'

            file_path = f'/Volumes/sandwich-post/assets/render_queue/{script_name}_{date_time_stamp}.txt'
            with open(file_path, 'w') as file:
                file.write(submission_details)

            
            # Do something with the frame range values...
            nuke.message(f"Render Submitted")
        except ValueError:
            # Handle the case where the input is not a valid integer
            nuke.message("Please enter valid integer values for the frame range.")

# Run the panel function
# sandwich_render_panel()
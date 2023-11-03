from datetime import datetime

now = datetime.now()

date_time_stamp = now.strftime("%d%m%y_%H%M%S")

script_path = nuke.root().name()
script_name = os.path.basename(script_path)
script_name = os.path.splitext(script_name)[0]
first_frame = nuke.root().firstFrame()
last_frame = nuke.root().lastFrame()

submission_details = f'{script_path}\n{first_frame}\n{last_frame}'

file_path = f'/Volumes/sandwich-post/assets/render_queue/{script_name}_{date_time_stamp}.txt'
with open(file_path, 'w') as file:
    file.write(submission_details)

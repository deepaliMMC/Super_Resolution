
import subprocess
from fastapi import FastAPI, HTTPException
print('oyoyoyoyoy')

def run_srgan():
    # Extract data from request
    mode = "test_only"
    generator_path = "pretrained_models/SRGAN.pt"
    LR_path = "test_data"
    # Build command
    # print('oyo')
    command = f"python main.py --mode {mode} --LR_path {LR_path} --generator_path {generator_path}"
    print('oyoyo')
    try:
        # Execute command and capture output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = "Superresolution done"
        print("aaaaaaaaaaaaaaaaaa")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# print('run1')
run_srgan()
# print('complete')


#APPROVED!

#
# import subprocess
# from fastapi import FastAPI, HTTPException
# import os
# import shutil
#
# def run_srgan():
#     mode = "test_only"
#     generator_path = "pretrained_models/SRGAN.pt"
#     LR_folder = "test_data"
#     temp_folder = "test_patch_data"
#
#     # Ensure temp_folder is empty and exists
#     if not os.path.exists(temp_folder):
#         os.makedirs(temp_folder)
#     else:
#         # Clear the directory
#         for f in os.listdir(temp_folder):
#             os.remove(os.path.join(temp_folder, f))
#
#     files = sorted(os.listdir(LR_folder), key=lambda x: int(x.split('_')[1].split('.')[0]))
#
#     for file in files:
#         # Move file to temporary directory
#         src_path = os.path.join(LR_folder, file)
#         dest_path = os.path.join(temp_folder, file)
#         shutil.copy(src_path, dest_path)
#
#         # Build the command with the temporary directory
#         command = f"python main.py --mode {mode} --LR_path {temp_folder} --generator_path {generator_path}"
#
#         try:
#             # Execute command and capture output
#             result = subprocess.run(command, shell=True, capture_output=True, text=True)
#             if result.returncode != 0:
#                 raise Exception(f"Error in processing {file}: {result.stderr}")
#             print(f"Superresolution completed for {file}")
#
#             original_file_path = 'result/res_%04d.png'
#             if os.path.exists(original_file_path):
#                 # Define the new file name and path
#                 new_file_name = f"renamed_{file}"
#                 new_file_path = os.path.join('result', new_file_name)
#
#                 # Rename the file
#                 os.rename(original_file_path, new_file_path)
#
#                 # Assign the new file path to a variable
#                 renamed_file_path = new_file_path
#                 print(f"File has been renamed to: {renamed_file_path}")
#
#
#
#             # Remove the processed file from the temporary directory
#             os.remove(dest_path)
#
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=str(e))
#
# # Run the super resolution process
# run_srgan()
#
#
# import os
#
# # Path to the folder containing the images
# folder_path = '/Users/mihir/Desktop/chot/SRG/result'
#
# # List all files in the folder
# files = os.listdir(folder_path)
#
# # Sort the files to ensure the correct order
# files.sort()
#
# # Iterate over the files and rename them
# for index, file_name in enumerate(files):
#     # Construct the new file name
#     new_name = f"res_{index:04}.tif"
#
#     # Get the full path to the current file and the new file
#     old_file_path = os.path.join(folder_path, file_name)
#     new_file_path = os.path.join(folder_path, new_name)
#
#     # Rename the file
#     os.rename(old_file_path, new_file_path)
#     print(f"Renamed {file_name} to {new_name}")
#
# print("All files have been renamed.")

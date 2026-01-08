import os
import shutil

class MoveVHSVideo:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "filenames": ("VHS_FILENAMES",),
                "destination_path": ("STRING", {"default": "./moved_videos", "multiline": False}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "move_files"
    OUTPUT_NODE = True
    CATEGORY = "utils"

    def move_files(self, filenames, destination_path):
        # Resolve path relative to CWD if it's not absolute
        dest_dir = os.path.abspath(destination_path)

        # Ensure destination directory exists
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir)
            except OSError as e:
                print(f"Error creating directory {dest_dir}: {e}")
                return ()

        # Handle different potential input structures for VHS_FILENAMES
        file_list = []
        if isinstance(filenames, dict) and 'filenames' in filenames:
            file_list = filenames['filenames']
        elif isinstance(filenames, (list, tuple)):
            file_list = filenames
        else:
            print(f"Unexpected input type for filenames: {type(filenames)}")
            return ()
        
        for file_path in file_list:
            if os.path.exists(file_path):
                file_name = os.path.basename(file_path)
                new_path = os.path.join(dest_dir, file_name)
                
                try:
                    # If destination file exists, we remove it to allow overwrite
                    # standard shutil.move behavior on some platforms with existing files can be tricky
                    if os.path.exists(new_path):
                        os.remove(new_path)
                    
                    shutil.move(file_path, new_path)
                    print(f"Moved {file_path} to {new_path}")
                except Exception as e:
                    print(f"Error moving {file_path}: {e}")
            else:
                print(f"Source file not found: {file_path}")

        return ()

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
                "rename_video": ("STRING", {"default": "", "multiline": False}),
                "copy_video_with_audio": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "move_files"
    OUTPUT_NODE = True
    CATEGORY = "utils"

    def move_files(self, filenames, destination_path, rename_video="", copy_video_with_audio=False):
        # Resolve path relative to CWD if it's not absolute
        dest_dir = os.path.abspath(destination_path)

        # Ensure destination directory exists
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir)
            except OSError as e:
                print(f"Error creating directory {dest_dir}: {e}")
                return ()

        # Helper function to extract strings from nested structures
        def get_all_strings(data):
            strings = []
            if isinstance(data, (list, tuple)):
                for item in data:
                    strings.extend(get_all_strings(item))
            elif isinstance(data, dict):
                 # Handle dicts if they occur, e.g. {'filenames': [...]}
                 for value in data.values():
                     strings.extend(get_all_strings(value))
            elif isinstance(data, str):
                strings.append(data)
            return strings

        # Extract only file paths (strings) from the input
        # usage: filenames input might be (['path/to/video.mp4'], True) or similar
        file_list = get_all_strings(filenames)
        
        for file_path in file_list:
            if not os.path.exists(file_path):
                print(f"Source file not found: {file_path}")
                continue

            file_name = os.path.basename(file_path)
            _, ext = os.path.splitext(file_name)

            # Ignore .png files
            if ext.lower() == '.png':
                continue

            # Logic for filtering .mp4 files based on audio toggle
            if ext.lower() == '.mp4':
                has_audio_in_name = 'audio' in file_name.lower()
                
                if copy_video_with_audio:
                    # We want audio, so skip if it doesn't have it
                    if not has_audio_in_name:
                        continue
                else:
                    # We do NOT want audio, so skip if it HAS it
                    if has_audio_in_name:
                        continue
            
            # Handle renaming if rename_video string is provided
            if rename_video.strip():
                # If processing multiple files, this simple rename will overwrite subsequent ones
                # unless we assume only one file is expected or user handles it.
                # Per instructions: "renamed to this name", "extension is not affected".
                file_name = rename_video + ext

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

        return ()

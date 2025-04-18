import os
import subprocess

def unpack_firmware(save_path):
    for root, _, files in os.walk(save_path):
        for file in files:
            if file.endswith('.zip'):  # Only process zip files
                file_path = os.path.join(root, file)
                try:
                    # Create an extraction directory
                    extract_dir = os.path.join(save_path, os.path.splitext(file)[0] + "_extracted")
                    os.makedirs(extract_dir, exist_ok=True)
                    
                    # Modified command to use the extract directory
                    command = ['binwalk', '-e', file_path, '--directory', extract_dir]
                    subprocess.run(command, check=True)
                    print(f"Unpacked file using binwalk: {file_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to unpack file {file_path} using binwalk: {e}")


if __name__ == '__main__':
    save_path = "../fws"
    unpack_firmware(save_path)

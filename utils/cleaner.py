import os

from utils.debugger import logger

def delete_files(folder_path: str) -> None:
    files = os.listdir(folder_path)

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        try:
            os.remove(file_path)
        except Exception as e:
            logger.exception(f"Error deleting {file_path}: {e}")

if __name__ == '__main__':
    delete_files('data/txt_papers')
    delete_files('data/txt_parsed_papers')
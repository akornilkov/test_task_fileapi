import os
from pathlib import Path
from fileapi.app.config import config


def split_path(path: str):
    result = Path(path)
    return result.parent, result.name


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def find_file_paths(file: dict = None, search_path: str = config.FILES_BASE_PATH):
    result = []
    if filename := file.get('name', ''):
        if search_path:
            for root, dir, files in os.walk(search_path, topdown=True):
                if filename in files:
                    result.append(os.path.join(root, filename))
    return result


def create_dir_if_not_exists(path: str = None):
    if path:
        new_path = Path(path)
        if not new_path.exists():
            new_path.mkdir(parents=True, exist_ok=True)


def move_file(file: dict = None, new_path: str = None):
    if file:
        old_path = file.get('loaded_to', '')
        if new_path and old_path:
            create_dir_if_not_exists(new_path)
            file_to_move = Path(file.get('loaded_to', ''))
            if file_to_move.exists() and file_to_move.is_file():
                os.replace(old_path, f'{new_path}{file_to_move.name}')
                file.update({'loaded_to': f'{new_path}{file_to_move.name}'})
    return file


def delete_file(file: dict = None):
    if file:
        if loaded_to := file.get('loaded_to', ''):
            rmpath = Path(loaded_to)
            if rmpath.exists() and rmpath.is_file():
                os.remove(loaded_to)
                return True
    return False


def rename_file(file: dict = None, new_name: str = None):
    if file:
        if loaded_to := file.get('loaded_to', ''):
            path = Path(loaded_to)
            if path.exists() and path.is_file():
                os.rename(file.get('loaded_to'), f'{path.parent}/{new_name}')
                return True
    return False


def copy_file(file: dict = None):
    pass


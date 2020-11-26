from fileapi.api.controllers.filemanager import create_dir_if_not_exists
from fileapi.app.config import config

create_dir_if_not_exists(config.FILES_BASE_PATH)
create_dir_if_not_exists(config.UPLOAD_FOLDER)

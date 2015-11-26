import tempfile

import config


def generate_temp_file_path():
    indx, tmp_file = tempfile.mkstemp(suffix='.json', dir=config.TEMP_FILE_PATH)
    return tmp_file

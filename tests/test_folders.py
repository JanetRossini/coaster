import os.path

from modules.utils import coaster_base_path, coaster_data_in_path, coaster_objects_in_path, coaster_scripts_out_path


class TestFolders:
    def test_coaster_path_exists(self):
        path = coaster_base_path()
        exists = os.path.isdir(path)
        assert exists, "folder 'coaster' not found"

    def test_data_in_path_exists(self):
        path = coaster_data_in_path()
        exists = os.path.isdir(path)
        assert exists, "folder 'coaster/data-in' not found""folder 'coaster' not found"

    def test_objects_in_path_exists(self):
        path = coaster_objects_in_path()
        exists = os.path.isdir(path)
        assert exists, "folder 'coaster/objects-in' not found"

    def test_scripts_out_path_exists(self):
        path = coaster_scripts_out_path()
        exists = os.path.isdir(path)
        assert exists, "folder 'coaster/scripts-out' not found"




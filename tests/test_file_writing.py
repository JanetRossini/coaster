import os
from modules.v_mathutils import VtVector
from modules.vtfilewriter import VtFileWriter

program = """
// this is a comment
list vecdata = [
$lines
];

do_something() {
    llSay(0,"doing something");
}
"""


def make_pairs(items):
    return [items[i:i + 2] for i in range(0, len(items)-1, 2)]


class TestFileWriting:
    lines = ["line1", "line2", "line3"]

    def test_interpolation(self):
        pass
        # formatted = program.format(lines)
        # print(formatted)
        # assert formatted == ""

    def test_too_simple(self):
        not_what_we_want = "{0}".format(self.lines)
        assert not_what_we_want == "['line1', 'line2', 'line3']"

    def test_join(self):
        insert = "\n,".join(self.lines)
        result = "list vecdata = [\n{0}\n];".format(insert)
        assert result == 'list vecdata = [\nline1\n,line2\n,line3\n];'

    def test_template(self):
        insert = "\n,".join(self.lines)
        from string import Template
        program = "list vecdata = [\n$lines\n];"
        expected = "list vecdata = [\nline1\n,line2\n,line3\n];"
        template = Template(program)
        result = template.substitute(lines=insert)
        print(result)
        assert result == expected

    def test_join_again(self):
        file_track05 = 'C:/mumble/track.blend'
        inner_track05 = 'Object'
        object_track05 = 'track'
        filepath = os.path.join(file_track05, inner_track05, object_track05)
        path_mac = 'C:/mumble/track.blend/Object/track'
        filepath = filepath.replace('\\', '/')
        assert filepath == path_mac
        directory = os.path.join(file_track05, inner_track05)
        directory = directory.replace('\\', '/')
        dir_mac = 'C:/mumble/track.blend/Object'
        assert directory == dir_mac

    def test_we_can_compute_wm_elements(self):
        def bpy_ops_wm_append(filepath, directory, filename):
            pass

        def make_elements(name):
            working = os.getcwd()  # comment next line, should still work for DS
            working = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects'
            filepath = os.path.join(working, name + '.blend')
            directory = os.path.join(filepath, 'Object')
            filename = object_track
            return filepath, directory, filename

        file_track_mac = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/track.blend'
        inner_track = 'Object'
        object_track = 'track'
        filepath, directory, filename = make_elements('track')
        filepath = filepath.replace('\\', '/')
        assert filepath == file_track_mac
        dir_mac = filepath + '/' + inner_track
        directory = directory.replace('\\', '/')
        assert directory == dir_mac
        assert filename == 'track'
        # just to show how we use it:
        # bpy.ops.wm.append(
        bpy_ops_wm_append(
            filepath=filepath,
            directory=directory,
            filename=filename
        )

    def test_home(self):
        home = os.path.expanduser('~')
        print(home)
        # assert False

    def test_make_lines_rel_flat(self):
        back = VtVector((2, 2, 2))
        front = VtVector((3, 2, 2))
        up = VtVector((2, 3, 3))
        coords = [(back, up, front)]
        lines = VtFileWriter.make_lines(coords, False, False)
        assert lines[0] == '<0.000, 0.000, 0.000, 0>'

    def test_make_lines_rel_bank(self):
        back = VtVector((2, 2, 2))
        front = VtVector((3, 2, 2))
        up = VtVector((2, 3, 3))
        coords = [(back, up, front)]
        lines = VtFileWriter.make_lines(coords, False, True)
        assert lines[0] == '<0.000, 0.000, 0.000, 45>'

    def test_make_lines_abs_bank(self):
        back = VtVector((2, 2, 2))
        front = VtVector((3, 2, 2))
        up = VtVector((2, 3, 3))
        coords = [(back, up, front)]
        lines = VtFileWriter.make_lines(coords, True, True)
        assert lines[0] == '<2.000, 2.000, 2.000, 45>'

    def test_make_lines_abs_flat(self):
        back = VtVector((2, 2, 2))
        front = VtVector((3, 2, 2))
        up = VtVector((2, 3, 3))
        coords = [(back, up, front)]
        lines = VtFileWriter.make_lines(coords, True, False)
        assert lines[0] == '<2.000, 2.000, 2.000, 0>'

    def test_slicing(self):
        lis = [1, 2, 3, 4, 5, 6, 7]
        pairs = [lis[i:i+2] for i in range(0, len(lis), 2)]
        assert len(pairs[-2]) == 2
        assert len(pairs[-1]) == 1

    def test_make_pairs(self):
        items = [1, 2, 3, 4, 5, 6]
        assert len(make_pairs(items)) == 3
        items = [1, 2, 3, 4, 5, 6, 7]
        assert len(make_pairs(items)) == 3
        items = [1, 2, 3, 4, 5, 6, 7, 8]
        assert len(make_pairs(items)) == 4

    def test_make_filepath_directory_name(self):
        file_path = 'C:/mumble/foo/fragglerats.blend'
        path, file = os.path.split(file_path)
        assert file == 'fragglerats.blend'
        name, ext = os.path.splitext(file)
        assert name == 'fragglerats'
        assert ext == '.blend'
        directory = os.path.join(file_path, 'Object')
        assert directory == 'C:/mumble/foo/fragglerats.blend/Object'

    def test_get_data_path(self):
        import sys
        def running_as_add_on():
            return __name__ in sys.modules

        def data_path(is_add_on):
            if is_add_on:
                return ''
            else:
                return ''

        assert 2 == 2


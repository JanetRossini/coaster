import os

import pytest
from mathutils import Vector

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
        file_track05 = 'C:/mumble/track05.blend'
        inner_track05 = 'Object'
        object_track05 = 'track05'
        filepath=os.path.join(file_track05, inner_track05, object_track05)
        assert filepath == 'C:/mumble/track05.blend/Object/track05'
        directory=os.path.join(file_track05, inner_track05)
        assert directory == 'C:/mumble/track05.blend/Object'

    def test_pathlib(self):
        from pathlib import Path
        home = Path.home()
        home_file = home / 'HOME_DIR.txt'  # this file has my absolute path in it
        with home_file.open() as h:
            home_dir = h.readline().strip()
        assert str(home) == home_dir
        assert str(Path.cwd()) == home_dir + '/PycharmProjects/coaster'
        p = Path('test_file_writing.py')
        assert str(p.absolute()) == str(Path.cwd()) + '/test_file_writing.py'
        q = p.with_name('notes.md')
        assert str(q.absolute()) == str(Path.cwd()) + '/notes.md'

    def test_we_can_compute_wm_elements(self):
        def bpy_ops_wm_append(filepath, directory, filename):
            pass

        def make_elements(name):
            working = os.getcwd()  # comment next line, should still work for DS
            working = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects'
            filepath = os.path.join(working, name + '.blend')
            directory = os.path.join(filepath, 'Object')
            filename = object_track05
            return filepath, directory, filename

        file_track05 = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/track05.blend'
        inner_track05 = 'Object'
        object_track05 = 'track05'
        filepath, directory, filename = make_elements('track05')
        assert filepath == file_track05
        assert directory == file_track05 + '/' + inner_track05
        assert filename == 'track05'
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

    def test_get_line_data_rel_bank(self):
        absolute = False
        if absolute:
            back_zero = Vector((0, 0, 0))
        else:
            back_zero = Vector((1, 2, 2))
        bank = True
        back = Vector((2, 2, 2))
        front = Vector((3, 2, 2))
        up = Vector((2, 3, 3))
        bz, roll = VtFileWriter.get_line_data(back, up, front, back_zero, bank)
        assert roll == pytest.approx(45.0)
        assert bz.x == pytest.approx(1.0)
        assert bz.y == pytest.approx(0.0)
        assert bz.z == pytest.approx(0.0)

    def test_get_line_data_abs_bank(self):
        absolute = True
        if absolute:
            back_zero = Vector((0, 0, 0))
        else:
            back_zero = Vector((1, 2, 2))
        bank = True
        back = Vector((2, 2, 2))
        front = Vector((3, 2, 2))
        up = Vector((2, 3, 3))
        bz, roll = VtFileWriter.get_line_data(back, up, front, back_zero, bank)
        assert roll == pytest.approx(45.0)
        assert bz.x == pytest.approx(2.0)
        assert bz.y == pytest.approx(2.0)
        assert bz.z == pytest.approx(2.0)

    def test_get_line_data_abs_flat(self):
        absolute = True
        if absolute:
            back_zero = Vector((0, 0, 0))
        else:
            back_zero = Vector((1, 2, 2))
        bank = False
        back = Vector((2, 2, 2))
        front = Vector((3, 2, 2))
        up = Vector((2, 3, 3))
        bz, roll = VtFileWriter.get_line_data(back, up, front, back_zero, bank)
        assert roll == pytest.approx(0.0)
        assert bz.x == pytest.approx(2.0)
        assert bz.y == pytest.approx(2.0)
        assert bz.z == pytest.approx(2.0)

    def test_get_line_data_rel_flat(self):
        absolute = False
        if absolute:
            back_zero = Vector((0, 0, 0))
        else:
            back_zero = Vector((1, 2, 2))
        bank = False
        back = Vector((2, 2, 2))
        front = Vector((3, 2, 2))
        up = Vector((2, 3, 3))
        bz, roll = VtFileWriter.get_line_data(back, up, front, back_zero, bank)
        assert roll == pytest.approx(0.0)
        assert bz.x == pytest.approx(1.0)
        assert bz.y == pytest.approx(0.0)
        assert bz.z == pytest.approx(0.0)

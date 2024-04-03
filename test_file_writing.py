import os

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

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

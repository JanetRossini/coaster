import os
from math import ceil
from vehicle import Vehicle


class VtFileWriter:
    def __init__(self, vertices, path, base_name, size):
        self.vertices = vertices
        self.path = path
        self.base_name = base_name
        self.size = size

    def write_files(self):
        coords = tuple(v.co for v in self.vertices)
        triples = tuple(coords[i:i + 3] for i in range(0, len(coords) - 1, 2))
        all_lines = self.make_lines(triples)
        count = ceil(len(triples)/self.size)
        for file_number in range(count):
            start = file_number*self.size
            end = (file_number+1)*self.size
            lines = all_lines[start:end]
            name = [self.base_name, str(file_number)]
            file_name = "_".join(name) + ".lsl"
            full_path = os.path.join(self.path, file_name)
            with open(full_path, "w") as file:
                self.write_one_file(file_name, file_number, count, lines, file)
                print(f"File was written to {full_path}\n")

    def write_one_file(self, file_name, file_number, file_count, lines, file):
        from datetime import datetime
        now = datetime.now()
        file.write(f"// {file_name}\n")
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"// {time}\n")
        file.write("//    created by VtFileWriter\n")
        file.write("//    JR 20240115 - inert, last sends LOADING_DONE\n")
        file.write("//    Script names do not matter.\n\n")
        file.write(f"integer SCRIPT_NUMBER = {file_number};\n")
        file.write(f"integer LAST_SCRIPT_NUMBER= {file_count-1};\n")
        file.write(f"integer CHUNK_SIZE = {self.size};\n\n")
        file.write("list data = [\n")
        text = "\n,".join(lines)
        file.write(text)
        file.write("\n];\n")
        file.write(self.fixed_part)

    @staticmethod
    def make_lines(coordinate_triples):
        lines = []
        back_zero = coordinate_triples[0][0]
        for back, up, front in coordinate_triples:
            back_zeroed = back - back_zero
            roll = Vehicle(back, up, front).roll_degrees()
            output = f"<{back_zeroed.x:.3f}, {back_zeroed.y:.3f}, {back_zeroed.z:.3f}, {roll:.0f}>"
            lines.append(output)
        return lines

    fixed_part = """
// nothing varies from here on down

write_data() {
    integer limit = llGetListLength(data);
    integer out_key = CHUNK_SIZE*SCRIPT_NUMBER;
    integer end_key = out_key + limit;
    // llSay(0, llGetScriptName() + " writing " + (string) out_key + " up to " + (string) end_key);
    integer index;
    for (index = 0; index < limit; index++, out_key++) {
        llLinksetDataWrite("datakey"+(string) out_key,  llList2String( data , index));
    }
    if (SCRIPT_NUMBER == LAST_SCRIPT_NUMBER) {
        integer keyCount = llLinksetDataCountKeys(); 
        // llSay(0, "SIGNALLING LOADING_DONE " + (string) keyCount);
        llMessageLinked(LINK_THIS, keyCount, "LOADING_DONE", NULL_KEY);
    } else {
        llMessageLinked(LINK_THIS, SCRIPT_NUMBER + 1, "LOADING", NULL_KEY);
    }
}

default {
    on_rez(integer start_param) {
        llResetScript();
    }

    state_entry() {
    }

    link_message(integer sender_num, integer num, string str, key id) {
        if (str != "LOADING") return;
        if (num != SCRIPT_NUMBER) return;
        if (SCRIPT_NUMBER == 0) {
            llLinksetDataReset();
            // llSay(0, "SCRIPT 0 Resetting LSD");
        }
        write_data();
    }
}
"""

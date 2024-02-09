import os

from dizzi_blender import Vehicle


class Operator:
    pass


class RCG_OT_Exp_Banked_path(Operator):
    """ Set the render properties """
    bl_idname = "rcg.expbank"
    bl_label = "Export Banked Path Script"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        # Put code here
        obj = bpy.context.object

        if obj is None or obj.type != "MESH":
            return

        # Output geometry
        obj_eval = obj.evaluated_get(bpy.context.view_layer.depsgraph)
        filepath = "C:/Users/Terry/PycharmProjects/blenderPython/verticesbanked.lsl"

        verts = obj_eval.data.vertices
        self.write_files(verts, filepath)

        return {'FINISHED'}

    def write_files(self, verts, filepath):
        triples = [verts[i:i + 3] for i in range(0, len(verts) - 1, 2)]
        self.write_triples(triples, filepath)

    def write_triples(self, triples, filepath):
        with open(filepath, "w") as file:
            file.write("list vectdata = [\n")
            back_0 = triples[0][0].co
            comma = ""
            for back_vertex, up_vertex, front_vertex in triples:
                back = back_vertex.co
                up = up_vertex.co
                front = front_vertex.co
                back_zeroed = back - back_0
                roll = Vehicle(back, up, front).roll_degrees()
                output = f"{comma}<{back_zeroed.x:.3f}, {back_zeroed.y:.3f}, {back_zeroed.z:.3f}, {roll:.0f}>\n"
                file.write(output)
                print(output)
                comma = ","
            print(f"File was written to {os.path.join(os.getcwd(), filepath)}\n")
            file.write("];\n")
            file.write("\n")
            file.write("default\n")
            file.write("{\n")
            file.write("  state_entry()\n")
            file.write("  {\n")
            file.write("    integer length = llGetListLength(vectdata);\n")
            file.write("    llLinksetDataReset();\n")
            file.write("    integer a = 0;\n")
            file.write("    integer b = length;\n")
            file.write("    for(; a < b; ++a) {\n")
            file.write('      llLinksetDataWrite("datakey"+(string)a,  llList2String( vectdata , a) );\n')
            file.write("    }\n")
            file.write("  }\n")
            file.write("}\n")

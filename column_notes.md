# Column Notes

## 20240419_0700 JR

In about four steps, I have a column operator that has a header 
item in the menu, a button for Column, and that displays 
"Column coming soon" as an INFO message. Basically copied 
addnurbscurve or something.

I think I could add a cylinder wherever the cursor is, and I might 
do that. First, I'm going to look at the export and see how it 
finds the stuff to export.

In the export it does this:

~~~
obj_eval = obj.evaluated_get(bpy.context.view_layer.depsgraph)
~~~

I'm not sure what that is, and suspect I need to know. I'll just 
add a column and see what I can see. 

## 20240420_0815 JR

We have this to add a column at the origin:

~~~python
    def execute(self, context):
        height = 4.0
        bpy.ops.mesh.primitive_cylinder_add(
            location=(0.0, 0.0, height/2),
            vertices=3,
            end_fill_type='NOTHING',
            enter_editmode=False)
        ob = bpy.context.object
        x, y, _old_z = ob.dimensions
        ob.dimensions = [x, y, height]
        # self.report({"INFO"}, "Column set dimensions")
        return {'FINISHED'}
~~~

Now we want to add a number of columns, at differing x, y z 
coordinates. It would be convenient to have a function / method to 
do that for us. Let's set up this code so that we can extract a 
useful method.

Rename the x and y that we have in dimensions, to reflect that 
they are sizes not positions:

~~~python
        x_size, y_size, _old_z = ob.dimensions
        ob.dimensions = [x_size, y_size, height]
~~~

Rename height to z_size for consistency:

~~~python
    def execute(self, context):
        z_size = 4.0
        bpy.ops.mesh.primitive_cylinder_add(
            location=(0.0, 0.0, z_size/2),
            vertices=3,
            end_fill_type='NOTHING',
            enter_editmode=False)
        ob = bpy.context.object
        x_size, y_size, _old_z = ob.dimensions
        ob.dimensions = [x_size, y_size, z_size]
        # self.report({"INFO"}, "Column set dimensions")
        return {'FINISHED'}
~~~

Set up variables x_pos, y_pos, and z_pos, which will serve as 
parameters when we extract:

~~~python
    def execute(self, context):
        x_pos, y_pos, z_pos = (0.0, 0.0, 4.0)
        z_size = 4.0
        bpy.ops.mesh.primitive_cylinder_add(
            location=(x_pos, y_pos, z_pos - z_size/2),
            vertices=3,
            end_fill_type='NOTHING',
            enter_editmode=False)
        ob = bpy.context.object
        x_size, y_size, _old_z = ob.dimensions
        ob.dimensions = [x_size, y_size, z_size]
        # self.report({"INFO"}, "Column set dimensions")
        return {'FINISHED'}
~~~

I think this should still work as it did, placing a column of 
height 4 on the floor. Test in Blender, wishing that I had tests I 
could use in PyCharm. It does work. Commit save point.

I think I can extract a method now.

~~~python
    def execute(self, context):


    x_pos, y_pos, z_pos = (0.0, 0.0, 4.0)
z_size = 4.0
self.place_column(x_pos, y_pos, z_pos)
# self.report({"INFO"}, "Column set dimensions")
return {'FINISHED'}


def place_column(self, x_pos, y_pos, z_pos, z_size):
    bpy.ops.mesh.primitive_cylinder_add(
        location=(x_pos, y_pos, z_pos - z_size / 2),
        vertices=3,
        end_fill_type='NOTHING',
        enter_editmode=False)
    ob = bpy.context.object
    x_size, y_size, _old_z = ob.dimensions
    ob.dimensions = [x_size, y_size, z_size]
~~~

Just what I wanted. 

Oh. I just noticed that, according to our plan, we want the z size 
of the column to be the z coordinate. So I don't really need it as 
a parameter. We could revert and do over, or edit what we have. 
I'll edit. No, I'll do over. Back with this:

~~~python
    def execute(self, context):
        x_pos, y_pos, z_pos = (0.0, 0.0, 4.0)
        z_size = 4.0
        bpy.ops.mesh.primitive_cylinder_add(
            location=(x_pos, y_pos, z_pos - z_size/2),
            vertices=3,
            end_fill_type='NOTHING',
            enter_editmode=False)
        ob = bpy.context.object
        x_size, y_size, _old_z = ob.dimensions
        ob.dimensions = [x_size, y_size, z_size]
        # self.report({"INFO"}, "Column set dimensions")
        return {'FINISHED'}
~~~

Let's remove the z-size by setting it, for now, to z. Then, 
extract, including that part in the extracted bit:

~~~python
    def execute(self, context):


    x_pos, y_pos, z_pos = (0.0, 0.0, 4.0)
self.place_column(x_pos, y_pos, z_pos)
# self.report({"INFO"}, "Column set dimensions")
return {'FINISHED'}


def place_column(self, x_pos, y_pos, z_pos):
    z_size = z_pos
    bpy.ops.mesh.primitive_cylinder_add(
        location=(x_pos, y_pos, z_pos - z_size / 2),
        vertices=3,
        end_fill_type='NOTHING',
        enter_editmode=False)
    ob = bpy.context.object
    x_size, y_size, _old_z = ob.dimensions
    ob.dimensions = [x_size, y_size, z_size]
~~~

I think we like that better. I could test this in Blender. Since 
the refactoring was done by machine, it's quite safe. But I am 
cautious around blenders, so I will test again. Works as 
advertised. Commit save point.

Now let's look at how we did the export, because that operator 
iterates through all the vertices, and we will need to do 
something similar. The relevant part is this:

~~~python
    def execute(self, context):
        # Put code here
        obj = bpy.context.object

        if obj is None or obj.type != "MESH":
            return

        # Output geometry
        obj_eval = obj.evaluated_get(bpy.context.view_layer.depsgraph)

        verts = obj_eval.data.vertices
~~~

Reviewing the file writer, we find that the vertices, which are 
the corners of the fins or saw teeth that we use to compute 
position and roll, come in triples, back, up, front, the corners 
of the fins. For our purposes, we only need the back ones.

I think that I'll just type this in. It might not be too difficult.
In fact I paste most of it. Looking at the code above, I think we 
probably should be returning something, one of those Blender codes.
Leave it but make a note.

I only want every third vertex, the backs.

I really want the `co` part of the vertex, the coordinate, but 
we'll do that in a moment. We want to go every, oh, 40 points.

I think this might work:

~~~python
    def execute(self, context):


    obj = bpy.context.object
if obj is None or obj.type != "MESH":
    return
obj_eval = obj.evaluated_get(bpy.context.view_layer.depsgraph)
verts = obj_eval.data.vertices
backs = verts[::3]
column_verts = backs[::40]
for vert in column_verts:
    co = vert.co
    self.place_column(co.x, co.y, co.z)
# self.report({"INFO"}, "Column set dimensions")
return {'FINISHED'}
~~~

I have to try this in a file that has been prepared for me. I get 
a message saying

Python: RuntimeError: class RCG_OT_addcolumn, function execute: incompatible return value , , Function.result expected a set, not a NoneType

I am sure that comes from the empty return, which tells me that 
whatever is selected in the file provided, it's not a mesh. It's 
not: it's a nurbs path. I need a different start file.

~~~python
import bpy

# Name of the object you want to set smooth shading
object_name = "Cube"  # Change "Cube" to the name of your object

# Find the object by name
obj = bpy.data.objects.get(object_name)

# Ensure the object is a mesh
if obj and obj.type == 'MESH':
    # Switch to object mode to make changes
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Select all faces
    obj.data.polygons.foreach_set("select", [True] * len(obj.data.polygons))
    
    # Set shading to smooth
    bpy.ops.object.shade_smooth()
    
    print(f"Faces of {object_name} set to smooth shading.")
else:
    print(f"Object {object_name} is not a mesh or doesn't exist.")
~~~
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
self.place_support(position_vert, column_diameter, offset)
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
self.place_support(position_vert, column_diameter, offset)
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
    self.place_support(position_vert, column_diameter, offset)
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

## 20240422_0826 JR

Today I plan to start on causing the columns to be offset a bit, 
so as to line up better with the support rail of the track. The 
support rail will be assumed to be centered directly under the 
actual path the vehicle will follow. I propose to have an input 
value, the distance in meters below the path to the center of the 
support rail.

Because the `up` vector points to the local vertical of the path 
point, if we were to negate that vector, we would have the point a 
half meter *below* the path. We'll scale by the length and use 
that point. It should be "easy". (Should not have said that -- Hagrid)

Current code:

~~~python
def execute(self, context):
    obj = bpy.context.object
    if obj is None or obj.type != "MESH":
        return {'CANCELLED'}
    root_collection =
    bpy.context.view_layer.layer_collection.children[0]
    columns = bpy.data.collections.new("RCG Supports")
    scene = bpy.context.scene
    scene.collection.children.link(columns)
    bpy.context.view_layer.active_layer_collection =
    bpy.context.view_layer.layer_collection.children["RCG Supports"]
    obj_eval = obj.evaluated_get(bpy.context.view_layer.depsgraph)
    self.say_info(f"type {type(obj_eval)}")
    vertices = obj_eval.data.vertices
    self.say_info(f'vertices are {type(vertices)}')
    verts = vertices.values()
    self.say_info(f'verts are {type(verts)}, {len(verts)}')
    backs = verts[::2]
    self.say_info(f'{len(backs)} backs')
    column_verts = backs[::10]
    self.say_info(f'{len(column_verts)} column_verts')
    for vert in column_verts:
        co = vert.co
        self.place_support(position_vert, column_diameter, offset)
    bpy.context.view_layer.active_layer_collection = root_collection
    # self.report({"INFO"}, "Column set dimensions")
    return {'FINISHED'}


def place_column(self, x_pos, y_pos, z_pos):
    z_size = z_pos
    bpy.ops.mesh.primitive_cylinder_add(
        location=(x_pos, y_pos, z_pos - z_size / 2),
        vertices=6,
        radius=0.04,
        depth=z_size,
        end_fill_type='NOTHING',
        enter_editmode=False)
    ob = bpy.context.object
    ob.name = 'Support'
    bpy.ops.object.shade_smooth()
    # x_size, y_size, _old_z = ob.dimensions
    # ob.dimensions = [x_size/10, y_size/10, z_size]
~~~

This isn't easy to understand, so let's see if we can refactor to 
get some more meaningful bits, and get some of the noise out of 
the way. Along the way, I pass in the position vertex to the 
place_column. Soon, I'll pass in the up vertex as well.

~~~python
    def execute(self, context):


obj = bpy.context.object
if obj is None or obj.type != "MESH":
    return {'CANCELLED'}
root_collection = self.set_rcg_collection_active()
obj_eval = obj.evaluated_get(bpy.context.view_layer.depsgraph)
self.say_info(f"type {type(obj_eval)}")
vertices = obj_eval.data.vertices
self.say_info(f'vertices are {type(vertices)}')
verts = vertices.values()
self.say_info(f'verts are {type(verts)}, {len(verts)}')
backs = verts[::2]
self.say_info(f'{len(backs)} backs')
column_verts = backs[::10]
self.say_info(f'{len(column_verts)} column_verts')
for position_vert in column_verts:
    co = position_vert.co
    self.place_support(position_vert, column_diameter, offset)
bpy.context.view_layer.active_layer_collection = root_collection
# self.report({"INFO"}, "Column set dimensions")
return {'FINISHED'}


def set_rcg_collection_active(self):
    root_collection =
    bpy.context.view_layer.layer_collection.children[0]
    columns = bpy.data.collections.new("RCG Supports")
    scene = bpy.context.scene
    scene.collection.children.link(columns)
    bpy.context.view_layer.active_layer_collection =
    bpy.context.view_layer.layer_collection.children[
        "RCG Supports"]
    return root_collection


def place_column(self, x_pos, y_pos, z_pos, pos_vert):
    z_size = z_pos
    bpy.ops.mesh.primitive_cylinder_add(
        location=(x_pos, y_pos, z_pos - z_size / 2),
        vertices=6,
        radius=0.04,
        depth=z_size,
        end_fill_type='NOTHING',
        enter_editmode=False)
    ob = bpy.context.object
    ob.name = 'Support'
    bpy.ops.object.shade_smooth()
    # x_size, y_size, _old_z = ob.dimensions
    # ob.dimensions = [x_size/10, y_size/10, z_size]
~~~

This was done by machine, so I commit.

Now let's use the vertex, since we have passed it in. This I test 
in Blender, because I did it by hand. I might have found a machine 
way to do it, but I didn't really try. Works:

~~~python
    def place_column(self, x_pos, y_pos, z_pos, pos_vert):
        pos_co = pos_vert.co
        z_size = pos_co.z
        bpy.ops.mesh.primitive_cylinder_add(
            location=(pos_co.x,pos_co.y, pos_co.z - z_size / 2),
            vertices=6,
            radius=0.04,
            depth=z_size,
            end_fill_type='NOTHING',
            enter_editmode=False)
        ob = bpy.context.object
        ob.name = 'Support'
        bpy.ops.object.shade_smooth()
        # x_size, y_size, _old_z = ob.dimensions
        # ob.dimensions = [x_size/10, y_size/10, z_size]
~~~

Commit.

Remove unused parms from place_column and commit again.

~~~python
    def place_column(self, pos_vert):
~~~

Now I need to change the execute, which looks like this:

~~~python
    def execute(self, context):


obj = bpy.context.object
if obj is None or obj.type != "MESH":
    return {'CANCELLED'}
root_collection = self.set_rcg_collection_active()
obj_eval = obj.evaluated_get(bpy.context.view_layer.depsgraph)
self.say_info(f"type {type(obj_eval)}")
vertices = obj_eval.data.vertices
self.say_info(f'vertices are {type(vertices)}')
verts = vertices.values()
self.say_info(f'verts are {type(verts)}, {len(verts)}')
backs = verts[::2]
self.say_info(f'{len(backs)} backs')
column_verts = backs[::10]
self.say_info(f'{len(column_verts)} column_verts')
for position_vert in column_verts:
    co = position_vert.co
    self.place_support(position_vert, column_diameter, offset)
bpy.context.view_layer.active_layer_collection = root_collection
# self.report({"INFO"}, "Column set dimensions")
return {'FINISHED'}
~~~

That would be less ugly without all the say_info in there. I'll 
remove them. I do a rename as well:

~~~python
    def execute(self, context):


obj = bpy.context.object
if obj is None or obj.type != "MESH":
    return {'CANCELLED'}
root_collection = self.set_rcg_collection_active()
fins = obj.evaluated_get(bpy.context.view_layer.depsgraph)
vertices = fins.data.vertices
verts = vertices.values()
backs = verts[::2]
column_verts = backs[::10]
for position_vert in column_verts:
    co = position_vert.co
    self.place_support(position_vert, column_diameter, offset)
bpy.context.view_layer.active_layer_collection = root_collection
return {'FINISHED'}
~~~

I want to process pairs of back/up vectors in the `place_column` 
method, so this code needs a bit of tweaking. Down to `verts` 
we're OK but then let's group by two and see what we see.

This line:

~~~python
        backs = verts[::2]
~~~

Gives us every other one, starting at zero. If we would just 
produce pairs (back, up) we'd have what we need in `place_oolumn`. 
We can pass both in and ignore the up and have a testable point.

`backs` isn't a great name. `positions` would have been better. 
We'll use a better name in the new code.

~~~python
    def execute(self, context):


obj = bpy.context.object
if obj is None or obj.type != "MESH":
    return {'CANCELLED'}
root_collection = self.set_rcg_collection_active()
fins = obj.evaluated_get(bpy.context.view_layer.depsgraph)
vertices = fins.data.vertices
verts = vertices.values()
pos_up_pairs = [verts[i:i + 2] for i in range(0, len(verts), 2)]
every_tenth_pair = pos_up_pairs[::10]
for position_vert in every_tenth_pair:
    co = position_vert.co
    self.place_support(position_vert, column_diameter, offset)
bpy.context.view_layer.active_layer_collection = root_collection
return {'FINISHED'}
~~~

This much is testable as it stands. Try it. Error, the name I used 
confused me.This works:

~~~python
    def execute(self, context):


obj = bpy.context.object
if obj is None or obj.type != "MESH":
    return {'CANCELLED'}
root_collection = self.set_rcg_collection_active()
fins = obj.evaluated_get(bpy.context.view_layer.depsgraph)
vertices = fins.data.vertices
verts = vertices.values()
pos_up_pairs = [verts[i:i + 2] for i in range(0, len(verts), 2)]
every_tenth_pair = pos_up_pairs[::10]
for pair in every_tenth_pair:
    position_vert = pair[0]
    co = position_vert.co
    self.place_support(position_vert, column_diameter, offset)
bpy.context.view_layer.active_layer_collection = root_collection
return {'FINISHED'}
~~~

Commit. Now, let's see. We could follow the original plan and pass 
in the two vectors, but it seems like it's better to pass in the 
pair to the `place_column`. I don't see a machine refactoring 
series that will do this. I'll just code it, but I'll move the two 
setup lines into `place_column` and then pass pair, like this:

~~~python
    def execute:


...
for pair in every_tenth_pair:
    self.place_support(pair, column_diameter, offset)
bpy.context.view_layer.active_layer_collection = root_collection
return {'FINISHED'}


def place_column(self, pos_up_pair):
    position_vert = pos_up_pair[0]
    pos_co = position_vert.co
    z_size = pos_co.z
    bpy.ops.mesh.primitive_cylinder_add(
        location=(pos_co.x, pos_co.y, pos_co.z - z_size / 2),
        vertices=6,
        radius=0.04,
        depth=z_size,
        end_fill_type='NOTHING',
        enter_editmode=False)
    ob = bpy.context.object
    ob.name = 'Support'
    bpy.ops.object.shade_smooth()
~~~

I think this works but want to try it. Good. Commit: 
`place_column` now receives a position_up pair.

So that was a reasonably safe series, though I did make one 
mistake. Fortunately, I tested immediately, so it was easily found 
before things got worse. Now we are in a situation where every 
tenth pair of pos/up values gets a column. We could change the ten 
if we want to, and I think we may well want to.

As things stand, suppose that the coaster was 102 fins long. 
We'd set a column at 0, 10, ... 90, 100 ... and there would be two 
columns very close together at the join point. What I suspect we 
want is to work out a rule of thumb and then use the actual size 
of the track to decide how to allocate columns that appear equally 
spaced. It'll take some numeric thinking to figure that out, but 
it should be easy enough. And definitely for another day.

OK, now let's see about making the column offset itself. My first 
cut will be to add the negative of the vector from back to up to 
the position we use. That should offset the column a half-meter in 
the right direction since the length of the up vector is always 0.
5 as far as I know.

It's working as intended, the columns are now offset as if the fin 
was flipped 180 degrees. I've lost the ability to drag the screen 
around to my liking. Irritating.

Commit: columns placed opposite fin top.

Now let's set up and use a variable to represent the offset 
distance we want in meters.

Done. Too tired to write it up. Whew. Easy but intricate. Copied 
DS's note an chatGPT idea.

Commit: column placement accepts offset distance from 0 to 1 meter.

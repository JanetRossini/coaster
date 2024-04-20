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
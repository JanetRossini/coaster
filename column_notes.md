3 Column Notes

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
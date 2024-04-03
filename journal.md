# Journal

## 20240402

`test_pathlib` tests use of pathlib. I think we should stick with 
`os.path`, however, because Blender seems to want strings anyway, 
and `os.path` works OK.

## 20240413

I want to do some work to simplify the file code. I'll do some 
tests. One objective is to eliminate the explicit paths, because 
for privacy and security reasons we do not want those in the code. 
I think we can use the "working directory" feature to get them 
without needing to put them anywhere. For my purposes, I have 
created a file in my user base folder, HOME_DIR.txt, that contains 
the path to that folder, like /users/smith.

`test_we_can_compute_wm_elements` shows how we can compute the 
inputs to bpy.ops.wm.append. If we use `cwd`, we need not include 
the explicit paths.

With this code, we can completely remove all the triples like:

~~~python
file_track05 = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/track05.blend'
inner_track05 = 'Object'
object_track05 = 'track05'
~~~

... since they all follow the same naming pattern. 
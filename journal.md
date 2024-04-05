# Journal

## 20240402 (JR)

`test_pathlib` tests use of pathlib. I think we should stick with 
`os.path`, however, because Blender seems to want strings anyway, 
and `os.path` works OK.

## 20240413 (JR)

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

I've determined that the Vehicle class in dizziblender.py is the 
same as the one in Vehicle, except that the dizzi version has some 
spacing around @ operators. We can use the separate file pretty 
easily.

Similarly, for VTFileWriter, which can be moved to a separate file. 
It is currently in two files, a test of mine, and dizziblender.py.

I think that currently DS and JR have different project names. I'm 
not sure how we should change those to get synched up. Is it as 
simple as changing the project name in PyCharm? 

## 20240404 (JR)

Posted to my Slack for guidance on things. I think the DS project 
is probably properly set up to pull and push. We'll try pulling to 
get this new note, and then maybe have DS edit this and push it back.

We will both need to remember to pull from GitHub, and of course 
should also note via email when we have pushed something that 
needs pulling. I do not think that PyCharm will warn us if someone 
else has pushed. We'll find out. Hopefully with good news.

dizzi woz 'ere

## 20240405 (JR)

This morning I'm going to experiment with moving things around. In 
particular, I'd like to get down to just one Vehicle class, in its 
own file, and to get VTFileWriter moved out of the test files.

I plan to try these things and then roll back. Will report what 
happens here.

I start  with Git / Pull. All files are up to date, as I expected.

First experiment, cut Vehicle out of rollercoastergen and past 
over the existing one in vehicle.py.

### Bump

Before I even get there, I discover that both VtFileWriter and 
Vehicle are combined into rollercoastergen. This will not do. Why 
not? Because when changes are needed, they'll need to be done in 
multiple places.

I will try deleting mine, on the grounds that Dizzi's are newer. 
First, though, I'll diff them.

Ah. Some of your copies have CRLF line ends, not just LF. I think 
we should  change your prefs on that, tho it may be mostly harmless.

I've just spent mondo time fiddling with the LF / CRLF thing.

OK, moved VtFileWriter out of the tests into its own file. Will 
commit that.

We'll leave you with your own for now, try removing them when 
we're together.

Ran into trouble with Vehicle and its testing, because I use my 
own Vector and Quaternion classes, and you use blender mathutils, 
and, unfortunately for us all, mathutils in Blender has features 
that we seem not to have in Python's regular mathutils.

Best I can figure out right now, that means we can't have both a 
testable Vehicle class and one that is usable in Blender, unless 
we use my Q and V classes. Which we could do and should try, I guess.


### 0925

I'm gonna take a break. Eye bothering me this morning for some reason.
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

## 20240406 (JR Saturday)

By moving enough files to `modules` I was able to get Blender to 
act like it has accepted the file. I had to change the import in 
rollercoastergen from `from modules/vtfilewriter` to `from 
vtfilewriter`, which will of course not work in the tests. I did 
not know how to test the script, but at least it loaded.

I'm going to reset back to end of day Thursday and work from there.

Done. 

Now to figure out what to do.

I am quite sure that there are things we do not know about Blender 
add-ons, and things about Python modules, that are getting in the 
way here.

Some steps that could/should be taken include:

1. Make the two copies of Vehicle and VtFileWriter the same. In 
   the case of VtFileWriter, I think it needs improvement but 
   maybe that can wait. I think these absolutely must be done.
2. Try using `from . import thing`, which I saw somewhere as 
   something you can do with Blender.
3. Get the fake bpy files, which we may be able to use to help the 
   refactoring go more smoothly, or at least get rid of warnings, 
   and maybe even get prompting in PyCharm.

Found this idea, which would allow us to use different folders in 
blender from those in our local code. Seems nasty but might work.

~~~
if __name__ == '__main__':
    import sys
    import os
    rootdir = os.path.dirname(os.path.realpath(__file__))
    if rootdir not in sys.path:
        sys.path.append(rootdir)
    try:
        # Pycharm import
        from support import *
    except ModuleNotFoundError:
        # Blender Text Editor import
        from addon_folder.support import *
~~~

I have posted a question on Blender StackExchange, hoping for good 
ideas.

I've moved VtFileWriter out of rollercoastergen. May have to put it 
back, but I think the try/except horrid though it is, can be made 
to work.

Difficulty committing.

0850, gonna take a break.

Later that day ...

Discovered that my belief that mathutils does not have quaternion 
times vector was mistaken. I've converted all the files except 
those that directly test my replacement classes to use mathutils. 
All tests are green.

I have moved VtFileWriter out of rollercoastergen, but have not at 
this writing moved Vehicle. Both should be removed, if we can make 
rollercoastergen work. I think we can do that if I put try/except 
logic in, so that the imports are done two different ways.

I suppose there are other solutions, such as putting a file link 
into modules instead of the real file, or vice versa. I need a bit 
more thinking to be clear on what to do. Probably trying to 
explain will help me clarify my thoughts.

Committing for now. 1250 local time.

## 20240407_0805_JR

I am on a clean repo. I have one test skipped because it can't 
find Vehicle in VtFileWriter. The issue comes from the fact that 
Blender imports from the "modules" folder without your imports 
ever mentioning it.

I'll try breaking Vehicle away from RCG, because we want that anyway.

Miraculously, when I do that, the unlinked test passes. Life is good.

Committed. Now to test in Blender. Arguably I should have done 
that first. Manus do come up. Life remains good.

I think we are ready to begin refactoring in earnest. Whew! I hope 
I'm right. Committing this. 

### Looking at the flags

We should perhaps save this for a combined session, but I need to 
do something this morning, so I'll have a look at the use of the 
flags in the writer. I have a feeling that they should be sent in 
on creation. 

I notice that we pass a name into `write_files` but we do not use 
it, because the writer has been created already knowing the path 
and name. We should change the signature of the write_files method 
not to have that unused parameter. 

The methods of VtFileWriter are long and could use improvement.

I just realized that PyCharm will split the edit window, so I can 
have this file open on the right and another file, like 
vtfilewriter, open on the left. So I can study the code and take 
notes at the same time. I hesitate to say again that life is good.

Unless we go to class methods, such as

~~~
    writer = VtFileWriter.absolute_banked(...)
~~~

I have come to believe that the flags should not be passed in at 
creation time, although actual usage is always to create the 
writer and immediately call `write_files`. But there are so many 
parameters involved:

* Creation
    * verts - the vertices to be processed
    * filepath - the path to the output folder
    * basename - the output file name before numeric suffix
    * size - the chunk size to be written out
* Writing
    * basename - again, ignored, should remove
    * abs - absolute / relative flag. rename?
    * bank - bank / flat flag. rename?

Just noticed RCG line 555 triples is unused. Occurs four times. 
We'll remove. But I digress. 

What about having one creation method and four write methods:

~~~
write_absolute_flat, 
write_absolute_banked, 
write_relative_flat, 
write_relative_banked. 
~~~

That would let us hide the flags and make the meaning more clear.

If it were my code, I would try a few different ways, perhaps 
actually in the code, perhaps just typing alternatives into tests 
to see what I liked the look of.

In reality, this hardly matters, as we are really essentially done 
with this program, as far as we know. Until we aren't. But we are 
here to learn, every day, are we not?

Reading RCG throughout, I am impressed at how much DS has learned 
and figured out about Blender-Python relations. One could quibble 
about names and such, but given how little one knows about what 
Blender really cares about, it's quite impressive. 

I would like to see more pytest tests of the code here, but I 
don't see how to really do it. Well ... note this:

~~~
    def execute(self, context):
        # Put code here
        obj = bpy.context.object

        if obj is None or obj.type != "MESH":
            return

        # Output geometry
        obj_eval = obj.evaluated_get(bpy.context.view_layer.depsgraph)
        filepath = "C:/Users/Terry/PycharmProjects/blenderPython/"

        abs = True
        bank = False
        verts = obj_eval.data.vertices
        triples = [verts[i:i + 3] for i in range(0, len(verts) - 1, 2)]
        size = 500
        basename = "test_data"
        writer = VtFileWriter(verts, filepath, basename, size)
        writer.write_files(basename, abs, bank)

        return {'FINISHED'}
~~~

With just a little rearrangement, we could have the whole tail end 
of this block independent of Blender, just dependent on vertices. 
In that form we could test it. But is there anything really to test 
here, or is it just one big setup for calling the writer. Probably 
not.

Why do I write all this down? I write all this down for at least 
three reasons: first, to focus my attention; second, so that my 
readers (DS) can see what I think about and decide whether they 
would like to adopt any of those ways of thinking; and third, 
because I can look back over the past few days and see things 
that I'd like to remember but otherwise wouldn't.

I think we'll find that rearranging these is valuable. My guess is 
that I would hae to rearrange these things a few times to get to 
something I would like. Could we have a single class in here that 
all four of the Exp functions use, reducing their code to 
something much simpler? I bet we can! Maybe we'll start there.

One more thing ... should the Exp classes and the curve adding 
classes be in separate files? Given the hassle with imports, it 
may not be worth it.

Enough for now! Enjoy! 

## 20240408_0509_JR (Monday)

Too early to be awake, but there we are. Need to fix the writer 
bug. I know one way that will work, one way that might work, and 
one way that could possibly work.

1. Put Vehicle in with VtFileWriter
2. Change the import in VtFileWriter using try/except
3. Put import statements in the init.py in modules

Since #1 will absolutely work, we'll go with that: it's more 
important that we get to refactoring RCG. I'll move the long 
comment out of Vehicle, so the combined file isn't too awful to 
browse.

Right off the bat, I find that I didn't remove the old vehicle.py. 
I thought I moved the class and do not know how that happened. 
Remove it again. Tests all fail. I need to get better at this 
import for Blender thing. Fix one import, tests are green.

Commit: remove duplicate Vehicle file.

OK let's extract the comment from Vehicle. Put it in test_vehicle? 
A file of its own. vehicle.md. Commit: move vehicle comment to 
vehicle.md.

Now let's move Vehicle into VtFileWriter and remove vehicle.py. 
Almost forgot to repin the test tab after reboot. Remind me to 
mention that when next we work together.

Use the Move refactoring. Tests green. vehicle.py is empty. Remove 
the file with Safe Delete. Green. Commit: move vehicle to 
vtfilewriter, remove vehicle.py.

Now let's remove my Vector and Quaternion classes since we now 
know that mathutils works, which I mistakenly thought it did not 
in PyCharm. We don't mind removing them, because they are still in 
Git and GitHub.

I point the tests in test_vmath_quat to mathutils briefly, just to 
make sure it likes them. Then I can safe delete that test file, or 
could leave it pointed to real Quaternion. I think remove it: it'll 
be there if we need it. Remove v_quaternion also for one commit.
Commit: remove v_quaternion and tests.

Same drill for Vector and its tests. Safe Delete the tests then 
the class. Commit: remove v_vector and tests.

All green. Now, for my own amusement, I am going to look at 
Vehicle and VtFileWriter to see if they can be improved.

In this code:

~~~
class Vehicle:
    def __init__(self, back, up, front):
        self.back = back
        self.up = up
        self.front = front
        self.forward = (front - back).normalized()
        self.upward = (up - back).normalized()
~~~

We never use back, up, or front. We only use the forward and 
upward. Remove the first three statements. Green. Commit: remove 
unused member variables.

That's all I see in Vehicle. Let's look at VtFileWriter together: 
I think it would like to be improved just a bit. I'll make some 
notes here, but no changes.

I don't like the ifs here:

~~~
    def make_lines(coordinate_triples, abs, bank):
        lines = []
        back_zero = coordinate_triples[0][0]

        for back, up, front in coordinate_triples:
            if abs:
                back_zeroed = back
            else:
                back_zeroed = back - back_zero
            if bank:
                roll = Vehicle(back, up, front).roll_degrees()
            else:
                roll = 0
            output = f"<{back_zeroed.x:.3f}, {back_zeroed.y:.3f}, {back_zeroed.z:.3f}, {roll:.0f}>"
            lines.append(output)
        return lines
~~~

There are, in principle, four possible ways for this loop to go:
False, False; False, True; True, False; True, True. We could 
extract a couple of methods, perhaps like this:

~~~
    @staticmethod
    def make_lines(coordinate_triples, abs, bank):
        lines = []
        back_zero = coordinate_triples[0][0]

        for back, up, front in coordinate_triples:
            back_zeroed = VtFileWriter.get_rear_point(back, back_zero, abs)
            roll = VtFileWriter.get_roll(back, up, front, bank)
            output = f"<{back_zeroed.x:.3f}, {back_zeroed.y:.3f}, {back_zeroed.z:.3f}, {roll:.0f}>"
            lines.append(output)
        return lines

    @staticmethod
    def get_roll(back, up, front, bank):
        if bank:
            roll = Vehicle(back, up, front).roll_degrees()
        else:
            roll = 0
        return roll

    @staticmethod
    def get_rear_point(back, back_zero, abs):
        if abs:
            back_zeroed = back
        else:
            back_zeroed = back - back_zero
        return back_zeroed
~~~

We can make those two static methods much shorter:

~~~
    @staticmethod
    def get_roll(back, up, front, bank):
        return Vehicle(back, up, front).roll_degrees() if bank else 0

    @staticmethod
    def get_rear_point(back, back_zero, abs):
        return back if abs else back - back_zero
~~~

We also see that the write method is referring to the class, 
because it is static. We would prefer this:

~~~
    def make_lines(self, coordinate_triples, abs, bank):
        lines = []
        back_zero = coordinate_triples[0][0]

        for back, up, front in coordinate_triples:
            back_zeroed = self.get_rear_point(back, back_zero, abs)
            roll = self.get_roll(back, up, front, bank)
            output = f"<{back_zeroed.x:.3f}, {back_zeroed.y:.3f}, {back_zeroed.z:.3f}, {roll:.0f}>"
            lines.append(output)
        return lines
~~~

Each of those changes could be committed if we wished: the tests 
are all passing. I would prefer to have better tests that check 
all the combinations to be sure they give uw what we want. The 
code seems right, and it seems to work in SL ... but that's a pretty 
remote test.

There may be better ways to do this. For now, I'm rolling back, 
after committing just the journal.

## 20240408_0931_JR

Now to mess around with the RCG a bit, just to practice. There are 
a few different kinds of classes, each with a bunch of duplication.
For the export, I think we need to decide whether we prefer the 
curren buttons, or a smaller number of buttons with pull downs or 
cycler things. I'll start with the add methods, which all have an 
eerie similarity in their `execute` method. Here are two:

~~~
class RCG_OT_addflatruler20(Operator):
    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_trackflatruler20, inner_trackflatruler20, object_trackflatruler20),
            directory=os.path.join(file_trackflatruler20, inner_trackflatruler20), filename=object_trackflatruler20)
        trackflatruler20 = bpy.data.objects["trackflatruler20"]
        trackflatruler20.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = trackflatruler20


class RCG_OT_addflatruler10(Operator):
    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_trackflatruler10, inner_trackflatruler10, object_trackflatruler10),
            directory=os.path.join(file_trackflatruler10, inner_trackflatruler10), filename=object_trackflatruler10)
        trackflatruler10 = bpy.data.objects["trackflatruler10"]
        trackflatruler10.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = trackflatruler10
~~~

I think we might profit from moving all the similar adds adjacent 
to each other. Right now, there are some other classes sprinkled 
in between them, such as between the track ones and the ruler ones.
This will help us observe similarities and differences, and give 
us a better chance of finding all the places we can make an 
improvement. For now, I'm just practicing and plan to roll back.

I have split my screen to show the definition of 
`file_trackruler10` in one split, with the class 
RCG_OT_addflatruler10 underneath. And I have journal open on the 
right, so I can take these notes. 

We can make these methods more alike by using generic names where 
possible In the one above the name trackflatruler10 could be ruler.
But when we add track, I think we're using exactly the same code, 
so maybe we should use an even more generic word, like `item` or 
`addend` or the like. 

Put cursor on `trackruler10` and do Shift+F6, or pop up the 
right-click menu and select Rename. Or even use top Refactor / 
Refactor this. But learning a few hot keys speeds things up. 

PyCharm asks if we want to change string occurrences. We do not, 
just code. We get:

~~~
    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_trackruler10, inner_trackruler10, object_trackruler10),
            directory=os.path.join(file_trackruler10, inner_trackruler10), filename=object_trackruler10)
        addend = bpy.data.objects["trackruler10"]
        addend.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = addend
~~~

Interesting. If we did that throughout we could extract a variable:

~~~
    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_trackruler10, inner_trackruler10, object_trackruler10),
            directory=os.path.join(file_trackruler10, inner_trackruler10), filename=object_trackruler10)
        addend_name = "trackruler10"
        addend = bpy.data.objects[addend_name]
        addend.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = addend
~~~

Then we could extract this method:

~~~
    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_trackruler10, inner_trackruler10, object_trackruler10),
            directory=os.path.join(file_trackruler10, inner_trackruler10), filename=object_trackruler10)
        addend_name = "trackruler10"
        self.select_and_set_context(addend_name)
        return {'FINISHED'}

    def select_and_set_context(self, addend_name):
        addend = bpy.data.objects[addend_name]
        addend.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = addend
~~~

PyCharm observes that this method could be static, and offers to 
make it a function instead. We might like that, because as a 
function, it will be available to all our classes. PyCharm puts it 
somewhere. We'll want to move it somewhere prominent.

But now look at another ruler, like "05":

~~~
class RCG_OT_addruler05(Operator):
    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_trackruler05, inner_trackruler05, object_trackruler05),
            directory=os.path.join(file_trackruler05, inner_trackruler05), filename=object_trackruler05)
        trackruler05 = bpy.data.objects["trackruler05"]
        trackruler05.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = trackruler05

        return {'FINISHED'}
~~~

We can change that to:

~~~
    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_trackruler05, inner_trackruler05, object_trackruler05),
            directory=os.path.join(file_trackruler05, inner_trackruler05), filename=object_trackruler05)
        select_and_set_context("trackruler05")
        return {'FINISHED'}
~~~

I wonder if there is a more automated way to do this. I tweak the 
inspection for duplicates, and PyCharm will show them to me. If I 
extract `addend_name` from each of the `bpy.data.objects` lines, 
they all get marked as duplicated. (Any name would do, it ignores 
the names in looking for duplicates. But in general, when doing 
this, we work to *increase* duplication. Curiously, the more 
duplicated the code gets, the easier it is to extract it.)

Once we get PyCharm recognizing these segments, we can use the 
show duplicates screen to click to them, but we still have to do 
the edit somewhat manually. However, if we have set them all up by 
extracting addend_name, we can just paste the new call after 
selecting the lines that need to be changed.

Enough experimentation. I've been at this for about another hour 
and have plenty of ideas for things we could do.

All the ideas, so far, are a bit tedious. Once we create a lot of 
duplication, that often happens, because we have eight or ten 
places to clean up. Some folks will refactor on three duplications.
I will often do it with just two, but that is sometimes premature. 

Rolling back after committing journal.

## 20240411_0833_JR

I have two tasks on my task card: fix the mathutils issue so that 
tests will run on both machines, and change the path code for file 
writing so that it does not contain an explicit path but is 
instead put into a coasterdata folder in the user's base folder.

My plan is to change things so that we always use my Vector and 
Quaternion classes, which pass all my tests and worked throughout. 
It just seemed that using the official mathutils made more sense. 
But not if it's not going to work without a C++ compiler.

To do this, I will have to check out old versions of the tests and 
code. I'll make some notes of the process here.

This journal is getting long. I wonder if some other approach 
would be better, maybe a folder of notes? I'll add that to my card.

At the lower right on my screen are a few buttons that open a 
console, packages, etc. One of them is a little network-looking 
thing,and that leads to the Git history. Hover tip is "Git".

The approach is the best one I know for this kind of thing: find 
and check out the latest version that contained the files needed, 
and copy them somewhere else. I generally paste them into my 
regular editor, but I wonder if I can drag them to and from my 
desktop. I'll try that.

Looking at the Git list I see a small branch in there. Eeek, I try 
never to branch. I think that reflects a failure to pull.

Which reminds me to check my git status and I see that I have some 
mods hanging. I sort that out.

I checked out the revision, dragged the files out to desktop. 
Checked out main (top of changes), dragged the files back into the 
project window folder. They are now there, ready to be checked in.

I had to set up a conditional import in vtfilewriter to get the 
imports working but when I commit this, we'll be converted to use 
my mathutils, not Blender / Python's file. Needs a solid test.

And I am just about fed up with PyCharm's grammar and spelling 
whining. Commit: convert to use v_mathutils.

## 20240413_JR (Saturday)

We discovered that the change to use my library did not work. We 
actually came up against these issues:

1. Blender will produce mathutils Vectors, so unless we do a lot 
   of too clever stuff, we probably cannot use my library. (It 
   might be easy enough now to convert to JR-vectors in just 
   one spot, but I'm not sure yet what we should do.)
2. Blender seems to hold on to scripts even when you use its 
   reload function, so that our library scripts are not dropped. 
   (This, too, may ot be quite accurate, as DS's process was a 
   bit erratic.)
3. We need to get to the point where I can do a complete round 
   trip on my machine.
4. We need to get to the point where DS can test on her machine.
5. We need tests for fie writing and all four kinds of point creation.

## 20240414_0848_JR (Sunday)

Blender API says that MeshVertex.co is a mathutils.Vector. But 
vtfilewriter got an error trying to send `seq` to one of them. Right.
They do not understand `seq`, though JR vectors do. 

The "correct" thing is `to_tuple`, which we could implement in 
our v_mathutils. Added a couple of tests of vectors, numpy, array, 
etc.

Let's look at reading in the files on my machine. I think that to 
do that we should put them in some standard spot, like the output 
files. For now, I'll copy them to the same folder. They are in 
~/coasterdata/coasterobjects.

Code changed to read from there. My Blender created track 
successfully.

Tried to install bpy, no joy, requires python <= 3.8 or something 
like that. Tried a fake_bpy but probably did it wrong.

Changed again, to read track data from the project. DS should test 
as well.

## 20240415_0745_JR (Monday)

Short of trying to get an old python installed in the project, I 
do not see a way to get DS's version to run the tests. At this 
writing, I do not think it is worth doing, but that we should try 
to do new work in a project that is set up to work on both systems,
so that DS can learn the testing aspect of Python. Because of the 
incompatibility with mathutils, that may be difficult.

One possibility still on the table would be to convert the current 
code to use the JR version of Vector and Quaternion, and not to 
use mathutils at all. There is, however, at least one point in the 
system where we will be handed a mathutils Vector instance, but 
since Python is duck-typed, we can work around that.

I am waffling about this. Waffle waffle.

We need some tests for the vtfilewriter, since it has four options 
that produce somewhat different results. I'll work on that this 
morning. But first, I want to make a small change to the JR github.
io site.

Whee, excerpts!

### Tests for vtfilewriter

I think it's fair to say that the most important need is to test 
the four combinations of flags, to be sure that the right values 
are produced. We could test formatting or test that it writes all 
the data or such but that's of even lower priority.

The method in question is:

~~~python
    @staticmethod
    def make_lines(coordinate_triples, abs, bank):
        lines = []
        back_zero = coordinate_triples[0][0]

        for back, up, front in coordinate_triples:
            if abs:
                back_zeroed = back
            else:
                back_zeroed = back - back_zero
            if bank:
                roll = Vehicle(back, up, front).roll_degrees()
            else:
                roll = 0
            output = f"<{back_zeroed.x:.3f}, {back_zeroed.y:.3f}, {back_zeroed.z:.3f}, {roll:.0f}>"
            lines.append(output)
        return lines
~~~

I can see ways that I'd like to improve that code, which makes 
tests more necessary, since fiddling with the conditional logic is 
exactly why we have tests. 

We can test this method directly, as it is static. (Does not 
reference self.) So we can create a list of coordinate_triples, 
whatever those are, create a list of expected output records, and 
call it. 

Since we believe it works now. we could even inspect current 
output and then use it as a "golden master". We currently have no 
tests at all for that method.

Irritatingly, we'll need mathutils or v_mathutils, and we use the 
Vehicle class as well, which uses the math stuff. All this just to 
test the use of two booleans? 

I'm allowed to use machine refactorings without tests: they are 
highly reliable and almost certain not to break behavior. Extract:

~~~python
    @staticmethod
    def make_lines(coordinate_triples, abs, bank):
        lines = []
        back_zero = coordinate_triples[0][0]

        for back, up, front in coordinate_triples:
            back_zeroed, roll = VtFileWriter.get_line_data(back, up, front, back_zero, abs, bank)
            output = f"<{back_zeroed.x:.3f}, {back_zeroed.y:.3f}, {back_zeroed.z:.3f}, {roll:.0f}>"
            lines.append(output)
        return lines

    @staticmethod
    def get_line_data(back, up, front, back_zero, abs, bank):
        if abs:
            back_zeroed = back
        else:
            back_zeroed = back - back_zero
        if bank:
            roll = Vehicle(back, up, front).roll_degrees()
        else:
            roll = 0
        return back_zeroed, roll
~~~

Now we could just test `get_line_data` to be sure it does what we 
expect. We still have the issue of using Vehicle. 

I'll start by trying some simple tests on this new method. It 
should be possible now to just test one combination, or maybe just 
a few, to be sure we get what we want. Then we'll see if we can 
eliminate the reference to Vehicle. 

I should drop that Vehicle requirement: I'm trying to do this so 
that DS can run the tests, and that's really off the table unless we 
replace the vector and quad. 

Once I get started four tests are quite easy. They are in 
test_file_writing, named:

~~~python
    def test_get_line_data_rel_bank(self):
    def test_get_line_data_abs_bank(self):
    def test_get_line_data_abs_flat(self):
    def test_get_line_data_rel_flat(self):
~~~

That was fairly easy, once I got started. 

Now I have a couple of improvements in mind for this code:

~~~python
    @staticmethod
    def make_lines(coordinate_triples, abs, bank):
        lines = []
        back_zero = coordinate_triples[0][0]

        for back, up, front in coordinate_triples:
            back_zeroed, roll = VtFileWriter.get_line_data(back, up, front, back_zero, abs, bank)
            output = f"<{back_zeroed.x:.3f}, {back_zeroed.y:.3f}, {back_zeroed.z:.3f}, {roll:.0f}>"
            lines.append(output)
        return lines

    @staticmethod
    def get_line_data(back, up, front, back_zero, abs, bank):
        if abs:
            back_zeroed = back
        else:
            back_zeroed = back - back_zero
        if bank:
            roll = Vehicle(back, up, front).roll_degrees()
        else:
            roll = 0
        return back_zeroed, roll
~~~

My tests don't support these ideas terribly well, but I'll try to 
set that concern aside. Ideas include:

1. If we init back_zero either as shown above or to zero vector, 
   we can remove the first if from get_line_data. Oh, I think I 
   see a neat way to do that.
2. If we were to compute the roll and pass it in, we could avoid 
   the reference to Vehicle in our tests. Not important?

Let's do my neat idea. Refactor, pulling out a completely useless 
method:

~~~python
    @staticmethod
def get_line_data(back, up, front, back_zero, abs, bank):
    return VtFileWriter.get_line_data_2(back, up, front, back_zero,
                                        bank)


@staticmethod
def get_line_data_2(back, up, front, back_zero, abs, bank):
    if abs:
        back_zeroed = back
    else:
        back_zeroed = back - back_zero
    if bank:
        roll = Vehicle(back, up, front).roll_degrees()
    else:
        roll = 0
    return back_zeroed, roll
~~~

The tests still pass. Now we change to this:

~~~python
    @staticmethod
def get_line_data(back, up, front, back_zero, abs, bank):
    if abs:
        back_adjust = Vector((0, 0, 0))
    else:
        back_adjust = back_zero
    return VtFileWriter.get_line_data_2(back, up, front, back_adjust,
                                        bank)


@staticmethod
def get_line_data_2(back, up, front, back_adjust, abs, bank):
    back_zeroed = back - back_adjust
    if bank:
        roll = Vehicle(back, up, front).roll_degrees()
    else:
        roll = 0
    return back_zeroed, roll
~~~

Now the abs flag is not needed in the second method.

I may have lost the thread, but I think what we should do now is 
pass in the adjustment when we call the get_line_data method. But 
we need to do that in two places now, the tests and the real code.

I'm going to back up to before I did that last extract. And I'm 
going to commit to make a save point.


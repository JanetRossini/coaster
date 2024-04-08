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

~~~python
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
# Notes for Coaster Project - 20240402

## Fundamentals

* Very small steps. No, smaller than that.
* Spikes wherever possible[^spike].
* Use tests where possible.

## Objectives

* Reduce number of classes
* Remove duplication
* Improve ability to collaborate
* Improve DS ability to learn / apply power tools

## Steps, not necessarily in order

* Break VtFileWriter into separate file
* Do other things need breaking up?
* Build a little test file for spikes etc.
* Get rid of explicit personal paths (use pathlib.Path?)
* Arrange for JR and DS versions to stay synchronized. GitHub?
* Have ability to import bpy in PyCharm
* Devise good guidelines for use of separate files
* Get project all in one folder 
* Load into Blender, not cut and paste. (Reload?)

## Questions

Should we stick with current button approach or move to pull down
and rotating thing right away? Should we spike or sketch both 
approaches before we commit? Which way provides smaller steps?

Does pathlib work in Blender? 

## (Foot)Notes

[^spike]: Term from Ward Cunningham. Quick and dirty experiment. 
Think of quickly driving a spike through a board. Generally once 
we do a spike we should throw away the code and keep the learning.
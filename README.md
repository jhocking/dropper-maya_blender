# dropper4python

A very useful but unglamorous tool, a "dropper" is a simple level editor that lets you position objects in 3D space and then writes all the positions/rotations/etc. to an easily parsed text file. Your game can then read this file to put everything in the same place.

This is a pair of Python scripts that allow you to use either Maya or Blender as a dropper. It will export any custom attributes that you set, plus you can choose either JSON or XML for the output format. The included scene demonstrates how to setup objects for export.

---

written in Maya 2017
<br>MIT license
<br>open in Script Editor window, then Execute

Saves info about objects in the scene:
<br>name, position, rotation, scale, custom attributes
<br>Select either XML or JSON for the data format. 

---

code for Blender 2.8 (originally 2.77)
<br>GPL license https://www.blender.org/support/faq/
<br>install in Edit > Preferences > Add-ons
<br>once installed: File > Export > Dropper

Saves info about objects in the scene:
<br>name, position, rotation, scale, custom properties
<br>Select either XML or JSON for the data format. 

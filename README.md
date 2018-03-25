EDM model files - Blender Import/(Export) Addon
===============================================

This is a **HIGHLY EXPERIMENTAL**, totally **UNOFFICIAL** attempt to build a
blender addon to allow importing/exporting of `.EDM` model files, as used in
the flight simulator DCS world. It has been engineered by careful studying of
the binary file format, intuition, research, much guesswork, and many, many
crashes of the model viewer.

In its current state, it allows simple importing functionality whilst the fine
details of the file structure are worked out, and basic exporting. Much of the
data is reasonably easy to interpret, but translating the concepts to Blender
is still a WIP. Also, there may be advanced modelling features used in DCS
world modules that the author does not own, but a universal importer is less a
goal than understanding the file format well enough to build a simple
exporter.

What Works
----------

- Parsing and reading raw data for every .edm file included in DCS world (this
  is reading only, not importing into blender)
- Basic importing of geometry with diffuse texture layers - textures are
  assumed to be in the same folder or a subfolder named 'textures'
- Importing simple rotation, translation and visibility animations
- Connectors, and UI integration to mark empties as such
- Exporting basic meshes with simple animations and single diffuse textures

What Doesn't Work
-----------------
- Exporting anything in a hierarchy is WIP and really fails badly
- Scale animation, and non-quaternion rotation animation isn't exported
- Bone-based animations are not handled at all
- Multiple argument animations per object - decisions on the best way to 
  represent this in Blender need to be made (NLA? Custom Action attributes?)
- Complex translation of material layers, including specular, bump maps etc
- Not all geometry ends up properly placed when importing

Basic installation process
-------------------
1. Launch Blender and open up the User Preferences from the File menu.
2. Switch to the Addons tab and then click “Install From File...”
3. Navigate to where you downloaded Blender_io_EDM.zip and select the file. Blender will install io_EDM to a standard location, then show the newly installed addon in the list. Simple then check the ‘Enabled’ box to finish installing.

You can also click ‘Save User Settings’ to keep the addon loaded next time you start blender - If you do this, it will not interfere with any other uses of Blender, but will leave the edm-specific user interfaces in place until you disable the addon.

Further Information
-------------------
For further information and full installation instructions (with images), please see the
documentation at https://ndevenish.github.io/Blender_ioEDM/

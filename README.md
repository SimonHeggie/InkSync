# InkSync
An Inkscape extension for file syncing between apps.

Quickly sync Inkscape svg, plain svg, png, pdf and html5 canvas using the overwrite feature.
Inkscape 1.1+ (1.3 tested)

*Featuring* Inklinea's **object to path** code for ultimate compatability.

This is not a replacement for saving or Inkscape autosave :) ---

**Installation:**

Take the PY and INX file and place in the Extensions folder.

Linux Extension locations:

/home/username/.config/inkscape/extensions

/usr/share/inkscape/extensions

If it's not there or you're on Windows of Mac, try: 'Edit ‣ Preferences ‣ System: User extensions' to see which directory holds your extensions

**USE:**

-Appears at Extensions>Export
-After setting the options in the main dialogue, assign a shortcut in Inkscape Edit>Preferences>Interface>Keyboard to:

org.inkscape.simonh.ink_sync.noprefs

For shortcut triggered quick export --- Not 100% sure where the PDF and HTML5 settings are pulled from, presume from last used save settings.

These formats should work fine in multiple different apps including Photoshop and Blender.
I'll explain the process in Krita and it will be a very similar process for Photoshop users.
Because the focus on Inkscape is Vector and SVG is the best performing format here, that's what I recommend for most interchanges.

Syncing an SVG to Krita:

- Be sure to use an svg that has 'text to path' enabled if you have any fancy text with unusual kerning or the like.
- After syncing a file to a directory, in krita, in the drop down next to the new layer button; select 'File layer'.
- Give it a name, direct the file location to your SVG.
- 'No scaling' is fine if you're SVG is already big enough, try the other option for different scales.
- 'Bicupic' scaling can work pretty well but somehow nearest neighbor looks a little more appealing from my tests. (Hit ok)
- To update the svg, simply run the tool again, go to krita and somewhat quickly you'll see the new SVG.

Based on Inklinea's Quick Export extension:

https://gitlab.com/inklinea/quick-export

Be sure to support his efforts on quick export as InkSync may rely on his technology moving forward.

Future ideas:

-Option to merge layers down
-Support more types of objects/setups

#! /usr/bin/env python

"""
Installation instructions: Place this script in your path and make it
executable with "chmod +x labelpin" (without the quotes).

For usage instructions, see below.

----
Version 1.1 of 2012/6/25

By Nathan Dunfield : http://dunfield.info

Available from : https://faculty.math.illinois.edu/~nmd/software/index.html

----
Version 1.2 of 2017/8/25

By Oleg Soloviev : oleg.soloviev@gmail.com

Added bounding box calculation for PDF files

Versions for Python 2 and Python 3
----

This code is in the public domain.  
"""

help_str = r"""Usage:  labelpin file

where file is an ".eps" or ".pdf" file.

A window will appear with your image.  Simply click on it to generate
the label locations, which are output with the associated LaTeX code
in the terminal window.  When you're done, just close the window and
copy everything into your LaTeX file.

The resulting LaTeX code is intended for use with the "pinlabel" package:

http://www.ctan.org/tex-archive/help/Catalogue/entries/pinlabel.html

Requirements:

 * Python with Tkinter.  
 * GhostScript.

On OS X, the is first built in and the others are included with the
MacTeX-2010 distribution: http://www.tug.org/mactex/

On Linux, are all available as standard packages, with the first
called "python-tk" on Ubuntu/Debian and "tkinter" on
Fedora/Mandriva/PCLinuxOS.

On Windows, make a hardlink to your GhostScript executable with (type in command line the following line)

mklink /j gs.exe "C:\Program Files\gs\gs9.20\bin\gswin64c.exe"

and place it in some directory in the path.

To use, run in command line
 
python lablepinX.py file.ext

where X is your Python version and ext is either pdf or eps
"""

pinlabel_prefix_text = r"""% Click on the window that appeared to generate the label
% locations.  When you're done, close the window and then 
% copy everything into your LaTeX file.

\begin{figure}[htb]
\labellist
\small\hair 2pt"""

pinlabel_suffix_text = r"""\endlabellist
\centering
\includegraphics[scale=1.0]{%s}
\caption{  }
\label{fig:label}
\end{figure}"""

import os, sys, re, tempfile, string, Tkinter
import subprocess
from optparse import OptionParser

def file_extension(file_name):
    return os.path.splitext(file_name)[-1].lower()
    
def is_postscript_file(file_name):
    return os.path.splitext(file_name)[-1].lower() in ['.eps','.pdf']

def convert_file_to_bitmap(in_file, out_file, pixels_per_pt=1):
    # If it's PostScript-based, use GhostScript to convert to a bitmap.
    if is_postscript_file(in_file):
        os.system("gs -sDEVICE=ppmraw -dEPSCrop -dNOPAUSE -dBATCH -dSAFER -q " +
                  "-dAlignToPixels=0 -dTextAlphaBits=4 -dUseCropBox -dGraphicsAlphaBits=4 " + 
                  "-r%d -sOutputFile=%s %s" % (72*pixels_per_pt, out_file, in_file))
    else:
        # Use ImageMagick and pray.
        os.system("convert %s %s" % (in_file, out_file))

def get_bounding_box(in_file): 
    if is_postscript_file(in_file): # now we can get correct bounding box also for PDF
        data = subprocess.check_output("gs -dBATCH -dSAFER -dNOPAUSE -sDEVICE=bbox %s"      % (in_file),stderr=subprocess.STDOUT)
    else:
        data = ''
    box = re.search("%%BoundingBox:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", data)
    return [int(x) for x in box.groups()[:2]] if box else [0,0]
      
def label_file(file_to_label):
    # Start Tk
    root = Tkinter.Tk()

    # Load the image file
    base_name = os.path.splitext(file_to_label)[0]
    image_file = tempfile.mktemp() + ".ppm"
    pixels_per_pt = 2 if is_postscript_file(file_to_label) else 1
    convert_file_to_bitmap(file_to_label, image_file, pixels_per_pt)
    tkpi = Tkinter.PhotoImage(file=image_file)
    bbx, bby = get_bounding_box(file_to_label)

    W, H = tkpi.width(), tkpi.height()
    w, h = W/pixels_per_pt, H/pixels_per_pt
  
    # Print the inital TeX code 
    print( pinlabel_prefix_text )

    # Start Tk

    root.geometry('+%d+%d' % (100,100))
    root.geometry('%dx%d' % (W, H))
    
    image_canvas = Tkinter.Canvas(root, width=W, height=H, bd=0, highlightthickness=0)
    image_canvas.create_image( (0,0), anchor="nw", image=tkpi)
    image_canvas.circle_count = 0
    
    def process_click(event):
        x, y = event.x, event.y
        r = 6
        print " \pinlabel {$%s$} [ ] at %d %d" % (string.letters[image_canvas.circle_count % len(string.letters)],
                                                    x/pixels_per_pt + bbx, h - y/pixels_per_pt + bby)
        image_canvas.create_oval(x-r, y-r, x+r, y+r,outline="black", fill="red")
        image_canvas.circle_count += 1
        
    image_canvas.bind("<Button>", process_click)
    image_canvas.place(x=0, y=0)
    image_canvas.pack()
    root.title(base_name)
    root.mainloop()

    # Print the rest of the TeX code and clean up
    print( pinlabel_suffix_text % base_name )
    os.remove(image_file)

if __name__ == "__main__":
    parser = OptionParser()
    parser.set_usage(help_str)
    options, args = parser.parse_args()
    if len(args) == 0:
        print "Sorry, no file specified."

    for file_to_label in args:
        if not os.path.exists(file_to_label):
            print "Sorry, the file you specified (%s) does not exist." % file_to_label
        else:
            label_file(file_to_label)




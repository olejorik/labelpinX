# labelpinX


This is a (slightly) improved version of [labelpin](https://faculty.math.illinois.edu/~nmd/software/labelpin) script by Nathan Dunfield for labelling figures in LaTeX with pinlabel package.

## What is it for?

A beautiful publication in LaTeX uses the same font for its text and for the labels in its figures. At some prehistoric ages it was done with [PSfrag](https://www.wikiwand.com/en/PSfrag)
Unfortunately, this wonderful package is not compatible with modern LaTeX versions: pdfTeX, XeTeX, and LuaTex.
A good and light-weight alternative is to use [pinlabel](http://www.ctan.org/tex-archive/help/Catalogue/entries/pinlabel.html) package.
The only drawback of the package is tiresome procedure of getting right coordinates for the labels.
[Nathan Dunfield](http://dunfield.info) wrote this easy to use interface for the package, and I have added a couple of lines to make it compatible with Python 3 and to get correct coordinates for pdf files with crop box.

### Prerequisites

* Python with Tkinter.  
* GhostScript.



### Installing and using

The instructions are at the top of file. For instance, on Windows you should

1.  make a hardlink to your GhostScript executable, so you can call it as "gs" from command line (equivalent to as it's done on  Mac and Linux)

  ```
  mklink /j gs.exe "C:\Program Files\gs\gs9.20\bin\gswin64c.exe"
  ```

2. Place the link in some directory in the path, _e.g._ in `C:\Windows`

3. Run in command line

  ```
  python lablepinX.py file.ext
  ```
  where `X` is your Python version and `ext` is either `pdf` or `eps`

4. Copy the output to your tex file.

See also the attached example.


## Version history

Version 1.2 of 2017/8/25

* Added bounding box calculation for PDF files (_e.g._ version 1.1 gives wrong coordinates for file `simplex.pdf` in the [example](./example/) folder)
* Versions for Python 2 and Python 3
* uploaded to BitBucket

## Contributing

Feel free to improve it any way.



## Authors

* **Nathan Dunfield** - *Initial work* - [Nathan Dunfield](http://dunfield.info)

* **Oleg Soloviev** - *Version 1.2* - [Oleg Soloviev](https://www.researchgate.net/profile/Oleg_Soloviev)

## License

Public domain.

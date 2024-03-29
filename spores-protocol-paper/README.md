# File structure

 - `Makefile` contains build instructions.
 - `abstract.tex` contains the abstract.
 - `contents.tex` contains the main paper content, which might include sub-files 
   for the various sections.
    - `intro.tex` contains the intro section.
    - `related.tex` contains the Related Work section.
    - `user-model.tex` contains the user-model stuff.
    - `algorithm.tex` contains a description of the algorithm.
    - `privacy.tex` outlines our privacy expectations.
 - `preamble.tex` contains the LaTeX document preamble.
 - `spores.tex` simply puts the files together.


# Compilation

Ensure that you've cloned all the needed submodules:
```
git submodule update --init --recursive
```
Then you can compile the paper using the make utility:
```
make
```

# vstools-md2latex-conv-public

Utility for the conversion of markdown texts into LaTeX format

Requirements:

- Requires [Pandoc](https://github.com/jgm/pandoc) to be installed.
- Requires an installation of the following Python packages: `pip install emoji pypandoc`

Usage:

```
python md2latex.py input.md [input.tex]
```

By default, if only a `.md` file path is provided, we will get the output file with the same name (but with a `.tex` extension) and in the same location:

```
python md2latex.py my-md-file.md
```

In case you want to change the output filename and its location:

```
python md2latex.py my-md-file.md my-latex-file.tex
```





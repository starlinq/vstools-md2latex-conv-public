# vstools-md2latex-conv-public

Utility for the conversion of markdown texts into LaTeX format.

Nowadays, markdown files contain not only text with structural and formatting elements, but also emojis, especially in the output of various AI tools. The purpose of this utility is to convert those texts with emojis into a LaTeX-compatible format, not losing any elements of their rich formatting!

Requirements:

- Requires [Pandoc](https://github.com/jgm/pandoc) to be installed.
- Requires an installation of the following Python packages: `pip install emoji pypandoc`
- The output LaTeX file will need an `emoji` package

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





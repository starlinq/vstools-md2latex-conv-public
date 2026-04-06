# This is a Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import sys

import md2latex_lib




# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print("Utility for the conversion of markdown texts into LaTeX format (ver.3b)")
    print("Requires Pandoc to be installed.")
    print("Requires an installation of the following Python packages:")
    print("pip install emoji pypandoc")

    # debug
    print(f"Current command: python {sys.argv}")
    #print(f"Current command: {sys.argv[0]} {sys.argv[1]} {sys.argv[2]}")


    # release v>3a

    # test: python md2latex.py cp-20260326-model-assisted-annotation.md
    # test: python md2latex.py cp-20260326-model-assisted-annotation.md cp-20260326-model-assisted-annotation.tex

    input_md   = ""
    output_tex = ""


    if 3 < len(sys.argv) < 2:

        print("Usage: python md2latex.py input.md [input.tex]")
        print("Requires Pandoc installed.")
        print("Requires an installation of the following Python packages:")
        print("`pip install emoji pypandoc`")
        print("The output LaTeX file will need an `emoji` package as `\usepackage{emoji}`")
        print(f"Current command: python {sys.argv}")

        sys.exit(1)

    if len(sys.argv) == 2:
        input_md = sys.argv[1]
        # v1 initial, simple
        # output_tex = input_md.replace(".md", ".tex")
        # v2
        output_tex = md2latex_lib.md_to_tex_path(input_md)
    elif len(sys.argv) == 3:
        input_md = sys.argv[1]
        output_tex = sys.argv[2]


    md2latex_lib.md_to_latex_v3(input_md, output_tex)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/

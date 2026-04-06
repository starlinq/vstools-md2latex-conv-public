
import os
import pypandoc  # pip install pypandoc
import re
from pathlib import Path

import emoji



# The issue is that when converting emoji names from Markdown to LaTeX (using the emoji package),
# long names should use hyphens (-) instead of underscores (_). You can fix this by writing
# a small Python function that replaces underscores with hyphens in emoji names before generating the LaTeX code.
def markdown_to_latex_emoji(text):
    """
    Convert Markdown emoji (like :smiling_face_with_hearts:)
    into LaTeX emoji package format (\emoji{smiling-face-with-hearts}).
    """
    # Regex to match :emoji_name:
    pattern = r":([a-zA-Z0-9_]+):"

    def replacer(match):
        emoji_name = match.group(1)
        # Replace underscores with hyphens
        latex_name = emoji_name.replace("_", "-")
        return f"\\emoji{{{latex_name}}}"

    return re.sub(pattern, replacer, text)


def replace_all_emojis_v2(text: str) -> str:
    # Convert all emojis to aliases like :rocket:
    demojized = emoji.demojize(text)

    # Replace :alias: with \emoji{alias}
    # return re.sub(r":([a-zA-Z0-9_+\-]+):", r"\\emoji{\1}", demojized)
    return markdown_to_latex_emoji(demojized)


def replace_all_pandoc_unicode_escapes(latex_text: str) -> str:
    """
    Replace ANY Pandoc LaTeX Unicode escape, without regex.
    """

    for prefix in ("\\unichar{\"", "\\symbol{\""):
        start = 0
        while True:
            idx = latex_text.find(prefix, start)
            if idx == -1:
                break
            # Find the closing brace after the hex code
            end_idx = latex_text.find("}", idx + len(prefix))
            if end_idx == -1:
                break
            codepoint = latex_text[idx + len(prefix):end_idx]
            # Replace the whole sequence with \emoji{CODEPOINT}
            latex_text = (
                latex_text[:idx] +
                f"\\emoji{{{codepoint}}}" +
                latex_text[end_idx + 1:]
            )
            # Move past this replacement
            start = idx + len(f"\\emoji{{{codepoint}}}")
    return latex_text


def read_markdown_file(file_path):
    """
    Reads a Markdown file containing multibyte Unicode characters
    into a single string variable.

    :param file_path: Path to the Markdown file
    :return: File content as a string
    :raises FileNotFoundError: If the file does not exist
    :raises UnicodeDecodeError: If the file cannot be decoded with UTF-8
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            content = f.read()
        return content
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(
            f"Error decoding file '{file_path}' with UTF-8: {e}"
        )

def md_str_to_latex_str6(md_text: str) -> str:
    """
    Convert Markdown to LaTeX with full emoji replacement.
    Requires Pandoc installed.
    """
    # Pass 1: Replace shortcodes before Pandoc
    # preprocessed = replace_shortcodes(gfm_text)
    preprocessed = replace_all_emojis_v2(md_text)
    # preprocessed = replace_shortcodes(gfm_text)

    print("###########################################")
    print(preprocessed)
    print("###########################################")

    # Convert Markdown(+extensions) → LaTeX
    latex_output = pypandoc.convert_text(
        preprocessed,
        to="latex",
        format = "markdown+gfm_auto_identifiers+pipe_tables+raw_tex+tex_math_dollars"
    )

    # Pass 2: Replace Unicode emoji after Pandoc
    # latex_output = replace_unicode_emojis(latex_output)
    # latex_output = replace_pandoc_unicode_escapes(latex_output)
    # latex_output = replace_pandoc_unicode_escapes_no_regex(latex_output)

    latex_output = replace_all_pandoc_unicode_escapes(latex_output)

    # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    # print(latex_output)
    # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    return latex_output.strip()


def write_latex_file(latex_file_path, text):
    """
    Writes a LaTeX text to file.

    Args:
        latex_file_path (str): Path to the markdown file.

    Returns:
        str: File contents as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there is an error reading the file.
    """
    # if not os.path.isfile(file_path):
    #     raise FileNotFoundError(f"File not found: {file_path}")

    try:
        file = open(latex_file_path, "w", encoding="utf-8")
        # The output LaTeX file will need an emoji package as \usepackage{emoji}
        file.write("%\n")
        file.write("% To display emojis, this output LaTeX file needs an 'emoji' package as \\usepackage{emoji}\n")
        file.write("%\n")
        file.write(text)
        file.close()
    except Exception as e:
        raise IOError(f"Error writing file '{latex_file_path}': {e}")




def md_to_tex_path(md_file_path):
    """
    Convert a .md file path to a .tex file path.

    Args:
        md_file_path (str or Path): Path to the Markdown file.

    Returns:
        Path: Path with .tex extension.
    """
    try:
        path = Path(md_file_path)

        # Validate that the file has a .md extension
        if path.suffix.lower() != ".md":
            raise ValueError(f"Expected a .md file, got '{path.suffix}' instead.")

        # Replace extension with .tex
        return path.with_suffix(".tex")

    except Exception as e:
        print(f"Error: {e}")
        return None


# # Example usage
# md_path = "docs/example.md"
# tex_path = md_to_tex_path(md_path)
#
# if tex_path:
#     print(f"Converted path: {tex_path}")


def is_markdown_file(file_path: str) -> bool:
    """
    Check if the given path points to an existing Markdown file.
    Accepts .md and .markdown extensions (case-insensitive).
    """
    try:
        path = Path(file_path).expanduser().resolve()  # Expand ~ and get absolute path
    except Exception as e:
        print(f"Error resolving path: {e}")
        return False

    # Check if file exists and is a file
    if not path.is_file():
        print("The path does not point to an existing file.")
        return False

    # Check file extension (case-insensitive)
    return path.suffix.lower() in {".md", ".markdown"}


def md_to_latex_v3(input_file, output_file):
    """
    Convert a Markdown (+extensions) file to LaTeX using Pandoc.

    Args:
        input_file:  a markdown file path
        output_file: a latex file path

    Returns:

    """

    markdown_content = ""
    latex_output = ""

    # Validate file existence and type of the file
    if not is_markdown_file(input_file):
        print("❌ The input file is either missing or not a Markdown file.")
        # raise FileNotFoundError(f"Input file '{input_file}' not found.")
        return
    else:
        # ✅ The file exists and is a Markdown file.
        # read it into variable
        markdown_content = read_markdown_file(input_file)

        # print("*******************************************")
        # print(markdown_content)
        # print("*******************************************")


    try:

        # Convert
        latex_output = md_str_to_latex_str6(markdown_content)

        write_latex_file(output_file, latex_output)

        print("\n")

        print(f"✅ Conversion successful: '{output_file}' created.")

    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        raise e




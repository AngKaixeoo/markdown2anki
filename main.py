from datetime import datetime
import re
import markdown
import sys
import os
import hashlib
import base91

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(CURRENT_FOLDER, "output")
# INPUT_FILE = os.path.join(CURRENT_FOLDER, "input.md")

extensions = []
extension_configs = {}


def main():
    file = open(
        os.path.join(
            OUTPUT_FOLDER, f"{datetime.today().strftime('%Y%m%d_%H%M%S')}.txt"
        ),
        "w",
    )
    file.write("""#separator:tab\n#html:true\n#guid column:1\n""")
    for input_file in sys.argv[1:]:
        with open(input_file, "r") as f:
            content = f.read()
        cards = re.split(r"#+", content)
        for card in cards:
            if not card.strip():
                continue
            title, text_replaced = toAnki(card)
            guid = generate_deterministic_guid64(title)
            print(f"Processing card: {title} with GUID: {guid}")
            file.write(f"{guid}\t{title}\t{text_replaced}\n")


def toAnki(card: str) -> list[str, str]:
    if not card.strip():
        return []
    lines = card.strip().splitlines()
    title = lines[0].strip()
    description = "<br>".join(lines[1:]).strip()

    block_math: list[str] = []
    inline_math: list[str] = []

    def save_block_math(match: re.Match[str]) -> str:
        expression = match.group(1).strip()
        expression = re.sub(r"^(?:<br>\s*)+|(?:\s*<br>)+$", "", expression)
        block_math.append(expression)
        return f"ANKIBLOCKTOKEN{len(block_math) - 1}END"

    def save_inline_math(match: re.Match[str]) -> str:
        inline_math.append(match.group(1).strip())
        return f"ANKIINLINETOKEN{len(inline_math) - 1}END"

    description = re.sub(r"\$\$(.*?)\$\$", save_block_math, description, flags=re.DOTALL)
    description = re.sub(
        r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)",
        save_inline_math,
        description,
        flags=re.DOTALL,
    )
    text = (
        markdown.markdown(
            description, extensions=extensions, extension_configs=extension_configs
        )
        .replace("<p>", "")
        .replace("</p>", "")
        .replace("<strong>", "<b>")
        .replace("</strong>", "</b>")
        .replace("<em>", "<i>")
        .replace("</em>", "</i>")
    )

    for i, expr in enumerate(block_math):
        text = text.replace(
            f"ANKIBLOCKTOKEN{i}END", f'<anki-mathjax class="block">{expr}</anki-mathjax>'
        )

    for i, expr in enumerate(inline_math):
        text = text.replace(f"ANKIINLINETOKEN{i}END", f"<anki-mathjax>{expr}</anki-mathjax>")

    return [title, text]


def generate_deterministic_guid64(input_str: str) -> str:
    """
    Takes an input string, generates a deterministic 64bit integer
    via SHA-256, and returns a base91-encoded representation.
    """
    # 1. Hash the input string to get a unique, deterministic byte digest
    hash_digest = hashlib.sha256(input_str.encode()).digest()

    # 2. Convert the first 8 bytes (64 bits) of the hash to an integer
    # Using 'big' endian is standard, 'little' works too as long as it's consistent.
    guid64_int = int.from_bytes(hash_digest[:8], byteorder="big")

    # 3. Format the integer as bytes to be compatible with your base91 function
    # Your base91 function likely expects bytes. If it expects an int,
    # you might need to convert it differently.
    int_as_bytes = guid64_int.to_bytes(8, byteorder="big")

    # 4. Return the base91-encoded representation
    return base91.encode(int_as_bytes).replace('"', "?")


if __name__ == "__main__":
    main()

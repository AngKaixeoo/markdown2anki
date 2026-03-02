from datetime import date
import re
import markdown
import sys
import os

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(CURRENT_FOLDER, "output")
# INPUT_FILE = os.path.join(CURRENT_FOLDER, "input.md")


def main():
    file = open(os.path.join(OUTPUT_FOLDER, f"{date.today()}.txt"), "w")
    file.write("""#separator:tab\n#html:true\n#tags column:3\n""")
    for input_file in sys.argv[1:]:
        with open(input_file, "r") as f:
            content = f.read()
        cards = content.split("##")
        for card in cards:
            if not card.strip():
                continue
            title, text_replaced = toAnki(card)

            file.write(f"{title}\t{text_replaced}\t\n")


def toAnki(card: str) -> list[str, str]:
    if not card.strip():
        return []
    lines = card.strip().splitlines()
    title = lines[0].strip()
    description = (
        "\n".join(lines[1:])
        .strip()
        .replace("\n", "<br>")
        .replace("$$<br>", "$$")
        .replace("<br>$$", "$$")
    )
    html_description = (
        markdown.markdown(description).replace("<p>", "").replace("</p>", "")
    )
    text_replaced = re.sub(
        r"\$\$(.*?)\$\$", r"\[\1\]", html_description, flags=re.DOTALL
    )

    text_replaced = re.sub(r"\$(.*?)\$", r"\(\1\)", text_replaced)
    return [title, text_replaced]


if __name__ == "__main__":
    main()

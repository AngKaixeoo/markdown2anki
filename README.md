# Markdown2Anki

Markdown2Anki is a Python script that converts Markdown files into Anki importable files.
**Supported Markdown features include**:

- Header H2 only
- Math blocks (`$$ ... $$`)
- Math inline (`$ ... $`)

## Usage

clone this repository and run the following command:

```bash
uv run ./main.py "path/to/input1.md" "path/to/input2.md" ...
```

or

```bash
python main.py "path/to/input1.md" "path/to/input2.md" ...
```

### Markdown file example

```markdown
## Question 1

Answer 1
Answer _2_

$$
1+1=2
$$
```

### Output

The output (importable in Anki) is placed in the `output/` directory.

## Importing into Anki

1. Open Anki and go to `File > Import`.
2. Select the generated file from the `output/` directory.
3. Change the import settings on your need and click `Import`.

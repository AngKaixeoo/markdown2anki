# Markdown2Anki

Markdown2Anki is a Python script that converts Markdown files into Anki importable files. (Only support Basic note)
**Supported Markdown features include**:

- Header as Title/Question
- Italic and Bold text
- Math blocks (`$$ ... $$`)
- Math inline (`$ ... $`)

## Usage

Clone this repository, install the dependencies, and run the following command:

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

$$
1+1=2
$$

## Question 2

Answer 2

$$
\frac{2}{4} = \frac{1}{2}
$$
```

### Output

The output (importable in Anki) is placed in the `output/` directory.

## Importing into Anki

1. Open Anki and go to `File > Import`.
2. Select the generated file from the `output/` directory.
3. Change the import settings to your needs and click `Import`.

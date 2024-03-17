import click
import sys
import tiktoken
import string
import os


def run(token_count, model, file, tail):
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(file.read())
    selected_tokens = tokens[-token_count:] if tail else tokens[:token_count]
    click.echo(enc.decode(selected_tokens))


@click.group
def cli():
    """Extract the head or tail of text based on GPT tokens."""
    pass


def add_command(func, name):
    help_text = (
        f"Prints the {'last' if name == 'tail' else 'first'} N tokens from the input."
    )

    @cli.command(name=name, help=help_text)
    @click.option(
        "-n",
        "--token-count",
        default=100,
        help="Number of tokens to include in the output.",
    )
    @click.option(
        "-m", "--model", default="gpt-4", help="GPT model to use for tokenization."
    )
    @click.argument("file", type=click.File("r"), default=sys.stdin)
    def command(token_count, model, file):
        run(token_count, model, file, name == "tail")


add_command(run, "head")
add_command(run, "tail")


@cli.command
@click.option(
    "-n", "--token-count", default=100, help="Maximum token length for each split part."
)
@click.option(
    "-m", "--model", default="gpt-4", help="GPT model to use for tokenization."
)
@click.option("--overwrite", is_flag=True, help="Overwrite existing files.")
@click.argument("file", type=click.File("r"), default=sys.stdin)
def split(token_count, model, file, overwrite):
    """Splits the input text into multiple files."""
    enc = tiktoken.encoding_for_model(model)
    content = file.read()
    tokens = enc.encode(content)
    prefix = "x"

    for i, start in enumerate(range(0, len(tokens), token_count), start=0):
        file_suffix = (string.ascii_lowercase + string.ascii_lowercase)[i // 26] + (
            string.ascii_lowercase
        )[i % 26]
        filename = f"{prefix}{file_suffix}"

        if not overwrite and os.path.exists(filename):
            raise FileExistsError(
                f"File {filename} already exists. Use --overwrite to ignore."
            )

        with open(filename, "w") as file:
            file.write(enc.decode(tokens[start : start + token_count]))


@cli.command
@click.option(
    "-m", "--model", default="gpt-4", help="GPT model to use for tokenization."
)
@click.argument("file", type=click.File("r"), default=sys.stdin)
def count(model, file):
    """Prints the number of tokens in the input."""
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(file.read())
    click.echo(len(tokens))


@cli.command
@click.option(
    "-m", "--model", default="gpt-4", help="GPT model to use for tokenization."
)
@click.argument("file", type=click.File("r"), default=sys.stdin)
def dump(model, file):
    """Dumps the tokens and their text representations."""
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(file.read())
    for token in tokens:
        token_text = enc.decode([token])
        click.echo(f"{token}\t{repr(token_text)}")

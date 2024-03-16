import click
import sys
import tiktoken


def process_input(token_count, model, input_stream, tail):
    enc = tiktoken.encoding_for_model(model)
    text = input_stream.read()
    tokens = enc.encode(text)
    selected_tokens = tokens[-token_count:] if tail else tokens[:token_count]
    click.echo(enc.decode(selected_tokens))


def run(token_count, model, files, tail):
    if files:
        for file in files:
            process_input(token_count, model, file, tail)
    else:
        process_input(token_count, model, sys.stdin, tail)


@click.group
def cli():
    """Extract the head or tail of text based on GPT tokens."""
    pass


@cli.command
@click.option(
    "-n",
    "--token-count",
    default=100,
    help="Number of tokens to include in the output.",
)
@click.option(
    "-m", "--model", default="gpt-4", help="GPT model to use for tokenization."
)
@click.argument("files", type=click.File("r"), nargs=-1, required=False)
def head(token_count, model, files):
    run(token_count, model, files, False)


@cli.command
@click.option(
    "-n",
    "--token-count",
    default=100,
    help="Number of tokens to include in the output.",
)
@click.option(
    "-m", "--model", default="gpt-4", help="GPT model to use for tokenization."
)
@click.argument("files", type=click.File("r"), nargs=-1, required=False)
def tail(token_count, model, files):
    run(token_count, model, files, True)


if __name__ == "__main__":
    cli()

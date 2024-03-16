import click
import sys
import tiktoken


def run(token_count, model, input_stream, tail):
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(input_stream.read())
    selected_tokens = tokens[-token_count:] if tail else tokens[:token_count]
    click.echo(enc.decode(selected_tokens))


@click.group
def cli():
    """Extract the head or tail of text based on GPT tokens."""
    pass


def add_command(func, name):
    @cli.command(name=name)
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

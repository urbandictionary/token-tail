# Token-Tail

A command-line tool that mimics the Unix `head` and `tail` commands but operates based on GPT-defined tokens, using the TikToken tokenizer.

It allows users to extract the first or last N tokens from text input, which can be passed via files or STDIN.

```
Usage: -c [OPTIONS] COMMAND [ARGS]...

  Extract the head or tail of text based on GPT tokens.

Options:
  --help  Show this message and exit.

Commands:
  count  Prints the number of tokens in the input.
  head   Prints the first N tokens from the input.
  split  Splits the input text into multiple files.
  tail   Prints the last N tokens from the input.
```
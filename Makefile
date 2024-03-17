head:
	cat input | python -c 'import token_tail.main; token_tail.main.cli()' head

tail:
	cat input | python -c 'import token_tail.main; token_tail.main.cli()' tail

install:
	pip install .
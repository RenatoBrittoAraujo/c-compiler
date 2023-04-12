build:
# gcc main.c

run: build
	@cat $(F) > target.c
	@python3 ccompiler.py

test:
	gcc $(F) -o test
	./test && rm test
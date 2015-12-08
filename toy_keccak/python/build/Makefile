# Makefile for build/

all:
	python generate_input.py
	python create_digest.py input.txt output.txt
	python find_duplicates.py

duplicate:
	python find_duplicates.py

clean:
	rm -rf *.txt
	rm -rf *.py
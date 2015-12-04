# Makefile 

default: clean build run

PHONY: build
build:
	mkdir build/
	cp *.py build/
	cp *.txt build/
	rm -rf build/Notes.txt

PHONY: duplicate
duplicate: 
	cp find_duplicates.py build/ && cd build && python find_duplicates.py

PHONY: run
run:
	cd build && python generate_input.py && python create_digest.py input.txt output.txt && python find_duplicates.py

PHONY: clean
clean:
	rm -rf build/
	rm -rf *.pyc
	rm -rf output.txt
.PHONY: build run

build:
	clang -fopenmp src/iter_dist.c -o bin/iter_dist -lomp -lm

run: build
	./bin/iter_dist 128 4
	python utils/visualise.py

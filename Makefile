
.PHONY: all clean upload

all: clean
	./setup.py sdist
	./setup.py bdist_wheel --universal

upload: all
	@type twine &>/dev/null || pip install --user twine
	twine upload -u con-f-use ./dist/*

clean:
	rm -rf build/ dist/ *.egg-info/ pip-wheel-metadata/

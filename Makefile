.PHONY: develop sdist sphinx-compile sphinx upload pushcode \
		push-googlecode push-bitbucket push-github clean

# Setup virtual environment under pagd-env/ directory. And installs sphinx
# generator package.
develop :
	@rm -rf pagd-env
	@echo "Setting up virtual environment for python 3.x ..."
	@virtualenv --python=python3.2 pa-env
	@bash -c "source pa-env/bin/activate ; python ./setup.py develop"
	@bash -c "source pa-env/bin/activate ; easy_install-3.2 sphinx"

# Generate source distribution. This is the command used to generate the
# public distribution package.
sdist :
	python ./setup.py sdist

# Generate sphinx documentation.
sphinx-compile :
	pa -w confdoc -p pagd -o docs/configuration.rst
	cp README.rst docs/index.rst
	cp CHANGELOG.rst docs/
	cat docs/index.rst.inc >> docs/index.rst
	rm -rf docs/_build/html/
	make -C docs html

# Generate sphinx documentation and zip the same for package upload.
sphinx : sphinx-compile
	cd docs/_build/html; zip -r pagd.sphinxdoc.zip ./

# Upload package to python cheese shop (pypi).
upload :
	python ./setup.py sdist register -r http://www.python.org/pypi upload -r http://www.python.org/pypi
	
# Push code to repositories.
pushcode: push-github 

push-github:
	hg bookmark -f -r default master
	hg push git+ssh://git@github.com:prataprc/pagd.git

cleandoc :
	rm -rf docs/_build/*

clean :
	rm -rf docs/_build;
	rm -rf dist;
	rm -rf pagd.egg-info/;
	rm -rf `find ./ -name parsetyrtab.py`;
	rm -rf `find ./ -name lextyrtab.py`;
	rm -rf `find ./ -name "*.pyc"`;
	rm -rf `find ./ -name "yacctab.py"`;
	rm -rf `find ./ -name "lextab.py"`;

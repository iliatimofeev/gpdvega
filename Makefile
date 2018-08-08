all: install

install:
	python setup.py install

test :
	python -m pytest --pyargs --doctest-modules gpdvega


test-coverage:
	python -m pytest --pyargs --doctest-modules --cov=gpdvega --cov-report term gpdvega

test-coverage-html:
	python -m pytest --pyargs --doctest-modules --cov=gpdvega --cov-report html gpdvega

help:
	 $(MAKE) -C doc publish

publish:
	rm -rf dist build
	python setup.py sdist bdist_wheel
	twine upload dist/*



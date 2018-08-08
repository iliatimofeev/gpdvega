all: install

install:
	python setup.py install

test :
	python -m pytest --pyargs --doctest-modules gpdvega


test-coverage:
	python -m pytest --pyargs --doctest-modules --cov=altair --cov-report term gpdvega

test-coverage-html:
	python -m pytest --pyargs --doctest-modules --cov=altair --cov-report html gpdvega

publish:
	rm -r dist build
	python setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*



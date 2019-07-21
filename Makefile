mypy:  ## run mypy
	mypy src

flake8:  ## run flake8
	flake8 src

yamllint:  # run yamllint
	yamllint .

lint: mypy flake8 yamllint  # run all linters

unittests:  ## run pytest with coverage and -s flag for debugging
	pytest --cov=koles tests/ --cov-branch -s

coverage_report:  ## display pytest coverage report
	coverage report

coverage_html:  ## create html coverage report and open it in the default browser
	coverage html
	xdg-open htmlcov/index.html




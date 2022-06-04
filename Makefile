SHELL = /bin/bash

help:
	@echo "Targets:"
	@echo " "
	@echo "- make black"
	@echo "- make reqs"
	@echo "- make run"
	@echo " "

black:
	python3 -m black --skip-string-normalization .

reqs:
	poetry export -f requirements.txt --output requirements.txt

run:
	uvicorn super_app.__main__:app --host 0.0.0.0 --port 8771
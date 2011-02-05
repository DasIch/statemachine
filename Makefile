help:
	@echo "Possible targets:"
	@echo "  doc         - builds the html documentation"
	@echo "  test        - runs all tests"
	@echo "  view-doc    - opens the documentation in your browser"
	@echo "  clean-doc   - deletes the build files"
	@echo "  clean-files - deletes bytecode files"
	@echo "  clean       - calls all clean-* targets"

doc:
	@make -C docs/ html

test:
	@tox

view-doc: doc
	@python -c "import webbrowser; webbrowser.open('docs/_build/html/index.html')"
clean-doc:
	@make -C docs/ clean > /dev/null

clean-files:
	@find . -iname "*.pyc" -delete

clean-test:
	@rm -r .tox

clean: clean-doc clean-files clean-test

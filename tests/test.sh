# Run tests and then show coverage report (only if no errors):
python -m coverage run --source="." -m unittest discover -s tests -v || exit

# Compute and show coverage:
coverage report -m --omit="tests/*.py,*/__init__.py"

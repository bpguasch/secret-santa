# Delete the previous distribution files
rm -rf dist

# Build this package version
python3 -m build

# Create the Lambda layer
rm -rf "python"
mkdir "python"
unzip dist/*.whl -d "python"
zip -r python.zip "python"
rm -rf "python"

# Upload the package to TestPyPi
#python3 -m twine upload --repository testpypi dist/*

# Upload the package to PyPi
#python3 -m twine upload dist/*
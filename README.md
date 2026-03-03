# Python Project Template Repository

This is a template repository for a Python project. Feel free to use and edit
this repository (including this file) for your needs. Below, find some
instructions and tips for using this template repository.

## To-do:
- fill out README
- currently data must be downloaded manually, and then the paths need to be changed in the txt_csv_converter.py file -> add 'requests' package here to automate this process

## How to Use

-> data file is too big to upload to github
--> need to include directions for how to download the data from the website and probably have a script to run to turn it into an excel spreadsheet?

Click on the "Use this template" button in the top right corner to create a new
repository based on this template. If this is for a class project, we ask that
you keep it in the `olincollege` GitHub organization, and that you refrain from
keeping the repository private. This will ensure that relevant people can access
your repository for assessment, etc.

## Requirements

The `requirements.txt` file is blank and should be filled out with any project
dependencies. There is a Python package called `pipreqs` that autogenerates the
contents of the `requirements.txt` file based on the `import` statements in your
`.py` files. To get this, run

```
pip install pipreqs
```

Then, in the root of your project repository, run:

```
pipreqs --mode compat
```

If you already have a `requirements.txt`, the above command will ask you to
rerun the command with the `--force` flag to overwrite it.

# Metdesk JC
 
A command line driven script that reads a local CSV file from disk and outputs basic statistics. 

# Installation
Install action MetDesk (JC) uses `pip` and `setuptools` the recommended install method is as follows. 

```
pip install -i https://test.pypi.org/simple/ metdesk-jc
```

# Usage
If a CSV file location is not specified Metdesk (JC) will look for a file called "data" in the same directory that it is run in.
```
metdesk-jc
```

If you want to specifiy a file and it's location then use the `--csv` argument.

```
metdesk-jc --csv ./subdir/interesting-data
```

Other commands can be seen by using `--help`, there are no required arguments as all have a default value that can be adjusted.

# Development 
Activate your virtual environment and install of the the development dependencies. 

```py
pip install -r requirements-dev.txt
```

Build the package locally

```py 
py -m build
pip install -e .
```
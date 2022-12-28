# Metdesk JC
 
A command line driven script that reads a local CSV file from disk and outputs basic statistics. 

# Installation
Install action MetDesk (JC) uses `pip` and `setuptools` the recommneded install method is as follows. 

# Usage
If a CSV file location is not specified Metdek (JC) will look for a file called "data" in the same directory that it is run in.
```
metdesk-jc
```

If you want to specifiy a file and it's location then use the `--csv` argument.

```
metdesk-jc --csv ./subdir/intresting-data
```

Other commands can be seen by using `--help`, there are no required argments as all have a default value that can be adjusted.

# Development 
Activate your virtual environment and install of the the developemnt dependancies. 

```py
pip install -r requirements-dev.txt
```

Build the package locally

```py 
py -m build
pip install -e .
```



## Intall the package

```
py setup.py install
```

## Build 

```
py -m build
```
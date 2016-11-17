# TYLER


**Tyler** is just a simple "tail -f" command written in Python that can be used like a module to be integrated in 
own projects or as a standalone command from the command line (expecially useful on Windows
where tail command does not exists).

## INSTALL

To install Tyler simply use pip

````Bash
$ pip install pytyler
````

## USAGE

### From the command line

````Bash
c:\tyler prova.txt
````

### As a module

````Python
import tyler

my_file = tyler.Tyler('filename_to_be_tailed.log')
while True:
    for line in my_file:
        # insert here whatever you whatn to do with the read line
````        
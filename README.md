# wrex-py
[WREX](https://github.com/mikiTesf/wrex) in Python. `wrex-py` does not come with a user interface but it's CLI is easy and intuitive.
<br/><br/>
### How to use **WREX-Py**?

```
usage: wrex-py [-h] [-s] [-v] path [path ...]

    wrex-py (from the original wrex written in Java) extracts the presentations in a
    Meeting Workbook and prepares an Excel document making assignments easy for the
    responsible Elder or Ministerial Servant. It is mandatory that all files passed
    to wrex-py be in the EPUB format.

positional arguments:
  path               path to a meeting workbook EPUB

optional arguments:
  -h, --help         show this help message and exit
  -s, --single-hall  don't insert hall dividing labels above presentation rows
                     (bible reading and improve in ministry)
  -v, --version      show program's version number and exit

Give the Java version a try. Its faster!
```
### Contribution
Contributions are always welcome. One way is to translate the values in the JSON files in [language/](./language) to the languages indicated by the file names.
Right now, all values in almost all the files are written in English.

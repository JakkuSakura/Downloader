# Downloader

a downloader based on python

## positional arguments

```text
  download_file         The file(s) or the list(s) you want to download
```
## optional arguments
```text
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -l, --list            Assume your files as downloading list(s)
  -d DEST, --dest DEST  The base path where you want to save your file(s)
```
## Download list
### format
each line represents ONE file
```text
https://www.foo.com/
```

Append the path or filename if you want to save it somewhere

```text
http://www.baidu.com/index.html baidu.html
http://www.4399.com/ fall/
```
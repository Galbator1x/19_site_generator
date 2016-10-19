19_site_generator
=================

This script takes the .md files from the folder "article", and convert 
them to html and creates a special index page index.html. After each 
commit script automatically rebuilds the [site](https://galbator1x.github.io/galbator1x.github.io-site-generator/).

Usage
-----

Put 'post-commit' into ./git/hooks/

```
~$ chmod +x .git/hooks/post-commit
~$ pip install -r requirements.txt
~$ python3 site_generator.py 
```

Requirements
------------

- Jinja2==2.8
- Markdown==2.6.7
- GitPython==2.0.9

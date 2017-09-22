# verbs-in-python-functions
# ABOUT
<b>verbs_in_functions.py</b> finds the .py files in the folder and displays a list of the most used verbs in the functions.

# USAGE
<pre><code>
python verbs_in_functions.py [path] [-f: NUMBER OF FILES] [-t: TOP NUMBER OF VERBS]
</code></pre>

# EXAMPLE
<pre><code>
python verbs_in_functions.py path -f 100 -t 5
found 100 file(s), valid 100 file(s)
found 1798 function(s) of which 93 verb(s), 13 unique
top 5 verbs are:
('get', 60)
('find', 11)
('run', 5)
('add', 5)
('replace', 3)
</code></pre>

# DEPENDENCIES
This has been tested with Python 3.6.2. The required module <b>pos_tag</b> from package <b>nltk</b> ver 3.2.4.

# LICENSE
MIT License

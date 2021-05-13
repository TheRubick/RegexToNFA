# RegexToNFA
## Description
Simple code to convert user input **regex** ***"regular expression"*** into **NFA** ***"non deterministic finite automata"***. 

### The code handles the following regex symbols:
* **oring** either by using + , | symbols
* **concatenating** like AB
* **zero or more occurrence** by using * symbol

### Some restrictions on the user input:
* The valid set of characters are : **[a-zA-Z0-9\(\)]**, any other character will be considered invalid like **$,^,etc..**
* Also invalid sequences will be taken in consideration like: **\*\*,|*,)(etc..**

### Prerequisities to run the code:
```
sudo apt-get install graphviz
pip3 install graphviz
```

### Pipeline of the code
* First it validates and checks the user input regex, if it is valid it will process it otherwise not

* Second it will work on top-down approach to build graph structure by merging nodes until they converge to **superNode** ***"the biggest abstract node"***

* Third after building the graph of nodes, it will create NFA graph then plot the resulted NFA in a PDF file.
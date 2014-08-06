FDU ACM Training Report Generator
=================================

For those who is not familar with latex.

How to use
----------

Write the source with the specification, and run `python genfatr`


How to manage source
--------------------
```
-----source-root/
    |
	|-----meta.json     # date, team name, members, title, author, report file name
	|-----overview.md   # section 概况
	|-----process.md	# section 过程
	|-----problems/		# section 题解报告
	|	 |
    |    |-----meta.json        # Problems list, in order
	|	 |-----problemA.json	# title, members, situation
	|	 |-----problemA.md		# the solution of problemA
	|	 |-----problemB.json
	|	 |-----problemB.md
	|	 |...
	|
	|-----summary.md	# section 总结
```

Dependencies
------------

*   python 2.7
*   xelatex

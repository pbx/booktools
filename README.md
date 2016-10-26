A little-known bit of trivia about our book, [Python Web Development with Django][1]: we wrote the manuscript in [Markdown][].

I think it was my idea. One of the major motivations for using a text-based format (versus the unfortunate _de facto_ standard, Microsoft Word) was integration with good developer tools and workflow. 

Our manuscript and all our project code was in a Subversion repo, so each author always had the latest updates. HTML generated from the Markdown files was great for generating nice printed/printable output too. 

We could have used any number of similar formats: Markdown, Textile, reStructuredText. If we did it again we'd probably use [reST][] plus [Sphinx][]. That would grant all the same advantages, plus give us a little more formatting flexibility and tool support.

This workflow enabled certain kinds of programmatic action on our text, notably two things: automated testing of the interactive examples within the text, and automated extraction of example snippets from source code files.

There's a little documentation in the docstrings of the scripts. Here's the summary:

* To test code snippets in the manuscript file: `test_snippets.py example/text.txt`
* To extract code from source files into the manuscript file: `try_excerpt.py example/text.txt`

Authors, make use of this if you can — or maybe even better, take inspiration from the idea and implement a system of your own. 

— Paul Bissex, September 2010

[1]: http://withdjango.com/
[markdown]: http://daringfireball.net/projects/markdown/
[sphinx]: http://sphinx.pocoo.org/
[rest]: http://docutils.sourceforge.net/rst.html
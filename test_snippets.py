#!/usr/bin/env python
"""
Python snippet tester for Markdown manuscripts

This tester executes doctests in the Markdown file(s) passed as arguments.

Precede tests that need to be skipped with a comment like this:

    <!-- test:skip (description of why it's being skipped) -->
     
This comment should not be indented, and a blank line after it is required 
to preserve Markdown parsing. No closing marker is needed; the blank line 
after the code block is sufficient. Skipped test lines are printed to the 
console.
"""

import doctest
import sys

def remove_skipped_examples(lines):
    """Remove examples preceded by <!-- test:skip -->"""
    cleaned_text = skipped_text = ""
    for num, line in enumerate(lines):
        if line.startswith("<!-- test:skip"):
            skipped_text += "\nSkipping @ line %s: %s\n" % (num, line[14:-4])
            line = lines.next() # consume leading blank line
            line = lines.next() # get first line of test
            while line.strip():
                skipped_text += line.rstrip() + "\n"
                line = lines.next()
            line = ""
        cleaned_text += line
    skipped_text += "\n"
    return cleaned_text, skipped_text

def checkfiles(files):
    """Check doctest examples embedded in provided files"""
    for f in files:
        lines = iter(open(f).readlines())
        cleaned_text, skipped_text = remove_skipped_examples(lines)
        parser = doctest.DocTestParser()
        test = parser.get_doctest(cleaned_text, {}, f, f, 1)
        if len(test.examples):
            print "\nTesting %s" % f
            if skipped_text:
                print skipped_text
            runner = doctest.DocTestRunner(optionflags=doctest.NORMALIZE_WHITESPACE + 
                doctest.ELLIPSIS)
            runner.run(test)
            print
            runner.summarize(verbose=True)
        else:
            print "\nNo tests in %s" % f
        
if __name__ == "__main__":
    files = sys.argv[1:]
    if files:
        checkfiles(files)
    else:
        print "Please provide one or more filenames."

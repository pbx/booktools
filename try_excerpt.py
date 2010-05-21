#!/usr/bin/env python
"""
This script inserts code snippets into Markdown or HTML files.

In the source files, it looks for comments like this:

    <!-- excerpt foo/bar/baz.py#1 -->
    
    As you can see from the above...
    
Which corresponds to a marked section of baz.py like this:

    # begin excerpt 1
    print "This will be extracted"
    # end excerpt 1
    print "And this will not"

The source file will be changed thus:

    <!-- excerpt foo/bar/baz.py#1 -->

        print "This will be extracted"

    As you can see from the above...
    
When run on files where the snippets have already been inserted, 
it will endeavor to replace them cleanly. There are no particular
guarantees it will be successful at this, hence the "try" part 
of the name :)
"""

import os
import re
import sys
import subprocess

LOOKING_STATE, GATHERING_STATE = 1, 2        

def get_excerpt(path, tag):
    """Get the tagged excerpt from the source file"""
    try:
        lines = file(path)
    except IOError:
        raise ValueError, "Can't open file at %s" % path
    begin_markers = ["# begin excerpt %s" % tag, "{# begin excerpt %s #}" % tag]
    end_markers = ["# end excerpt %s" % tag, "{# end excerpt %s #}" % tag]
    state = LOOKING_STATE
    excerpt = []
    for line in lines:
        if line.strip() in end_markers:
            break
        if state == GATHERING_STATE:
            excerpt.append("    " + line)
        if line.strip() in begin_markers:
            state = GATHERING_STATE
    if excerpt:
        return "".join(excerpt)
    else:
        raise ValueError, "Tag '%s' not found in source file '%s'" % (tag, source_file)


def update_excerpts(textfile_path):
    lines = file(textfile_path)
    output = []
    comment = re.compile("^<!\-\- excerpt (.+)#(.+) \-\->")
    for line in lines:
        output.append(line)
        match = comment.match(line)        
        if match:
            print "Found excerpt: %s#%s" % match.groups()
            # Discard version that's currently at this spot.
            # Start by skipping two lines, so that a blank line below
            # the excerpt directive doesn't prematurely end this.
            output.append(lines.next())
            line = lines.next()
            while line[:4] <= "    ":
                line = lines.next()
            sourcefile, tag = match.groups()
            source_file_path = os.path.join(os.path.dirname(textfile_path), sourcefile)
            excerpt = get_excerpt(source_file_path, tag) + "\n"
            output.append(excerpt)
            output.append(line)
    return "".join(output)

def update_excerpts_in_file(textfile_path):
    """
    Check for example references embedded in provided file, 
    then (safely) update that file.
    """
    print "Processing", textfile_path
    result = update_excerpts(textfile_path)
    newname = textfile_path + "_"
    newfile = open(newname, "w")
    newfile.write(result)
    newfile.close()
    diff = subprocess.call(["diff", "-u", textfile_path, newname])
    if diff:
        ok = raw_input("OK? ")
        if ok.lower() == "y":
            bak = textfile_path + ".bak"
            os.rename(textfile_path, bak)
            os.rename(newname, textfile_path)
            os.remove(bak)
            print "Updated file."
        else:
            os.remove(newname)
            print "Cancelled update."
    else:
        os.remove(newname)
        print "No changes needed."
         
           
if __name__ == "__main__":
    try:
        path = os.path.abspath(sys.argv[1])
        update_excerpts_in_file(path)
    except KeyError:
        print "Please provide a filename."

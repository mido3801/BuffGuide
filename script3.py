import re

with open('test3trimmed.txt','w') as outfile:
    with open('test3.txt','r') as infile:
        for line in infile:
            if line.strip():
                outfile.write(line)

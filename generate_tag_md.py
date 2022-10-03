#!/usr/bin/env python3
# coding: utf-8

import os
import re
import shutil

tag_page_content = '''---
layout: tagpage
tag: {tag}
robots: noindex
---'''

tag_list = []
tag_dir = "tag"
posts_dir = "_posts"
md_ext = ('.md', '.markdown')
rgxp = r'---[\s\S]*?tags:(.*)[\s\S]*?---'

# wipe up and recreate tag dir
shutil.rmtree(tag_dir, ignore_errors=True)
os.makedirs(tag_dir)

# Get unique tags from post
for post in os.listdir(posts_dir):
    if post.endswith(md_ext):
        p = open(os.path.join(posts_dir, post))
        s = re.search(rgxp, p.read(), re.MULTILINE)
        if s:
            tag_list = list(set(tag_list + s.group(1).strip().split()))

# Create tag pages
for tag in tag_list:
    with  open(os.path.join(tag_dir, tag+".md"), 'w') as f:
        f.write(tag_page_content.format(tag=tag))

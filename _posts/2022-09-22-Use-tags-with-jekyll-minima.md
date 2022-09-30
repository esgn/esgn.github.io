---
layout: post
title:  "Using tags with jekyll minima v2 default theme"
date:   2022-09-22 9:14:43 +0200
tags: jekyll
description: How to support tags and tags browsing in Jekyll default minima v2 theme using GitHub pages.
---

I was looking for a simple way to write notes while working on different projects. I never touched a Ruby project before, so why not give [Jekyll](https://jekyllrb.com/){:target="_blank"} a try. The default `minima` theme is good enough for displaying blog posts. The only missing feature was the ability to tag posts and browse posts using tags while using GitHub pages. 

Some people already tried their hands on this feature and they were very useful introductions to the subject:
* <http://longqian.me/2017/02/09/github-jekyll-tag/>{:target="_blank"}
* <https://rfong.github.io/rflog/2020/02/28/jekyll-tags/>{:target="_blank"}
* <http://www.jasonemiller.org/2020/12/23/tagging-posts-in-jekyll-minima.html>{:target="_blank"}

Be aware this post uses the minima theme in its v2.5.1 version (current release at time of writing). A v3 version is brewing here <https://github.com/jekyll/minima>{:target="_blank"} but a release is still pending.

## Jekyll theme

Jekyll uses the [Liquid templating language](https://shopify.github.io/liquid/){:target="_blank"} created by [Shopify](https://www.shopify.com/){:target="_blank"} written in [Ruby](https://www.ruby-lang.org/en/){:target="_blank"} to process templates.

Overriding Jekyll theme defaults is explained in its official documentation [here](http://jekyllrb.com/docs/themes/#overriding-theme-defaults){:target="_blank"}. It's as simple as: copy-paste the file from the original theme you wish to modify and put it either in `_layouts/` or `_includes/` depending where the file was originaly situated.

## Adding tags to post

Jekyll extracts post metadata from [Front Matter](https://jekyllrb.com/docs/front-matter/){:target="_blank"} header. Front Matter variables are extensible and can be access via Liquid. So let's add a `tags` variable to our post Front Matter header. We'll stick to `[\d\w-]+` for tag naming.

{% highlight markdown %}
{% raw %}
---
layout: post
title:  "Using tags with jekyll minima default theme"
date:   2022-09-22 9:14:43 +0200
tags: jekyll liquid another-tag
---
{% endraw %}
{% endhighlight %}

Then we need to copy the original `post.html` layout file from minima theme to a `_layouts/` directory local to our project and edit it as follows (copy paste the block between HTML comments):

{% highlight html %}
{% raw %}
 <header class="post-header">
    ...
      {%- if page.author -%}
      • <span itemprop="author" itemscope itemtype="http://schema.org/Person">
          <span class="p-author h-card" itemprop="name">{{ page.author }}</span>
        </span>
      {%- endif -%}

      <!-- Add tags to post header start -->
      {% if page.tags.size > 0 %}
      <span itemprop="keywords">
        {% for tag in page.tags %}
        <a href="{{ site.baseurl }}/tag/{{ tag }}">
          <code>
            <small>{{ tag }}</small>
          </code>
        </a>
        {% endfor %}
      </span>
      {% endif %}
      <!-- Add tags to post header end -->

    </p>
  </header>
    ...
{% endraw %}
{% endhighlight %}

Here we create, for each tag present in the post header, a link to a tag page (yet to be defined). Pretty straightforward.

## Creating tag page template

Let's define the template for the tag page that will display all the posts available with a given tag. We do this by adding a `tagpage.html` file with the following code in the `_layouts/` directory of our project.

{% highlight html %}
{% raw %}
---
layout: default
---

<div class="post">
  <h1>Tag: {{ page.tag }}</h1>
  <div>
    <ul>
      {% for post in site.posts %}
        {% if post.tags contains page.tag %}
        <li>
        <a href="{{ post.url }}">{{ post.title }}</a> ({{ post.date | date_to_string }})
        </li>
        {% endif %}
      {% endfor %}
    </ul>
  </div>
</div>
{% endraw %}
{% endhighlight %}

Here we simply iterate over all site posts and display the ones containing the tag targeted by the page.

## Creating markdown page for each tag

Finaly we have to create a `tag/` directory in our project and put a markdown file in it for each tag used on our website. Of course we're not going to do this manually.

Below is a trimmed down version of existing scripts using regular expression to grab the tags in post files.

{% highlight python %}
{% raw %}
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
rgxp = r'---(?:.|\n)*^tags\s*:(.*)$(?:.|\n)*---'

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

# Create tag markdown pages
for tag in tag_list:
    with  open(os.path.join(tag_dir, tag+".md"), 'w') as f:
        f.write(tag_page_content.format(tag=tag))
{% endraw %}
{% endhighlight %}


## Adding tag cloud

Displaying the list of available tags on the tag pages seems like a reasonable idea. Former solutions rely on a big block of code. It can actually be written more effectively by using Liquid filters.  

To add the list of all available tags to the tag pages, just append the following block before the end of the main `<div>` in `tagpage.html`

{% highlight html %}
{% raw %}
<div class="post">

  ...

  <!-- Add tag cloud start -->
  <h2>All tags</h2>
  {% assign tags = site.posts | map: "tags" | compact | uniq | sort %}
  {% for tag in tags %}
    <a href="/tag/{{ tag }}"><code><small>{{ tag }}</small></code></a>
  {% endfor %}
  <!-- Add tag cloud end -->

</div>
{% endraw %}
{% endhighlight %}

`map` creates a list from all tags in `site.posts`, `compact` removes `nil` values from the list and `uniq` removes duplicates from the list. `sort` simply sort the resulting list. You may want to have a look at [Liquid filters](https://shopify.github.io/liquid/filters/){:target="_blank"} to discover more useful features of Liquid.


## Adding tag to home page post list

As a final touch to this patch, I also wanted tags to be directly visible in the post listings on the home page. Once again, we just have to copy-paste the original `home.html` in `_layouts/` and add the following snippet to it (see code between HTML comments).

{% highlight html %}
{% raw %}
{%- if site.posts.size > 0 -%}
  <h2 class="post-list-heading">{{ page.list_title | default: "Posts" }}</h2>
  <ul class="post-list">
    {%- for post in site.posts -%}
    <li>
      {%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
      <span class="post-meta">{{ post.date | date: date_format }}</span>

      <!-- display tags in post list start-->
      {% if post.tags.size > 0 %}
        <span class="post-meta"></span>
          {% for tag in post.tags %}
          <a href="{{ site.baseurl }}/tag/{{ tag }}">
            <code>
              <small>{{ tag }}</small>
            </code>
          </a>
          {% endfor %}
        </span>
      {% endif %}
      <!-- display tags in post list end-->

      <h3>
        <a class="post-link" href="{{ post.url | relative_url }}">
          {{ post.title | escape }}
        </a>
      </h3>
        ...
{% endraw %}
{% endhighlight %}

## Conclusion

For more context about this solution, you may want to have a look to this website [repository](https://github.com/esgn/esgn.github.io).

# -*- coding: utf-8 -*-
from wordpress_xmlrpc import Client, WordPressPost, WordPressTerm
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
import argparse
import feedparser
import os

__all__ = ["Client"]

def entry_to_wppost(entry):
    post             = WordPressPost()
    # Convert entry values to Post value
    post.user        = entry.author
    post.date        = entry.published_parsed
    post.post_status = "draft"
    post.title       = entry.title
    post.content     = entry.content[0].value
    post.excerpt     = entry.summary
    post.link        = entry.link
    """
    # Create a categorie with the first tag item
    category = WordPressTerm()
    if len(entry.tags):
        category.group    = 'category'
        category.name     = entry.tags[0].term
        post.terms        = [ category ]
        for tag in entry.tags[1:]:
            term          = WordPressTerm()
            term.group    = 'tag'
            term.name     = tag.term
            # Add the term
            post.terms.append(term)
    """
    return post

def has_duplicate(title, client):
    # Get all the post from wordpress
    if not hasattr(has_duplicate, "posts"):
        has_duplicate.posts = []
        offset = 0
        limit  = 100
        while True:
            page = wp.call(GetPosts({'number': limit, 'offset': offset}))
            # no more posts returned
            if len(page) == 0: break
            # stacks pages
            has_duplicate.posts += page
            offset = offset + limit
    # Use posts cache version
    posts = has_duplicate.posts
    return len( [p for p in posts if p.title == post.title] ) > 0


if __name__ == "__main__":
    try:
        wp_user = os.environ["WP_USER"]
        wp_pwd  = os.environ["WP_PWD"]
        wp_url  = os.environ["WP_URL"]
    except KeyError as e:
        print "Please set the environement variable `%s`." % e
        exit()
    # Create wp client
    wp = Client(wp_url, wp_user, wp_pwd)
    # Read cmd arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help="Feed file path or URL (e.g: ./file.rss, http://exemple.org/rss)")
    parser.add_argument('--force', dest='force', help="Force the parser to create the posts (without checking duplicates).", action='store_true')
    parser.set_defaults(force=False)
    args = parser.parse_args()
    # Parse feed file
    document = feedparser.parse(args.target)
    # Convert every feed entry into a wp post
    for entry in document.entries:
        post = entry_to_wppost(entry)
        if args.force or not has_duplicate(post.title, client=wp):
            # Create the post on wordpress
            idx =  wp.call(NewPost(post))
            print "Post `%s` created." % post.title
        else:
            print "Post `%s` already exists." % post.title

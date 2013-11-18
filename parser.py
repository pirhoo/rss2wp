# -*- coding: utf-8 -*-
from colors import red, green
from wordpress_xmlrpc import Client, WordPressPost, WordPressUser, WordPressTerm
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUsers
import argparse
import feedparser
import os

__all__ = ["Client"]

def entry_to_wppost(entry, client):
    post             = WordPressPost()
    # Convert entry values to Post value
    post.user        = get_author_by_display_name(entry.author, client)
    post.date        = entry.published_parsed
    post.post_status = "draft"
    post.title       = entry.title
    post.content     = entry.content[0].value
    post.excerpt     = entry.summary
    post.link        = entry.link
    # There is some given tags
    if len(entry.tags):
        entry.tags = [t.term for t in entry.tags]
        # Add category (with the first tag)
        post.terms_names = {
            'category': entry.tags[0:1],
            'post_tag': [],
        }
        # Add tags
        if len(entry.tags) > 1: post.terms_names['post_tag'] = entry.tags[1:]
    return post

def get_author_by_display_name(display_name, client):
    # Get all the post from wordpress
    if not hasattr(get_author_by_display_name, "authors"):
        get_author_by_display_name.authors = []
        offset = 0
        limit  = 100
        while True:
            page = wp.call(GetUsers({'number': limit, 'offset': offset}))
            # no more posts returned
            if len(page) == 0: break
            # stacks pages
            get_author_by_display_name.authors += page
            offset = offset + limit
    # Use author cache version
    authors = get_author_by_display_name.authors
    author  = [a for a in authors if a.display_name == display_name]
    return author[0].id if len(author) else None




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
        post = entry_to_wppost(entry, client=wp)
        if args.force or not has_duplicate(post.title, client=wp):
            # Create the post on wordpress
            idx =  wp.call(NewPost(post))
            print green(u" ✔ Post `%s` created." % post.title)
        else:
            print red(u" ✖ Post `%s` already exists." % post.title)

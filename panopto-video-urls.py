#!/usr/bin/python3
# Created by Jacob Strieb
# February 2020

import argparse
import requests

from urllib.parse import urlparse

import xml.etree.ElementTree as ET

from lxml import html


###############################################################################
# Helper Functions
###############################################################################

def parse_args():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Extract video URLs from RSS "
        "podcast link")
    parser.add_argument("podcast_url", help="Link to the RSS feed containing "
        "video URLs")
    parser.add_argument("-o", "--output_file", required=False, help="Path for "
        "a file to output the list of links to. If not specified, print to "
        "standard output")
    parser.add_argument("-x", "--output_xargs", required=False,
        action="store_true", help="Use to output file names in addition to "
        "file URLs. Output will be in xargs format")
    return parser.parse_args()

def process_title(title):
    # Turn titles into valid filenames by removing disallowed characters,
    # replacing spaces with understcores, and replacing periods with dashes
    disallowed_chars = "/\\?%*:|\"><,'()+#"
    trans = str.maketrans("", "", disallowed_chars)
    return title.translate(trans).replace(" ", "_").replace(".", "-")

def parse_xml(url, parse_filenames=False):
    # Download the XML from the URL
    r = requests.get(url)
    data = r.content.decode(r.encoding if r.encoding else r.apparent_encoding)

    # Parse the retrieved XML file
    root = ET.fromstring(data)

    # Return the URLs from enclosure tags inside items. For reference, see:
    # https://docs.python.org/3.8/library/xml.etree.elementtree.html
    items = root.findall("*/item")
    urls = list(map(lambda i: i.find("enclosure").get("url"), items))
    titles = list(map(process_title, map(lambda i: i.findtext("title"), items)))

    # NOTE: We assume order is preserved so that titles and URLs correspond
    return urls, titles

def parse_html(url, parse_filenames=False):
    # Download and parse the HTML from the URL
    r = requests.get(url)
    tree = html.fromstring(r.content)

    # NOTE: there is probably only one of each of these
    urls = list(tree.xpath("//meta[@property='og:video']/@content"))
    titles = list(tree.xpath("//meta[@property='og:title']/@content"))

    return urls, titles



###############################################################################
# Main Function
###############################################################################

def main():
    # Parse command-line arguments
    args = parse_args()
    podcast_url = args.podcast_url
    output_file = args.output_file
    output_xargs = args.output_xargs

    # Parse the input URL to decide how to proceed
    url_path = urlparse(podcast_url).path

    # Pick a function for getting video URLs depending on main URL path
    get_url_functions = {
        "/Panopto/Podcast/Podcast.ashx": parse_xml,
        "/Panopto/Pages/Viewer.aspx": parse_html,
    }
    try:
        parse = get_url_functions[url_path]
    except KeyError:
        print("Invalid input URL")
        return

    # Get video URLs from parsed XML link
    video_urls, video_titles = parse(podcast_url)
    assert(len(video_urls) == len(video_titles))

    # Generate output string
    out_string = ""
    for url, title in zip(video_urls, video_titles):
        out_string += ("\"%s.mp4\"\n" % title) if output_xargs else ""
        out_string += url
        out_string += "\n"

    # Write to the output file if applicable, otherwise print
    if output_file is not None:
        with open(output_file, "w") as f:
            f.write(out_string)
    else:
        print(out_string)



if __name__ == "__main__":
    main()

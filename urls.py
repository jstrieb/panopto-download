#!/usr/bin/python3

import argparse
import requests

import xml.etree.ElementTree as ET


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
    disallowed_chars = "/\\?%*:|\"><,'()+"
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



###############################################################################
# Main Function
###############################################################################

def main():
    # Parse command-line arguments
    args = parse_args()
    podcast_url = args.podcast_url
    output_file = args.output_file
    output_xargs = args.output_xargs

    # Get video URLs from parsed XML link
    video_urls, video_titles = parse_xml(podcast_url)
    assert(len(video_urls) == len(video_titles))

    # Generate output string
    out_string = ""
    for url, title in zip(video_urls, video_titles):
        out_string += ("-O \"%s.mp4\"\n" % title) if output_xargs else ""
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

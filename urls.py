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
    return parser.parse_args()

def parse_xml(url):
    # Download the XML from the URL
    r = requests.get(url)
    data = r.content.decode(r.encoding if r.encoding else r.apparent_encoding)

    # Parse the retrieved XML file
    root = ET.fromstring(data)

    # Return the URLs from enclosure tags inside items. For reference, see:
    # https://docs.python.org/3.8/library/xml.etree.elementtree.html
    items = root.findall("*/item/enclosure")
    return list(map(lambda i: i.get("url"), items))



###############################################################################
# Main Function
###############################################################################

def main():
    # Parse command-line arguments
    args = parse_args()
    url, outfile = args.podcast_url, args.output_file

    # Get video URLs from parsed XML link
    video_urls = parse_xml(url)

    # Generate output string
    out_string = "\n".join(video_urls)
    print(out_string)


if __name__ == "__main__":
    main()

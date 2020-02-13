# Background & Overview

Students deserve access to course materials, even after completing a course. At
Carnegie Mellon, many lecture videos are recorded and made available online on
[Panopto](https://www.panopto.com/). There is no easy user-interface to
download course videos, but there is a feature where folders of recorded videos
generate RSS feeds.

This script parses Panopto RSS feeds and extracts video URLs for batch
downloading.


# Quick Start

1. To use the script, clone the repository or download `panopto-video-urls.py`,
   and go into the `panopto-download` directory.

    ```
    git clone https://github.com/jstrieb/panopto-download.git && cd panopto-download
    ```

2. Make sure Python 3 is running (check by running `python --version` or
   locating a `python3` binary). Also make sure the `requests` library is
   installed -- it may have been installed by another package. To install it
   (particularly if seeing a `ModuleNotFoundError`), run the following.

    ```
    pip3 install -r requirements.txt
    ```

    Depending on the system configuration, `pip3` in the command above may need to
    instead be replaced with `pip`. Additionally, if on a system with limited
    permissions, instead run the following command. This only installs the
    dependencies for the local user, rather than system-wide. In particular, if
    running the script on the Andrew servers, students can only install locally
    since their accounts lack `sudo` permissions.

    ```
    pip3 install --user -r requirements.txt
    ```
    
3. Test that the command works. When run, there should be output like the
   following.

    ```
    $ python3 panopto-video-urls.py
    usage: panopto-video-urls.py [-h] [-o OUTPUT_FILE] [-x] podcast_url
    panopto-video-urls.py: error: the following arguments are required: podcast_url
    ```
    
4. Get a Panopto RSS URL. For more information on how to do this, see the next
   section.

5. Now, use the script to generate a list of video URLs to download. This can
   be saved into a file using the `-o` option, or it can be piped directly into
   `xargs` if on a system where it installed. The latter is my preferred option.
   To download all videos from an RSS link, I do the following.
   
    ```
    python3 panopto-video-urls.py -x "http://<some link>" | xargs --max-lines=2 --max-procs=0 wget
    ```


# Getting Panopto RSS Feed URLs

==================
Download Subtitles
==================

Download the subtitle of a movie by right-clicking the file in Finder and clicking in 'Download Subtitle'. 

Requirements
============
- Mac OS X 10.6 or later
- python 2.7
- wget
- automator

Preferences
===========

The language of choice can be configured in the 'download_subtitle.ini' file in the user's home folder. 
Example:

    [options]
    language = pob

pob is for Brazillian Portuguese. The language codes follow the OpenSubtitles.org settings.

Install
=======

    sudo python setup.py install

Usage
=====

Right click a movie file in Finder and click in the Download Subtitle menu.

License
=======

See License.txt

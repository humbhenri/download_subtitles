#!/usr/bin/python
# Download Subtitles: Download subtitle of a movie using OpenSubtitles.org
# Copyright (C) 2013  Humberto Henrique Campos Pinheiro

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from ConfigParser import SafeConfigParser
import os
import struct
import subprocess
import sys
import tempfile
import tkMessageBox
import traceback
import xmlrpclib
import zipfile

USER_AGENT = 'OS Test User Agent'
SERVER_HOST = 'http://api.opensubtitles.org/xml-rpc'
LANGUAGE = 'pob'
CONFIG_FILE = os.path.join(os.getenv('HOME'), '.download_subtitle.ini')
DEFAULT_SECTION = 'options'

def compute_hash(filepath):
    """ size + 64bit checksum of first and last 64k """
    with open(filepath, 'rb') as file:
        file.seek(0, 2)
        fsize = file.tell()
        file.seek(0)
        limit = 65536
        uint = 8
        fhash = fsize
        for i in xrange(0, limit/uint):
            fhash += struct.unpack('q', file.read(uint))[0]
            fhash = fhash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number
        file.seek(max(0, fsize - limit))
        for i in xrange(0, limit/uint):
            fhash += struct.unpack('q', file.read(uint))[0]
            fhash = fhash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number
        return '%016x' % fhash     


def download(url, dest):
    wget = '/usr/local/bin/wget %s -O %s' % (url, dest)
    subprocess.call(wget.split())


def subtitle_info(moviehash, moviebytesize):
    server = xmlrpclib.ServerProxy(SERVER_HOST)
    resp = server.LogIn('', '', LANGUAGE, USER_AGENT)
    token = resp['token']
    return server.SearchSubtitles(token, [{'sublanguageid': LANGUAGE, 'moviehash': moviehash, 'moviebytesize': moviebytesize}])


def download_subtitle(filepath):
    moviehash = compute_hash(filepath)
    moviebytesize = os.path.getsize(filepath)
    info = subtitle_info(moviehash, moviebytesize)
    if info['data']:
        link = info['data'][0]['ZipDownloadLink']
        dest = tempfile.gettempdir()
        zipname = os.path.join(dest, 'subtitle.zip')
        download(link, zipname)
        zip = zipfile.ZipFile(zipname)
        subtitle = [file for file in zip.infolist() if file.filename.endswith('srt')][0]
        subtitle.filename = os.path.splitext(os.path.basename(filepath))[0] + '.srt'
        zip.extract(subtitle, os.path.dirname(filepath))
        os.remove(zipname)


def subtitle_exists(filepath):
    subtitle, _ = os.path.splitext(filepath)
    subtitle += '.srt'
    return os.path.exists(subtitle)


def read_config():
    parser = SafeConfigParser()
    parser.read(CONFIG_FILE)
    global LANGUAGE
    LANGUAGE = parser.get(DEFAULT_SECTION, 'LANGUAGE')


def create_config():
    parser = SafeConfigParser()
    parser.add_section(DEFAULT_SECTION)
    parser.set(DEFAULT_SECTION, 'LANGUAGE', 'pob')
    f = open(CONFIG_FILE, 'w')
    parser.write(f)
    f.close()


def main():
    if len(sys.argv) < 2:
        tkMessageBox.showinfo('', 'Usage: download_subtitle <path>')
    elif subtitle_exists(sys.argv[1]):
        tkMessageBox.showinfo('', 'Subtitle alread exists\n')
    else:
        try:
            if not os.path.exists(CONFIG_FILE):
                create_config()
            read_config()
            download_subtitle(sys.argv[1])
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tkMessageBox.showinfo('', traceback.format_exception(exc_type, exc_value,
                                          exc_traceback))


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Credits: https://gist.github.com/luizoti/20e41bb0ea30f2ce0170b657e1238499
#Usage: python3 ChromeAppDownloader.py
#

"""
    Python3 script to download the Chrome Extensions (CRX) file directly from the google chrome web store.
    Referred from http://chrome-extension-downloader.com/how-does-it-work.php
"""

import re
import sys
import platform

import requests
from urllib.parse import urlparse
from os.path import join, dirname, basename


ARCH = platform.architecture()

class ChromeExtensionDownloader():
    """Class to download Chrome Extension by URL."""

    def __init__(self):
        self.ext_download_url = "https://clients2.google.com/service/update2/crx?response=redirect&prodversion={chrome_version}&acceptformat=crx2,crx3&x=id%3D{extension_id}%26uc&nacl_arch={arch}"

    def download(self, chrome_store_url, user_agent_ver, dest_dir=None):
        """
            Download the given URL into given filename.
            :param chrome_store_url:
            :param _file_name_:
            :return:
        """
        arch = self.get_arch()
        extension_id, file_name = self.parse_extension_url(chrome_store_url=chrome_store_url)
        chrome_version = self.get_chrome_version(user_agent_ver)

        extension_url = self.ext_download_url.format(chrome_version=chrome_version, extension_id=extension_id, arch=arch)
        return extension_url, self.download_file(extension_url, dest_dir, file_name)


    def parse_extension_url(self, chrome_store_url):
        """
            Validate the given input is chrome store URL or not.
            Returning app ID and app Name from the URL
            :param chrome_store_url:
            :return:
        """
        try:
            # Try to validate the URL
            uparse = urlparse(chrome_store_url)

            if uparse.netloc != "chrome.google.com":
                raise ValueError("Not a valid URL %s" % chrome_store_url)

            splits = uparse.path.split("/")

            if not uparse.path.startswith("/webstore/detail/"):
                raise ValueError("Not a valid URL %s" % chrome_store_url)
        except Exception as e:
            raise e
        return splits[-1], splits[-2]

    def sizeof_fmt(self, num, suffix="B"):
        """Format size for humans."""
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, "Yi", suffix)

    def download_file(self, extension_url, dest_dir=None, file_name=None):
        """Download file with url."""

        if not file_name:
            # Maybe is possible to ge extension from requests, maybe is to work
            file_name = basename(extension_url)

        if not dest_dir:
            dest_dir = dirname(__file__)

        dest_file = join(dest_dir, file_name + ".crx")

        with open(dest_file, "wb") as binary_file:
            print()
            response = requests.get(extension_url, stream=True)
            total = response.headers.get("content-length")

            if total is None:
                binary_file.write(response.content)
                return False
            else:
                downloaded = 0
                total = int(total)
                try:
                    for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                        downloaded += len(data)
                        binary_file.write(data)
                        done = int(50 * downloaded / total)
                        str_to_format = f"\rBaixando: {dest_file} {'█' * done}{'.' * (50 - done)} | {self.sizeof_fmt(downloaded)}/{self.sizeof_fmt(total)}"
                        print(str_to_format, end="\r")
                        if downloaded == total:
                            return dest_file
                except KeyboardInterrupt:
                    print("\nDonwload interrompido")
                    return False
                print()


    def get_arch(self):
        """Return a compatible architecture to use in download url."""
        if "64bit" in ARCH:
            return 'x86-64'
        elif "32bit" in ARCH:
            return 'x86-32'
        else:
            print("Not inplemented")
            sys.exit(0)


    def get_chrome_version(self, chrome_version):
        """Extract get_chrome version from User Agent."""
        from_user_agent = re.findall(r"Chrom(?:e|ium)\/(\d+)\.(\d+)\.(\d+)\.(\d+)", chrome_version)

        if from_user_agent:
            return ".".join(from_user_agent[0])
        elif re.match(r"\d+\.\d+\.\d+", chrome_version):
            return chrome_version



if __name__ == '__main__':
    #url = "https://chrome.google.com/webstore/detail/certisign-websigner/acfifjfajpekbmhmjppnmmjgmhjkildl"
    urls = ["https://chrome.google.com/webstore/detail/foxyproxy-standard/gcknhkkoolaabfmlnjonogaaifnjlfnp", "https://chrome.google.com/webstore/detail/wappalyzer-technology-pro/gppongmhjkpfnbhagpmjfkannfbllamg", "https://chrome.google.com/webstore/detail/retirejs/moibopkbhjceeedibkbkbchbjnkadmom"]
    user_agent_ver = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    for url in urls:
        downloader = ChromeExtensionDownloader().download(url, user_agent_ver)
        print(downloader)

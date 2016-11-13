# GMF [File Downloader] for NAVER Blog

import re
import sys
import json
from http import client
from urllib import request


def print_logo():
    print("#------------------------------------------#")
    print("# [GMF] Give Me a File!! [File Downloader] #")
    print("#------------------------------------------#")
    print("# for NAVER Blog\n")


def get_url_source(url):
    try:
        while url.find("PostView.nhn") == -1 and url.find("PostList.nhn") == -1:
            f = request.urlopen(url)
            url_info = f.info()
            url_charset = client.HTTPMessage.get_charsets(url_info)[0]
            url_source = f.read().decode(url_charset)

            # find 'NBlogWlwLayout.nhn'
            if url_source.find("NBlogWlwLayout.nhn") == -1:
                print("\n[-] It is not a NAVER Blog")
                sys.exit(0)

            # get frame src
            p_frame = re.compile(r"\s*.*?<frameset.*?>(.*)</frameset>", re.IGNORECASE | re.DOTALL)
            p_src_url = re.compile(r"\s*.*?src=[\'\"](.+?)[\'\"]", re.IGNORECASE | re.DOTALL)
            src_url = p_src_url.match(p_frame.match(url_source).group(1)).group(1)
            url = src_url

        if url.find("http://blog.naver.com") == -1:
            last_url = "http://blog.naver.com" + url
        else:
            last_url = url

        print("   => Last URL : %s\n" % last_url)
        f = request.urlopen(last_url)
        url_info = f.info()
        url_charset = client.HTTPMessage.get_charsets(url_info)[0]
        url_source = f.read().decode(url_charset)

        return url_source

    except Exception as e:
        print("[-] Error : %s" % e)
        sys.exit(-1)


def main():
    print_logo()

    if len(sys.argv) != 2:
        print("[*] Usage : gmf_nb.py [NAVER Blog URL]")
    else:
        url = sys.argv[1]
        print("[*] Target URL : %s" % url)
        url_source = get_url_source(url)

        # find 't.static.blog.naver.net'
        if url_source.find("t.static.blog.naver.net") == -1:
            print("\n[-] It is not a NAVER Blog")
            sys.exit(0)

        try:
            # find 'aPostFiles'
            p_attached_file = re.compile(r"\s*.*aPostFiles\[1\] = \[(.*?)\]", re.IGNORECASE | re.DOTALL)
            result = p_attached_file.match(url_source).group(1)
            if result:
                # convert to JSON style
                data = "[" + result.replace('\'', '\"') + "]"
                json_data = json.loads(data)

                for each_file in json_data:
                    print("* File : %s, Size : %s Bytes" % (each_file["encodedAttachFileName"], each_file["attachFileSize"]))
                    print("  Link : %s" % each_file["encodedAttachFileUrl"])
                    # File Download
                    request.urlretrieve(each_file["encodedAttachFileUrl"], each_file["encodedAttachFileName"])
                    print("  => Done!!\n")
            else:
                print("[-] Attached File not found !!")

        except Exception as e:
            print("[-] Error : %s" % e)
            sys.exit(-1)

if __name__ == "__main__":
    sys.exit(main())

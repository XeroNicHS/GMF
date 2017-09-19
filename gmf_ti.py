# GMF [File Downloader] for Tistory Blog

import re
import sys
from http import client
from urllib import request


def print_logo():
    print("#------------------------------------------#")
    print("# [GMF] Give Me a File!! [File Downloader] #")
    print("#------------------------------------------#")
    print("# for Tistory Blog\n")


def get_url_source(url):
    try:
        f = request.urlopen(url)
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
        print("[*] Usage : gmf_ti.py [Tistory Blog URL]")
    else:
        url = sys.argv[1]
        print("[*] Target URL : %s\n" % url)
        url_source = get_url_source(url)

        # find 's1.daumcdn.net/cfs.tistory'
        if url_source.find("t1.daumcdn.net/tistory") == -1:
            print("[-] It is not a Tistory Blog")
            sys.exit(0)

        try:
            # find all 'attach file link'
            p_attach = re.compile(r"href=[\'\"](\S+?/attachment/.*?)[\'\"]\s*.*?/> (.*?)</", re.IGNORECASE | re.DOTALL)
            result = p_attach.findall(url_source)

            if result:
                for each_file in result:
                    file_url = each_file[0]
                    if each_file[1] == "":
                        file_name = file_url[file_url.rfind('/') + 1:]
                    else:
                        file_name = each_file[1]
                    print("* File : %s" % file_name)
                    print("  Link : %s" % file_url)
                    request.urlretrieve(file_url, file_name)
                    print("  ==> Done")
            else:
                print("[-] Attached File not found !!")

        except Exception as e:
            print("[-] Error : %s" % e)
            sys.exit(-1)

if __name__ == "__main__":
    sys.exit(main())

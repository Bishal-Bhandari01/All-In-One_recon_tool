#!/usr/bin/python3

from argparse import ArgumentParser, FileType
import requests
import socket
from time import time
from threading import Thread

print("\t", "*"*97)
print("\t*           __        _       _       __________ __      _ __________ __      _ ___________       *")
print("\t*         /    \     | |     | |     |___    ___|  \    | |   ____   |  \    | |   ________|      *")
print("\t*        /  /\  \    | |     | |         |  |   |   \   | |  |    |  |   \   | |  |________       *")
print("\t*       /  /__\  \   | |     | |         |  |   |  |\ \ | |  |    |  |  |\ \ | |   ________|      *")
print("\t*      /  /    \  \  | |_____| |_____ ___|  |___|  | \ \| |  |____|  |  | \ \| |  |________       *")
print("\t*     /__/      \__\ |_______|_______|__________|__|  \___|__________|__|  \___|___________|      *")
print("\t*                                                                                                 *")
print("\t", "*"*97)


def help():
    """ prepare argument parse

    return:
        args(argparse.Namespace)
    """
    parse = ArgumentParser(description="Developed by github: @Bishal-Bhandari01\n\tPython based fast all in one tool",
                           usage="%(prog)s -s domin.com -t 50\n\t%(prog)s -subs domain.com -t 50")
    parse.add_argument("-subs", "--sub-domain", metavar="",
                       dest="subs", help="Find sub-domain")
    parse.add_argument("--v", help="Version of the tool", version="0.0.1")
    parse.add_argument("-t", "--thread", metavar="", dest="threads",
                       help="Set threads", default=500)
    parse.add_argument("-p", "--port", metavar="",
                       dest="ports", help="Scan ports from 1-65535")
    parse.add_argument("-w", "--wordlist", dest="wordlist",
                       metavar="", help="wordlist for sub-domains use seclists", type=FileType("r"))
    parse.add_argument("-net", "-network", dest="network",
                       metavar="", help="url for port scanning")
    parse.add_argument("-iL", "--List", dest="domain_list",
                       help="lists of domain or a string", metavar="", type=FileType("r"))
    parse.add_argument("-o", metavar="", dest="output",
                       help="Get output of the result")
    args = parse.parse_args()
    return args


def output(outputs):
    if arguments.ports:
        file = open(arguments.output, "a")
        file.write("==> Port " + str(outputs) + " is open.", end="\n")
        file.close()

    if arguments.subs:
        file = open(arguments.output, "a")
        file.write(outputs+"\n")
        file.close()

# Port Scanning Tool Code starts here...


def scan_ports(end: int):
    """ scanning ports
        end(int): number of ports to be scanned
    """
    for port in range(1, end):
        yield port


def prepare_threads(thread: int):
    """prepare threads:

        thread(int) - number of threads
    """
    thread_list = []
    for _ in range(thread+1):
        thread_list.append(Thread(target=scan_ports))

    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()


def scan(domain):
    while True:
        try:
            port = next(ports)
            result = s.connect_ex((domain, port))

            if result == 0:
                print(f"[+] Port "+str(port)+" is open.")

            if arguments.output:
                output(port)

        except (ConnectionRefusedError, socket.timeout):
            continue
        except StopIteration:
            break
# Port Scanning Tool Code end here...


# Sub-domain Scanning Code Start Here...
def prepare_words():
    """Generator function for words
    """
    words = arguments.wordlist.read().split()
    for word in words:
        yield word


def scan_subs(subdomains):
    for subdomain in subdomains:
        url = f"https://{subdomain}.{arguments.subs}"
        try:
            requests.get(url)
            urls = url
            print(f"[+] {url}")
            if arguments.output:
                outputs = urls.replace('https://', '')
                output(outputs)

        except requests.ConnectionError:
            pass
# Sub-domain Scanning Code End Here...


if __name__ == "__main__":
    arguments = help()
    words = prepare_words()
    if arguments.ports:
        ports = scan_ports(int(arguments.ports))
    else:
        ports = scan_ports(65535)
    if arguments.subs:
        start = time()
        scan_subs(words)
        end = time()

    if arguments.network:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target = socket.gethostbyname(arguments.network)
        socket.setdefaulttimeout(1)

        start = time()
        print(f"[X] Port Scanning for {arguments.network}")
        scan(target)
        end = time()

    if arguments.domain_list:
        words = arguments.domain_list.read().split()
        start = time()
        for w in words:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target = socket.gethostbyname(w)
            socket.setdefaulttimeout(1)
            print(f"[X] Port Scanning for {w}")
            scan(target)

        end = time()

    print("Time taken to scan: ", round(end-start, 2))

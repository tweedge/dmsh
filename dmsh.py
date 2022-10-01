import argparse
import tldextract
from time import sleep
from whois import whois
from serpapi import GoogleSearch
from pprint import pprint

parser = argparse.ArgumentParser(
    description=(
        "Checks if any domains in a list are expired, and optionally evaluates how popular each domain was"
    )
)
parser.add_argument(
    "--file",
    help="File to read, where 1 line = 1 domain to check",
    type=str,
    required=True,
)
parser.add_argument(
    "--sleep",
    help="Optional: How long to sleep between whois queries (in milliseconds)",
    type=int,
    default=1000,
)
parser.add_argument(
    "--key",
    help="Optional: SerpApi key if you want to quickly check how popular a domain might be",
    type=str,
    default="",
)
parser.add_argument(
    "--debug",
    help="Optional: Pretty print WHOIS data and exceptions returned",
    type=bool,
    default=False,
)


args = parser.parse_args()


extract = tldextract.TLDExtract()

file_handle = open(args.file, "r")
file_lines = file_handle.readlines()

domains = set()
lines_count = 0
domains_count = 0
for line in file_lines:
    lines_count += 1
    line = line.strip()
    if line:
        domain = extract(line).registered_domain
        if domain:
            domains_count += 1
            domains.add(domain)

print(f"Looking up {domains_count} domains (from {lines_count} lines)")

for domain in domains:
    sleep(args.sleep / 1000)
    exists = True
    who = None

    registrable_exceptions = [
        "No match",
        "No entries found",
        "No data found",
        "NOT FOUND",
        "We do not have an entry in our database",
        "Status: free",
    ]

    try:
        who = whois(domain)
    except Exception as e:
        if args.debug:
            print(f"Exception returned when looking up {domain}:")
            pprint(e)

        exception_str = str(e)
        for exceptions_check in registrable_exceptions:
            if exceptions_check.lower() in exception_str.lower():
                if args.debug:
                    print(f"Match found: '{exceptions_check}' - domain DNE")
                exists = False

        if exists:
            if args.debug:
                print(f"No match found, unclear if domain DNE")
            continue

    if who:
        if args.debug:
            print(f"WHOIS data returned when looking up {domain}:")
            pprint(who)

        if "registrar" in who.keys():
            if who["registrar"]:
                continue

        if "status" in who.keys():
            if who["status"]:
                continue

    total_results = 0
    try:
        if args.key:
            params = {
                "engine": "google",
                "q": f'"{domain}"',
                "api_key": args.key,
            }

            search = GoogleSearch(params)
            results = search.get_dict()

            total_results = results["search_information"]["total_results"]
    except Exception as e:
        print(e)

    if total_results:
        print(f"{domain} is registrable ({total_results} results on Google)")
    else:
        print(f"{domain} is registrable")

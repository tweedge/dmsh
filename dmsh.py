import argparse
import tldextract
from time import sleep
from PyFunceble import DomainAvailabilityChecker


parser = argparse.ArgumentParser(
    description=("Checks if any domains in a list are expired")
)
parser.add_argument(
    "--file",
    help="File containing domains",
    type=str,
    required=True,
)
parser.add_argument(
    "--sleep",
    help="Optional: Sleep [x] seconds between WHOIS queries (default: 1)",
    type=float,
    default=1.0,
)
parser.add_argument(
    "--only",
    help="Optional: Only check the first [x] domains (default: check all)",
    type=int,
    default=0,
)


args = parser.parse_args()

extract = tldextract.TLDExtract()
checker = DomainAvailabilityChecker()
unique_domains = set()
domain_data = []

with open(args.file) as file:
    while line := file.readline():
        if len(unique_domains) >= args.only and args.only > 0:
            break

        line = line.strip()
        if not line:
            continue

        split_line = line.split(" ")
        if len(split_line) == 1:
            domain = extract(line).registered_domain
            if domain in unique_domains:
                continue

            unique_domains.add(domain)
            domain_data.append([domain, 0])
        elif len(split_line) == 2:
            domain = extract(split_line[1]).registered_domain
            if domain in unique_domains:
                continue

            unique_domains.add(domain)
            domain_data.append([domain, int(split_line[0])])
        else:
            print(f"error: line format not recognized: {line}")

for domain_datum in domain_data:
    domain = domain_datum[0]
    rank = domain_datum[1]

    sleep(args.sleep)

    domain_details = checker.set_subject(domain).get_status()
    domain_status = domain_details.status

    if domain_status != "INACTIVE":
        continue

    if rank > 0:
        print(f"{rank} {domain} is registrable")
    else:
        print(f"{domain} is registrable")

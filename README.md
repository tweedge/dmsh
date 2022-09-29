# Dead Mailserver Hunter

[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Written By](https://img.shields.io/badge/written%20by-some%20nerd-red.svg)](https://chris.partridge.tech)

DMSH is a quick Python script to iterate through a list of domains (one line = one domain), check if the domain can be registered, and optionally assess how popular the domain was based on a Google search. There are many possible applications for this, but DMSH was created specifically to hunt for expired domains that had hosted mailservers, so that any lingering email sent to it can be caught.

Looking for registrable domains among the following could be especially fruitful:
* Matt Ketmo's EmailChecker package and its list of [throwaway domains](https://github.com/MattKetmo/EmailChecker/blob/master/res/throwaway_domains.txt)
* Ozan Bayram's massive list of [free email provider domains](https://gist.github.com/okutbay/5b4974b70673dfdcc21c517632c1f984)

### Recommendations

This tool was inspired by [this Reddit post](https://www.reddit.com/r/cybersecurity/comments/xm8qtm/legality_of_making_an_email_feed_from_by_using/) on the legal/ethical considerations of registering old domains and publishing any incoming email, so it's fitting that it should come with a usage warning.

Please use any expired domain you purchase responsibly and ethically. **Everyone deserves privacy.** Any email you collect from a registered domain should be reviewed for a specific purpose (ex. malware to research, spam to publish, statistics to track, etc.) and any identified PII should be deleted on discovery.

### Usage

```
% python3 dmsh.py --help
usage: dmsh.py [-h] --file FILE [--sleep SLEEP] [--key KEY] [--debug DEBUG]

Checks if any domains in a list are expired, and optionally evaluates how popular each domain was

options:
  -h, --help     show this help message and exit
  --file FILE    File to read, where 1 line = 1 domain to check
  --sleep SLEEP  Optional: How long to sleep between whois queries (in milliseconds)
  --key KEY      Optional: SerpApi key if you want to quickly check how popular a domain might be
  --debug DEBUG  Optional: Pretty print WHOIS data and exceptions returned
```

Using [SerpApi](https://serpapi.com/) to check how popular domains might be is *completely optional*. It is a search engine scraper with a reasonable free plan for this task (100 searches/month), and without providing a key, DMSH will work normally to identify expired domains, but not their popularity.

### Caveats

Google may not be the "right" tool for determining mailserver popularity, as Google's "search for a specific string in quotes" trick no longer works to match that string exactly in 100% of cases. While most domains will be accurate (typically, domains without a dash in them):

```
kimsdisk.com is registrable (381 results on Google)
commail2molly.com is registrable (308 results on Google)
verticalheaven.com is registrable (71 results on Google)
```

Some domains will show far more results on Google because Google is no longer attempting to match the string exactly, such as:

```
women-only.net is registrable (82100 results on Google)
from-italy.net is registrable (24300 results on Google)
fire-brigade.com is registrable (8320 results on Google)
```

However considering that backlink tools wouldn't be relevant (mail servers may not have many backlinks), and domain popularity tools would be out-of-date for any expired domains, this is "good enough." Just take any results with a grain of salt.

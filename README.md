# Dead Mailserver Hunter

[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Written By](https://img.shields.io/badge/written%20by-some%20nerd-red.svg)](https://chris.partridge.tech)
[![Author Also Writes On](https://img.shields.io/mastodon/follow/108210086817505115?domain=https%3A%2F%2Fcybersecurity.theater)](https://cybersecurity.theater/@tweedge)

DMSH is a quick Python script to iterate through a list of domains and check if the domain can be registered. There are many possible applications for this, but DMSH was created specifically to hunt for expired domains that had hosted mailservers, so that any lingering email sent to it can be caught.

After some trial and error, I've found that the best way is to find expired domains that appeared often in major breaches. I computed and released a list of the [most popular email domains](https://chris.partridge.tech/data/most-popular-email-domains-collections-1-5-etc/) found in Collection 1-5, ANTIPUBLIC, MYR, and Zabugor breach compilations - please feel free to leverage it in your research.

Though my original - and still valid! - tactic was to look at email domain lists, such as those used by some webmasters to fight SEO spam or potentially unwanted accounts:
* Matt Ketmo's EmailChecker package and its list of [throwaway domains](https://github.com/MattKetmo/EmailChecker/blob/master/res/throwaway_domains.txt)
* Ozan Bayram's massive list of [free email provider domains](https://gist.github.com/okutbay/5b4974b70673dfdcc21c517632c1f984)

### Recommendations

This tool was inspired by [this Reddit post](https://www.reddit.com/r/cybersecurity/comments/xm8qtm/legality_of_making_an_email_feed_from_by_using/) on the legal/ethical considerations of registering old domains and publishing any incoming email, so it's fitting that it should come with a note about that.

Please use any expired domain you purchase responsibly and ethically. **Everyone deserves privacy.** Any email you collect from a registered domain should be reviewed for a specific purpose (ex. malware to research, spam to publish, statistics to track, etc.) and any identified PII should be deleted on discovery.

### Usage

```
% python3 dmsh.py --help
usage: dmsh.py [-h] --file FILE [--sleep FLOAT] [--only INTEGER]

Checks if any domains in a list are expired

options:
  -h, --help      Show this help message and exit
  --file FILE     File containing domains
  --sleep FLOAT   Optional: Sleep [x] seconds between WHOIS queries (default: 1)
  --only INTEGER  Optional: Only check the first [x] domains (default: check all)
```

Files can be formatted **either** as just a list of domains:

```
domain
another_domain
wow_bill_your_mom_let_you_have_three_domains
```

**or** you can have an integer preceeding the domain, ex. how many times that domain appeared in a breach, or how popular it is relative to other domains:

```
100 domain
90 another_domain
1 exceedingly_unpopular_domain
```

So for example, after downloading and extracting `email_domains_by_popularity.txt` ([ref](https://chris.partridge.tech/data/most-popular-email-domains-collections-1-5-etc/)) you might check the top 2,000 entries for expired domains, waiting 0.1s between each lookup, using:

```
% python3 dmsh.py --file email_domains_by_popularity.txt --only 2000 --sleep 0.1
```

Any large scans (>1k domains) will take a while - be patient.
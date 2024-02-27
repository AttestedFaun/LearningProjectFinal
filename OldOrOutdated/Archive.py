#!/usr/bin/env python
#https://github.com/palewire/archiveis/blob/master/archiveis/api.py
import logging
import urllib.parse

import click
import requests

logger = logging.getLogger(__name__)
#https://12ft.io/

def capture(
    target_url,
    user_agent="archiveis (https://github.com/pastpages/archiveis)",
    #user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    proxies={},
):
    """
    Archives the provided URL using archive.is

    Returns the URL where the capture is stored.
    """
    # The site changes its TLD all the time. Cache what we get currently.
    domain = requests.get("https://archive.is").url

    # Put together the URL that will save our request
    save_url = domain + "submit/"

    # Configure the request headers
    headers = {
        "User-Agent": user_agent,
        "host": urllib.parse.urlparse(domain).netloc,
    }

    # Request a unique identifier for our activity
    logger.debug(f"Requesting {domain}")
    get_kwargs = dict(
        timeout=120,
        allow_redirects=True,
        headers=headers,
    )
    if proxies:
        get_kwargs["proxies"] = proxies
    response = requests.get(domain, **get_kwargs)
    response.raise_for_status()

    # It will need to be parsed from the homepage response headers
    html = str(response.content)
    try:
        unique_id = (
            html.split('name="submitid', 1)[1].split('value="', 1)[1].split('"', 1)[0]
        )
        logger.debug(f"Unique identifier: {unique_id}")
    except IndexError:
        logger.warning(
            "Unable to extract unique identifier from archive.is. Submitting without it."
        )
        unique_id = None

    # Send the capture request to archive.is with the unique id included
    data = {
        "url": target_url,
        "anyway": 1,
    }
    if unique_id:
        data.update({"submitid": unique_id})

    post_kwargs = dict(timeout=120, allow_redirects=True, headers=headers, data=data)
    if proxies:
        post_kwargs["proxies"] = proxies

    logger.debug(f"Requesting {save_url}")
    response = requests.post(save_url, **post_kwargs)
    response.raise_for_status()

    # There are a couple ways the header can come back
    if "Refresh" in response.headers:
        memento = str(response.headers["Refresh"]).split(";url=")[1]
        logger.debug(f"Memento from Refresh header: {memento}")
        return memento
    if "Location" in response.headers:
        memento = response.headers["Location"]
        logger.debug(f"Memento from Location header: {memento}")
        return memento
    logger.debug("Memento not found in response headers. Inspecting history.")
    for i, r in enumerate(response.history):
        logger.debug(f"Inspecting history request #{i}")
        logger.debug(r.headers)
        if "Location" in r.headers:
            memento = r.headers["Location"]
            logger.debug(
                "Memento from the Location header of {} history response: {}".format(
                    i + 1, memento
                )
            )
            return memento
    # If there's nothing at this point, throw an error
    logger.error("No memento returned by archive.is")
    logger.error(f"Status code: {response.status_code}")
    logger.error(response.headers)
    logger.error(response.text)
    raise Exception("No memento returned by archive.is")


@click.command()
@click.argument("url")
@click.option("-ua", "--user-agent", help="User-Agent header for the web request")
def cli(url, user_agent):
    url = "https://www.foxbusiness.com/markets/elon-musks-56-billion-pay-package-voided-by-judge?dicbo=v2-82oXEEr"
    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
    """
    Archives the provided URL using archive.is.
    """
    kwargs = {}
    if user_agent:
        kwargs["user_agent"] = user_agent
    archive_url = capture(url, **kwargs)
    click.echo(archive_url)

#Archive.capture('https://www.foxbusiness.com/markets/elon-musks-56-billion-pay-package-voided-by-judge?dicbo=v2-82oXEEr')

if __name__ == "__main__":
    url = "https://www.foxbusiness.com/markets/elon-musks-56-billion-pay-package-voided-by-judge?dicbo=v2-82oXEEr"
    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
    kwargs = {}
    kwargs["user_agent"] = user_agent
    archive_url = capture(url, **kwargs)
    click.echo(archive_url)
    #cli(Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0, https://www.foxbusiness.com/markets/elon-musks-56-billion-pay-package-voided-by-judge?dicbo=v2-82oXEEr)
    #cli()
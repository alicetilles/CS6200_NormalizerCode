import re

## Many URLs can refer to the same web resource. In order to ensure that you crawl 40,000 distinct web sites, you
# should apply the following canonicalization rules to all URLs you encounter.


def get_domain(url):
    # Used to normalize everything to http or https
    if "http://www." in url:
        schema = "http://"

    elif "https://www." in url:
        schema = "https://"

    else:
        schema = "https://"

    url = canonicalize_single_url(url)
    url_split = url.split("/")
    domain = url_split[2]
    return schema + domain


def canonicalize_domain(domain):
    domain = domain.lower()

    # Get HTTP or HTTPS and :// and remove it
    pattern = r"([htpHTP]+[sS]*[\:\/\/]+)"
    domain = re.sub(pattern, "", domain)

    # Get www. and remove it (make sure just at beginning of string)
    pattern = r"^([wW]{3}\.)"
    domain = re.sub(pattern, "", domain)

    return domain



def canonicalize_single_url(url, domain=""):
    print("\n")

    # If the URL is relative, make it absolute
    if url.startswith(".."):
        url = url.strip("..")

        ## Normalize domain name
        domain = canonicalize_domain(domain)

        # Add final slash just in case (gets removed later if it's a double)
        domain = domain + "/"
        url = domain + url

    # Another way for the URL to be relative (starting with /, not ..):
    if url.startswith("/"):

        ## Normalize domain name
        domain = canonicalize_domain(domain)
        url = domain + url

    # Another way for the URL to be relative (starting with #):
    if url.startswith("#"):

        ## Normalize domain name
        domain = canonicalize_domain(domain)
        url = domain + url

    # Get HTTP or HTTPS and :// and lowercase it
    pattern = r"([htpHTP]+[sS]*[\:\/\/]+)"
    http = re.search(pattern, url)
    url = re.sub(pattern, "", url)

    if http:
        http = http.group(1).lower()
    else:
        http = "https://"

    # Get www. and remove it (make sure just at beginning of string)
    pattern = r"^([wW]{3}\.)"
    url = re.sub(pattern, "", url)

    # Remove any ports
    url = url.replace(":80", "")
    url = url.replace(":443", "")

    # Remove hash suffixes
    url = url.split("#")[0]

    # Remove & suffixes
    url = url.split("&")[0]

    # Remove duplicate slashes
    url = url.replace("//", "/")

    # Remove final slashes before suffix
    url = url.replace("/.", ".")

    # Make domain lowercase but keep case of anything after /
    split = url.split('/', 1)
    before_slash = split[0]
    if len(split) > 1:
        after_slash = split[1]
    else:
        after_slash = ""

    url = before_slash.lower() + "/" + after_slash
    url = url.strip("/")
    url = http + url

    return url



def run_tests():
    print(canonicalize_single_url("https://www.abc.com"))
    print(canonicalize_single_url("http://www.abc.com"))
    print(canonicalize_single_url("http://www.abc.html"))
    print(canonicalize_single_url("/wiki/SomeText", "wikipedia.com"))
    print(canonicalize_single_url("../wiki/SomeText", "Wikipedia.com"))
    print(canonicalize_single_url("../wiki/SomeText", "www.Wikipedia.com"))
    print(canonicalize_single_url("www.wikipedia.org/wiki/SomeText"))
    print(canonicalize_single_url("HTTP://www.Example.com/SomeFile.html"))
    print(canonicalize_single_url("http://www.example.com:80"))
    print(canonicalize_single_url("../c.html", "example.com"))
    print(canonicalize_single_url("http://www.example.com/a.html#anything"))
    print(canonicalize_single_url("http://www.example.com//a.html"))
    print(canonicalize_single_url("https://www.google.com/search?q=hash+table&oq=hash+table&aqs=chrome..69i57j0i67j0l3j0i10j0i67j0l3.3698j0j9&sourceid=chrome&ie=UTF-8"))
    # print(get_domain("http://www.example.com/a.html"))
    # print(get_domain("https://www.abc.com"))
    # print(get_domain("abc.com"))
    # print(get_domain("www.abc.com"))
    # print(get_domain("www.abc.com/"))
    # print(get_domain("www.abc.com/hi"))
    # print(get_domain("https://www.google.com/search?q=hash+table&oq=hash+table&aqs=chrome..69i57j0i67j0l3j0i10j0i67j0l3.3698j0j9&sourceid=chrome&ie=UTF-8"))


# run_tests()




## Many URLs can refer to the same web resource. In order to ensure that you crawl 40,000 distinct web sites, you
# should apply the following canonicalization rules to all URLs you encounter.


def get_domain(url):
    url = canonicalize_single_url(url)
    url_split = url.split("/")
    domain = url_split[2]
    return domain


def canonicalize_single_url(url, domain=""):

    # If the URL is relative, make it absolute
    if url.startswith(".."):
        url = url.strip("..")

        ## Normalize domain name
        domain = get_domain(domain)

        # Add final slash just in case (gets removed later if it's a double)
        domain = domain + "/"
        url = domain + url

    # Another way for the URL to be negative (starting with /, not ..):
    if url.startswith("/"):

        ## Normalize domain name
        domain = get_domain(domain)
        url = domain + url


    # Make lowercase
    url = url.lower()

    # Used to normalize everything to http or https
    if "http://www." in url:
        schema = "http://"

    elif "https://www." in url:
        schema = "https://"

    else:
        schema = "https://"

    # Remove initial http or www
    url = url.replace("http://www.", "")
    url = url.replace("https://www.", "")
    url = url.replace("http://", "")
    url = url.replace("https://", "")
    url = url.replace("www.", "")

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

    return schema + url



def run_tests():
    print(canonicalize_single_url("https://www.abc.com"))
    print(canonicalize_single_url("http://www.abc.com"))
    print(canonicalize_single_url("http://www.abc.html"))
    print(canonicalize_single_url("/wiki/SomeText", "wikipedia.com"))
    print(canonicalize_single_url("../wiki/SomeText", "Wikipedia.com"))
    print(canonicalize_single_url("www.wikipedia.org/wiki/SomeText"))
    print(canonicalize_single_url("HTTP://www.Example.com/SomeFile.html"))
    print(canonicalize_single_url("http://www.example.com:80"))
    print(canonicalize_single_url("../c.html", "example.com"))
    print(canonicalize_single_url("http://www.example.com/a.html#anything"))
    print(canonicalize_single_url("http://www.example.com//a.html"))
    print(canonicalize_single_url("https://www.google.com/search?q=hash+table&oq=hash+table&aqs=chrome..69i57j0i67j0l3j0i10j0i67j0l3.3698j0j9&sourceid=chrome&ie=UTF-8"))
    print(get_domain("http://www.example.com/a.html"))
    print(get_domain("https://www.abc.com"))
    print(get_domain("abc.com"))
    print(get_domain("www.abc.com"))
    print(get_domain("www.abc.com/"))
    print(get_domain("www.abc.com/hi"))
    print(get_domain("https://www.google.com/search?q=hash+table&oq=hash+table&aqs=chrome..69i57j0i67j0l3j0i10j0i67j0l3.3698j0j9&sourceid=chrome&ie=UTF-8"))


# run_tests()



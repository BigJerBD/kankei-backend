def run_transaction(driver, function, string, **kwargs):
    with driver.session() as session:
        return session.read_transaction(function, string=string, **kwargs)


def cleanup_string(string):
    try:
        return string.strip()
    except AttributeError:
        return ValueError("search string is invalid")


def strip_tag(string: str):
    splited_string = string.split("#")
    if len(splited_string) == 2:
        return splited_string[0].strip(), splited_string[1].strip().lower()
    else:
        return string.strip(), ""

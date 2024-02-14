def tag(name: str, value: str | None = None, **attributes) -> str:
    """
    Generic function that returns an XML tag with the given name, optional value and zero or more attributes
    Args:
        name(str): name of the XML tag.
        value(str): Optional value of an XML tag, defaulted to None
        attributes(dict): Key value pairs of attributes to add to the XML tag
    Return:
        str: XML tag as a string.
    """
    attrs = "" if not attributes else " " + " ".join(
        f'{key.replace("_", "-")}="{value}"'
        for key, value in attributes.items()
    )

    if value is None:
        return f"<{name}{attrs} />"
    return f"<{name}{attrs}>{value}</{name}>"

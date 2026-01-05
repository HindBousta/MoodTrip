def parse_tags(tags) -> list:
    """
    Convert a comma-separated string of tags into a list of stripped strings.
    If input is already a list, return it as-is.
    """
    if isinstance(tags, str):
        return [tag.strip() for tag in tags.split(",") if tag.strip()]
    elif isinstance(tags, list):
        return tags
    return []

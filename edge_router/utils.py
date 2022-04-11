

def get_path_alias(path: str) -> str:
    """Returns the first part of a relative path that starts with '/'"""
    return path.split('/')[1]


# testing
if __name__ == "__main__":
    test_path = "/catalogue/all"
    print(get_path_alias(test_path))

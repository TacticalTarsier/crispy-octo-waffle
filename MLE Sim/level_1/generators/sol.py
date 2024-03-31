import random

# Example of use
custom_first_names = ["Max", "Sophia", "Liam"]
custom_last_names = ["Miller", "Davis", "Garcia"]


def username_generator(n: int,
                       first_names: list = custom_first_names,
                       last_names: list = custom_last_names) -> dict:
    """Generates dict with ids, names of a username

    Args:
        n (int): _description_
        first_names (str, optional): _description_. Defaults to None.
        last_names (str, optional): _description_. Defaults to None.

    Yields:
        dict: usernames and ids dict
    """
    for i in range(1, n+1):
        yield {'id': i,
               'first_name': random.choice(first_names),
               'last_name': random.choice(last_names)}


# Example of use
for user in username_generator(3, custom_first_names, custom_last_names):
    print(user['id'], user['first_name'], user['last_name'])


def data_generator(n: int):
    """Generates tuple of two value: (x, y)

    Args:
        n (int): number of points

    Yields:
        Tuple: (x, y))
    """
    for i in range(0, n):
        yield (i, random.randint(0, 100))


# Example of use
for data in data_generator(3):
    print(data)

# Example of output:
# (0, 49)
# (1, 27)
# (2, 88)

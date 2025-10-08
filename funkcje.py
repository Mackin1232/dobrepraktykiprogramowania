import string


def is_palindrome(text: str) -> bool:
    if reversed(text) == text:
        return True
    return False


def fibonacci(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 2) + fibonacci(n - 1)


def count_vowels(text: str) -> int:
    counter = 0
    vowels = ["a", "e", "i", "o", "u", "y"]
    text = text.lower()
    for letter in text:
        if letter in vowels:
            counter += 1
    return counter


def calculate_discount(price: float, discount: float) -> float:
    if discount < 0 or discount > 1:
        raise ValueError("Zniżka powinna się mieścić w zakresie 0-1")
    return price - (price*discount)


#def flatten_list(nested_list: list) -> list:
    #flattened = []
    #for element in nested_list:
        #if isinstance(nested_list,list)


def word_frequencies(text: str) -> dict:
    text = text.lower()
    text = text.translate(string.maketrans("",""),string.punctuation)
    words = text.split(" ")
    words_dict = dict()
    for word in words:
        if word in words_dict:
            words_dict[word] += 1
        else:
            words_dict[word] = 1
    return words_dict

#def is_prime (n: int) -> bool:
    #if n < 2:
        #return False


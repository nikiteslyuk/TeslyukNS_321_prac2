import random
import cowsay
import urllib.request
import argparse
from collections import Counter


def bullscows(guess: str, secret: str) -> (int, int):
    bulls = sum(1 for g, s in zip(guess, secret) if g == s)
    cnt_guess = Counter(guess)
    cnt_secret = Counter(secret)
    common = sum(min(cnt_guess[c], cnt_secret[c]) for c in cnt_guess)
    cows = common - bulls
    return bulls, cows


def gameplay(ask, inform, words: list[str]) -> int:
    secret = random.choice(words)
    print(secret)
    attempts = 0
    while True:
        guess, local_attempts = ask("Введите слово", words)
        attempts += local_attempts
        b, c = bullscows(guess, secret)
        if guess == secret:
            inform("Попадание. Быки: {}, Коровы: {}", b, c)
            return attempts
        else:
            inform("Быки: {}, Коровы: {}", b, c)


def load_words(source: str, length: int) -> list[str]:
    if source.startswith("http://") or source.startswith("https://"):
        with urllib.request.urlopen(source) as response:
            data = response.read().decode("utf-8")
    else:
        with open(source, encoding="utf-8") as f:
            data = f.read()
    words = [w.strip() for w in data.split() if w.strip().isalpha()]
    words = [w.lower() for w in words if len(w) == length]
    if not words:
        print(f"Не найдено слов длины {length} в источнике {source}")
        exit(0)
    return words


def ask(prompt, valid=None):
    local_attempts = 0
    while True:
        cow_type = random.choice(cowsay.list_cows())
        print(cowsay.cowsay(prompt, cow=cow_type))
        inp = input().strip().lower()
        local_attempts += 1
        if valid is None or inp in valid:
            return inp, local_attempts
        print(
            cowsay.cowsay("Некорректное слово.", cow=random.choice(cowsay.list_cows()))
        )


def inform(fmt, bulls, cows):
    message = fmt.format(bulls, cows)
    cow_type = random.choice(cowsay.list_cows())
    print(cowsay.cowsay(message, cow=cow_type))


parser = argparse.ArgumentParser()
parser.add_argument("source", nargs="?", default="russian_nouns.txt")
# parser.add_argument("source", nargs="?", default="google-1000-english.txt")
parser.add_argument("length", nargs="?", type=int, default=5)
args = parser.parse_args()
words = load_words(args.source, args.length)


attempts = gameplay(ask, inform, words)
print("Количество попыток:", attempts)

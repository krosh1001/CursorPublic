import argparse
import random
import string
from typing import List


def build_charset(use_digits: bool, use_letters: bool, use_symbols: bool) -> str:
    charset_parts: List[str] = []

    if use_digits:
        charset_parts.append(string.digits)
    if use_letters:
        charset_parts.append(string.ascii_letters)
    if use_symbols:
        # Берём стандартный набор символов пунктуации
        charset_parts.append(string.punctuation)

    if not charset_parts:
        raise ValueError("Не выбран ни один тип символов для пароля.")

    return "".join(charset_parts)


def generate_password(length: int, charset: str) -> str:
    if length <= 0:
        raise ValueError("Длина пароля должна быть положительным числом.")

    rng = random.SystemRandom()
    return "".join(rng.choice(charset) for _ in range(length))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Генератор случайных паролей."
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=8,
        help="Длина пароля (по умолчанию 8).",
    )
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=1,
        help="Количество паролей для генерации (по умолчанию 1).",
    )
    parser.add_argument(
        "--no-digits",
        action="store_true",
        help="Не использовать цифры.",
    )
    parser.add_argument(
        "--no-letters",
        action="store_true",
        help="Не использовать буквы.",
    )
    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Не использовать специальные символы.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    use_digits = not args.no_digits
    use_letters = not args.no_letters
    use_symbols = not args.no_symbols

    try:
        charset = build_charset(use_digits, use_letters, use_symbols)
    except ValueError as exc:
        print(f"Ошибка: {exc}")
        raise SystemExit(1)

    if args.number <= 0:
        print("Ошибка: количество паролей должно быть положительным числом.")
        raise SystemExit(1)

    for _ in range(args.number):
        try:
            password = generate_password(args.length, charset)
        except ValueError as exc:
            print(f"Ошибка: {exc}")
            raise SystemExit(1)
        print(password)


if __name__ == "__main__":
    main()


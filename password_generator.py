import argparse
import random
import string
from typing import List


_RNG = random.SystemRandom()


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


def transform_word_to_leet(word: str) -> str:
    """
    Трансформирует слово в leet-стиль:
    - случайно меняет регистр букв;
    - заменяет некоторые буквы на похожие символы/цифры.
    """
    leet_map = {
        "a": ["4", "@"],
        "o": ["0"],
        "e": ["3"],
        "i": ["!"],
        "s": ["5", "$"],
    }

    transformed_chars: List[str] = []

    for ch in word:
        if ch.isalpha():
            lower = ch.lower()
            upper = ch.upper()

            # Буквы из leet-карты могут быть заменены на цифры/символы
            if lower in leet_map:
                # варианты: нижний регистр, верхний регистр, или символы из leet-карты
                options = [lower, upper] + leet_map[lower]
                transformed_chars.append(_RNG.choice(options))
            else:
                # для остальных — только случайный регистр
                transformed_chars.append(_RNG.choice([lower, upper]))
        else:
            transformed_chars.append(ch)

    return "".join(transformed_chars)


def generate_password(length: int, charset: str, word: str | None = None) -> str:
    if length <= 0:
        raise ValueError("Длина пароля должна быть положительным числом.")

    # Если слово не задано, генерируем обычный пароль
    if word is None:
        return "".join(_RNG.choice(charset) for _ in range(length))

    leet_word = transform_word_to_leet(word)
    word_len = len(leet_word)

    # Если слово длиннее запрошенной длины — пароль принимает длину слова
    if word_len >= length:
        return leet_word

    # Если слово короче — дополняем случайными символами до нужной длины
    remaining = length - word_len
    padding = "".join(_RNG.choice(charset) for _ in range(remaining))

    # Вставляем слово в случайную позицию в пределах итоговой длины
    insert_pos = _RNG.randint(0, remaining)
    prefix = padding[:insert_pos]
    suffix = padding[insert_pos:]

    return f"{prefix}{leet_word}{suffix}"


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
    parser.add_argument(
        "--word",
        type=str,
        help=(
            "Слово, которое будет включено в пароль и "
            "предварительно преобразовано в leet-стиль."
        ),
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
            password = generate_password(args.length, charset, args.word)
        except ValueError as exc:
            print(f"Ошибка: {exc}")
            raise SystemExit(1)
        print(password)


if __name__ == "__main__":
    main()


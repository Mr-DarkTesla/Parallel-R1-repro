"""Conservative fallbacks for benchmark answers that math_verify cannot parse."""
import re


_SUPERSCRIPTS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")


def normalize_superscripts(answer):
    return re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+", lambda m: "^" + m.group().translate(_SUPERSCRIPTS), answer)


def lone_number(answer):
    numbers = re.findall(r"(?<![\w])[-+]?\d+(?:\.\d+)?(?:/\d+)?%?(?![\w])", answer)
    return numbers[0] if len(numbers) == 1 else None

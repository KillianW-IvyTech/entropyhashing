import argparse
import sys


def caesar(text: str, shift: int) -> str:
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)


# can read text files

def read_file(path: str) -> str:
    for encoding in ("utf-8-sig", "utf-16"):
        try:
            with open(path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"error: file not found: {path}", file=sys.stderr)
            sys.exit(1)
        except PermissionError:
            print(f"error: permission denied: {path}", file=sys.stderr)
            sys.exit(1)
        except OSError as e:
            print(f"error: could not read file: {e}", file=sys.stderr)
            sys.exit(1)
    print(f"error: could not decode file as text: {path}", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt text using a Caesar cipher."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for cmd in ("encrypt", "decrypt"):
        sub = subparsers.add_parser(cmd, help=f"{cmd} text with a Caesar cipher")
        group = sub.add_mutually_exclusive_group(required=True)
        group.add_argument("-s", "--string", metavar="TEXT", help="text to process")
        group.add_argument("-f", "--file", metavar="PATH", help="file to process")
        sub.add_argument(
            "-k", "--key",
            type=int,
            required=True,
            metavar="N",
            help="shift amount (1-25)",
        )

    args = parser.parse_args()

    if not 1 <= args.key <= 25:
        print("error: key must be between 1 and 25", file=sys.stderr)
        sys.exit(1)

    shift = args.key if args.command == "encrypt" else -args.key

    if args.string is not None:
        text = args.string
    else:
        text = read_file(args.file)

    print(caesar(text, shift))


if __name__ == "__main__":
    main()

import argparse
import hashlib
import sys


def hash_string(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def hash_file(path: str) -> str:
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
    except FileNotFoundError:
        print(f"error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"error: permission denied: {path}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"error: could not read file: {e}", file=sys.stderr)
        sys.exit(1)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(
        description="Generate SHA-256 hashes for strings or files."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--string", metavar="TEXT", help="string to hash")
    group.add_argument("-f", "--file", metavar="PATH", help="file to hash")

    args = parser.parse_args()

    if args.string is not None:
        digest = hash_string(args.string)
        print(f'SHA-256("{args.string}"): {digest}')
    else:
        digest = hash_file(args.file)
        print(f"SHA-256({args.file}): {digest}")


if __name__ == "__main__":
    main()

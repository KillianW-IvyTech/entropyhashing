import argparse
import sys
from pathlib import Path

try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.exceptions import InvalidSignature
except ImportError:
    print("error: missing dependency. Run: pip install cryptography", file=sys.stderr)
    sys.exit(1)


def cmd_keygen(args):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    priv_path = Path(args.out_dir) / "private.pem"
    pub_path = Path(args.out_dir) / "public.pem"

    priv_path.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    pub_path.write_bytes(
        private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )
    print(f"Private key: {priv_path}")
    print(f"Public key:  {pub_path}")


def cmd_sign(args):
    priv_path = Path(args.key)
    if not priv_path.exists():
        print(f"error: key file not found: {priv_path}", file=sys.stderr)
        sys.exit(1)

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"error: file not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    private_key = serialization.load_pem_private_key(priv_path.read_bytes(), password=None)
    signature = private_key.sign(file_path.read_bytes(), padding.PKCS1v15(), hashes.SHA256())

    sig_path = Path(args.sig) if args.sig else file_path.with_suffix(file_path.suffix + ".sig")
    sig_path.write_bytes(signature)
    print(f"Signature written to: {sig_path}")


def cmd_verify(args):
    pub_path = Path(args.key)
    if not pub_path.exists():
        print(f"error: key file not found: {pub_path}", file=sys.stderr)
        sys.exit(1)

    file_path = Path(args.file)
    sig_path = Path(args.sig)

    if not file_path.exists():
        print(f"error: file not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    if not sig_path.exists():
        print(f"error: signature file not found: {sig_path}", file=sys.stderr)
        sys.exit(1)

    public_key = serialization.load_pem_public_key(pub_path.read_bytes())

    try:
        public_key.verify(sig_path.read_bytes(), file_path.read_bytes(), padding.PKCS1v15(), hashes.SHA256())
        print("Signature valid -- file is authentic and unmodified.")
    except InvalidSignature:
        print("Signature INVALID -- file may have been tampered with.", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Sign and verify files using RSA + SHA-256.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # keygen
    kg = subparsers.add_parser("keygen", help="generate an RSA key pair")
    kg.add_argument("--out-dir", default=".", metavar="DIR", help="directory to write keys (default: current dir)")
    kg.set_defaults(func=cmd_keygen)

    # sign
    sg = subparsers.add_parser("sign", help="sign a file with a private key")
    sg.add_argument("-f", "--file", required=True, metavar="PATH", help="file to sign")
    sg.add_argument("-k", "--key", default="private.pem", metavar="PATH", help="private key file (default: private.pem)")
    sg.add_argument("-s", "--sig", metavar="PATH", help="output signature file (default: <file>.sig)")
    sg.set_defaults(func=cmd_sign)

    # verify
    vf = subparsers.add_parser("verify", help="verify a file's signature with a public key")
    vf.add_argument("-f", "--file", required=True, metavar="PATH", help="file to verify")
    vf.add_argument("-s", "--sig", required=True, metavar="PATH", help="signature file")
    vf.add_argument("-k", "--key", default="public.pem", metavar="PATH", help="public key file (default: public.pem)")
    vf.set_defaults(func=cmd_verify)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

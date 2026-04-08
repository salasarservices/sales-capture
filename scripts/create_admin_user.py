#!/usr/bin/env python3
"""
Generate a bcrypt hash for a password to paste into .streamlit/secrets.toml.

Usage:
    python scripts/create_admin_user.py --password YourStrongPass

The script prints the hash — copy it into secrets.toml under
[credentials.<username>] password_hash = "..."

Note: Streamlit auth stores credentials in secrets.toml, not in MongoDB.
Users collection in MongoDB is retained for audit/reference only.
"""

import argparse
import sys

import bcrypt


def main(password: str, username: str, role: str):
    if len(password) < 8:
        print("Error: password must be at least 8 characters.", file=sys.stderr)
        sys.exit(1)

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode()

    print(f"\n# Add this block to .streamlit/secrets.toml:")
    print(f"\n[credentials.{username}]")
    print(f'password_hash = "{hashed}"')
    print(f'role = "{role}"')
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate bcrypt hash for secrets.toml")
    parser.add_argument("--username", default="admin", help="Username (used as TOML key)")
    parser.add_argument("--password", required=True)
    parser.add_argument("--role", default="admin", choices=["admin", "viewer"])
    args = parser.parse_args()
    main(args.password, args.username, args.role)

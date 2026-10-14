#!/usr/bin/env python3
"""Print a bookstore report: for each author in a list, show linked books."""

import logging
import os
import sys

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.server_api import ServerApi

# Credentials come from environment variables (never hardcode them)
MONGODB_ATLAS_URL = os.environ.get("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.environ.get("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.environ.get("MONGODB_ATLAS_PWD")

# Mix of loaded authors (002, 003) and one added in Case Study 1 (004)
AUTHOR_IDS = ["author_002", "author_003", "author_004"]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def print_report(db, author_ids):
    """Print each author's name and their linked books.

    Args:
        db: A PyMongo database object for 'bookstore'.
        author_ids: List of author _id values to report on.
    """
    authors = db["authors"]
    books = db["books"]

    # Count how many of the requested authors actually exist
    total = authors.count_documents({"_id": {"$in": author_ids}})
    print(f"Authors: {total}\n")

    # Look up each author, then find books whose author_ids contains that _id
    for author in authors.find({"_id": {"$in": author_ids}}).sort("name"):
        print(author["name"])
        for book in books.find({"author_ids": author["_id"]}):
            print(f"  {book['title']} ({book['published_year']})")
        print()


def main():
    """Connect to MongoDB Atlas, print the report, and close the client."""
    if not all([MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD]):
        logging.error("Missing one or more MONGODB_ATLAS_* environment variables.")
        sys.exit(1)

    client = None
    try:
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            server_api=ServerApi("1"),
        )
        client.admin.command("ping")  # forces a real connection check
        logging.info("Connected to MongoDB Atlas")

        db = client["bookstore"]
        print_report(db, AUTHOR_IDS)
    except PyMongoError as err:
        logging.error("MongoDB error: %s", err)
        sys.exit(1)
    finally:
        if client is not None:
            client.close()
            logging.info("Connection closed")


if __name__ == "__main__":
    main()
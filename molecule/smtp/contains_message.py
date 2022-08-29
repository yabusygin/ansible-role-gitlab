#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from email import message_from_binary_file, policy
from mailbox import Maildir, MaildirMessage
from pathlib import Path
from sys import exit
from typing import IO, Optional, NamedTuple


DEBUG_ENABLED = False


class MessageFilter(NamedTuple):
    from_: Optional[str]
    reply_to: Optional[str]
    to: Optional[str]
    subject: Optional[str]

    @classmethod
    def create(cls, args: Namespace) -> "MessageFilter":
        return cls(
            from_=args.from_,
            reply_to=args.reply_to,
            to=args.to,
            subject=args.subject,
        )


def debug(message: str) -> None:
    if DEBUG_ENABLED:
        print(message)


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--count", type=int)
    parser.add_argument("--from", dest="from_")
    parser.add_argument("--reply-to")
    parser.add_argument("--to")
    parser.add_argument("--subject")
    parser.add_argument("--maildir-path", type=Path, required=True)
    return parser.parse_args()


def message_factory(stream: IO[bytes]) -> MaildirMessage:
    message = message_from_binary_file(fp=stream, policy=policy.default)
    return MaildirMessage(message)


def match_address(message: MaildirMessage, header: str, value: str) -> bool:
    if header not in message:
        if value == "!":
            return True
        return False
    if len(message[header].addresses) != 1:
        return False
    if str(message[header].addresses[0]) != value:
        return False
    return True


def match_string(message: MaildirMessage, header: str, value: str) -> bool:
    if header not in message:
        if value == "!":
            return True
        return False
    if message[header] != value:
        return False
    return True


def match(message: MaildirMessage, message_filter: MessageFilter) -> bool:
    if message_filter.from_ is not None:
        if not match_address(message, "From", message_filter.from_):
            return False
    if message_filter.reply_to is not None:
        if not match_address(message, "Reply-To", message_filter.reply_to):
            return False
    if message_filter.to is not None:
        if not match_address(message, "To", message_filter.to):
            return False
    if message_filter.subject is not None:
        if not match_string(message, "Subject", message_filter.subject):
            return False
    return True


def main() -> None:
    args = parse_args()
    global DEBUG_ENABLED
    DEBUG_ENABLED = args.debug
    mailbox = Maildir(
        dirname=args.maildir_path,
        factory=message_factory,
        create=False,
    )
    message_filter = MessageFilter.create(args)
    debug("filter: {}".format(message_filter))
    matches = 0
    for message in mailbox:
        debug(
            "message: {}".format(
                (
                    message.get("From"),
                    message.get("Reply-To"),
                    message.get("To"),
                    message.get("Subject"),
                ),
            ),
        )
        if match(message, message_filter):
            matches += 1
            debug("matched: {}".format(matches))
    if args.count is None or args.count == matches:
        exit(0)
    exit(1)


if __name__ == "__main__":
    main()

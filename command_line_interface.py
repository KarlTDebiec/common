#!/usr/bin/env python
#  Copyright 2017-2023 Karl T Debiec
#  All rights reserved. This software may be modified and distributed under
#  the terms of the BSD license. See the LICENSE file for details.
"""Abstract base class for command-line interfaces."""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from argparse import ArgumentParser, RawDescriptionHelpFormatter, _SubParsersAction
from inspect import cleandoc
from typing import Any, Optional

from .logging import set_logging_verbosity


class CommandLineInterface(ABC):
    """Abstract base class for command-line interfaces."""

    @classmethod
    def add_arguments_to_argparser(cls, parser: ArgumentParser) -> None:
        """Add arguments to a nascent argument parser.

        Arguments:
            parser: Nascent argument parser
        """
        verbosity = parser.add_mutually_exclusive_group()
        verbosity.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=1,
            dest="verbosity",
            help="enable verbose output, may be specified more than once",
        )
        verbosity.add_argument(
            "-q",
            "--quiet",
            action="store_const",
            const=0,
            dest="verbosity",
            help="disable verbose output",
        )

    @classmethod
    def argparser(
        cls, *, subparsers: Optional[_SubParsersAction] = None
    ) -> ArgumentParser:
        """Construct argument parser.

        Arguments:
            subparsers: Subparsers group to which a new subparser will be added; if
              None, a new ArgumentParser will be created
        Returns:
            Argument parser
        """
        if not subparsers:
            parser = ArgumentParser(
                description=str(cls.description()),
                formatter_class=RawDescriptionHelpFormatter,
            )
        else:
            parser = subparsers.add_parser(
                name=cls.name(),
                description=cls.description(),
                help=cls.help(),
                formatter_class=RawDescriptionHelpFormatter,
            )

        cls.add_arguments_to_argparser(parser)

        return parser

    @classmethod
    def description(cls) -> str:
        """Long description of this tool displayed below usage."""
        return cleandoc(cls.__doc__) if cls.__doc__ else ""

    @classmethod
    def help(cls) -> str:
        """Short description of this tool used when it is a subparser."""
        text = re.split(r"\.\s+", str(cls.description()))[0].rstrip(".")
        return text[0].lower() + text[1:]

    @classmethod
    @abstractmethod
    def main(cls) -> None:
        """Execute from command line."""
        parser = cls.argparser()
        kwargs = vars(parser.parse_args())
        verbosity = kwargs.pop("verbosity", 1)
        set_logging_verbosity(verbosity)

        cls.main_internal(**kwargs)

    @classmethod
    @abstractmethod
    def main_internal(cls, **kwargs: Any) -> None:
        """Execute with provided keyword arguments."""
        raise NotImplementedError()

    @classmethod
    def name(cls) -> str:
        """Name of this tool used to define it when it is a subparser."""
        return cls.__name__.lower()

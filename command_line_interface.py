#!/usr/bin/env python
#  Copyright 2017-2023 Karl T Debiec
#  All rights reserved. This software may be modified and distributed under
#  the terms of the BSD license. See the LICENSE file for details.
"""Abstract base class for command-line interfaces."""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from argparse import (
    ArgumentParser,
    ArgumentTypeError,
    RawDescriptionHelpFormatter,
    _ArgumentGroup,
    _SubParsersAction,
)
from inspect import cleandoc
from pathlib import Path
from typing import Any, Callable, Optional

from .validation import (
    validate_float,
    validate_input_directories,
    validate_input_directory,
    validate_input_file,
    validate_input_files,
    validate_int,
    validate_ints,
    validate_output_directory,
    validate_output_file,
    validate_str,
)


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
    def float_arg(cls, **kwargs: Any) -> Callable[[Any], float]:
        """Validate a float argument.

        Arguments:
            **kwargs: Keyword arguments to pass to validate_float
        Returns:
            Value validator function
        """
        return cls.get_validator(validate_float, **kwargs)

    @classmethod
    @abstractmethod
    def execute(cls, **kwargs: Any) -> None:
        """Execute with provided keyword arguments.

        Arguments:
            **kwargs: Command-line arguments
        """
        raise NotImplementedError()

    @classmethod
    def help(cls) -> str:
        """Short description of this tool used when it is a subparser."""
        return re.split(r"\.\s+", str(cls.description()))[0].rstrip(".")

    @classmethod
    def input_directories_arg(cls, **kwargs: Any) -> Callable[[Any], list[Path]]:
        """Validate an input directory paths argument.

        Arguments:
            **kwargs: Keyword arguments to pass to validate_input_directory_paths
        Returns:
            Value validator function
        """
        return cls.get_validator(validate_input_directories, **kwargs)

    @classmethod
    def input_directory_arg(cls, **kwargs: Any) -> Callable[[Any], Path]:
        """Validate an input directory path argument.

        Arguments:
            **kwargs: Keyword arguments to pass to validate_input_directory_path
        Returns:
            Value validator function
        """
        return cls.get_validator(validate_input_directory, **kwargs)

    @classmethod
    def input_file_arg(cls, **kwargs: Any) -> Callable[[Any], Path]:
        """Validate an input file path argument.

        Arguments:
            **kwargs: Keyword arguments to pass to validate_input_file_path
        Returns:
            Value validator function
        """
        return cls.get_validator(validate_input_file, **kwargs)

    @classmethod
    def input_files_arg(cls, **kwargs: Any) -> Callable[[Any], list[Path]]:
        """Validate an input file paths argument.

        Arguments:
            **kwargs: Keyword arguments to pass to validate_input_file_paths
        Returns:
            Value validator function
        """
        return cls.get_validator(validate_input_files, **kwargs)

    @classmethod
    def int_arg(cls, **kwargs: Any) -> Callable[[Any], int]:
        """Validate an int argument.

        Arguments:
            **kwargs: Keyword arguments to pass to validate_int
        Returns:
            Value validator function
        """
        return cls.get_validator(validate_int, **kwargs)

    @classmethod
    def ints_arg(cls, **kwargs: Any) -> Callable[[Any], int]:
        """Validate a tuple of ints argument.

        Arguments:
            **kwargs: Keyword arguments to pass to validate_ints
        Returns:
            Value validator function
        """
        return cls.get_validator(validate_ints, **kwargs)

    @classmethod
    def main(cls) -> None:
        """Execute from command line."""
        parser = cls.argparser()
        kwargs = vars(parser.parse_args())
        cls.execute(**kwargs)

    @classmethod
    def name(cls) -> str:
        """Name of this tool used to define it when it is a subparser."""
        return cls.__name__

    @classmethod
    def output_directory_arg(cls, **kwargs: Any) -> Callable[[Any], Path]:
        """Validate an output directory path argument.

        Arguments:
            **kwargs: Keyword arguments to pass to validate_output_directory_path
        Returns:
            Value validator function
        """
        return cls.get_validator(validate_output_directory, **kwargs)

    @classmethod
    def output_file_arg(cls, **kwargs: Any) -> Callable[[Any], Path]:
        """Validate an output file path argument.

        Arguments:
            **kwargs: Keyword arguments to pass to validate_output_file_path
        Returns:
            Value validator function
        """
        return cls.get_validator(validate_output_file, **kwargs)

    @classmethod
    def str_arg(cls, **kwargs: Any) -> Callable[[Any], str]:
        """Validate a string argument.

        Arguments:
            **kwargs: Keyword arguments to pass to validate_str
        Returns:
            Value validator function
        """
        return cls.get_validator(validate_str, **kwargs)

    @staticmethod
    def get_optional_arguments_group(parser: ArgumentParser) -> _ArgumentGroup:
        """Get the 'optional arguments' group from an argparser.

        Arguments:
            parser: Argparser to get group from
        Returns:
            Optional arguments group
        """
        return next(
            ag
            for ag in parser._action_groups  # noqa
            if ag.title == "optional arguments"
        )

    @staticmethod
    def get_required_arguments_group(parser: ArgumentParser) -> _ArgumentGroup:
        """Get or create a 'required arguments' group from an argparser.

        Arguments:
            parser: Argparser to get group from
        Returns:
            Required arguments group
        """
        if any(
            (required := ag).title == "required arguments"
            for ag in parser._action_groups  # noqa
        ):
            return required  # noqa

        # Move "optional arguments" group below "required arguments" group
        optional = parser._action_groups.pop()  # noqa
        required = parser.add_argument_group("required arguments")
        parser._action_groups.append(optional)  # noqa

        return required

    @staticmethod
    def get_validator(function: Callable, **kwargs: Any) -> Callable:
        """Get a function that can be called with the same signature as function.

        Arguments:
            function: Function to be wrapped
        Returns:
            Wrapped function
        """

        def wrapped(value: Any) -> Any:
            try:
                return function(value, **kwargs)
            except TypeError as error:
                raise ArgumentTypeError from error

        return wrapped

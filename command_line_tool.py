#!/usr/bin/env python
#   Copyright (C) 2017-2022 Karl T Debiec
#   All rights reserved. This software may be modified and distributed under
#   the terms of the BSD license. See the LICENSE file for details.
"""General-purpose command-line tool base class."""
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
from typing import Any, Callable, Iterable, Optional, Union

from .general import set_logging_verbosity
from .validation import (
    validate_float,
    validate_input_path,
    validate_int,
    validate_ints,
    validate_output_path,
    validate_str,
)


class CommandLineTool(ABC):
    """General-purpose command-line tool base class."""

    def __init__(self, verbosity: int = 1, **kwargs: Any) -> None:
        """Validate and store configuration.

        Arguments:
            verbosity: Verbosity of logging
            **kwargs: Additional keyword arguments
        """
        self.verbosity = validate_int(verbosity, min_value=0)
        set_logging_verbosity(self.verbosity)

    @abstractmethod
    def __call__(self):
        """Perform operations."""
        raise NotImplementedError()

    @classmethod
    def add_arguments_to_argparser(
        cls,
        parser: Union[ArgumentParser, _SubParsersAction],
    ) -> None:
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
    def construct_argparser(
        cls,
        parser: Optional[_SubParsersAction] = None,
    ) -> Union[ArgumentParser, _SubParsersAction]:
        """Construct argument parser.

        Arguments:
            parser: May be a one of 1) a pre-existing argument parser, to which
              arguments will be added, 2) a pre-existing subparsers group, to which a
              new subparser with arguments will be added, or 3) None, in which case a
              new parser will be created with arguments
        Returns:
            Argument parser
        """
        if parser is None:
            parser = ArgumentParser(
                description=str(cls.description),
                formatter_class=RawDescriptionHelpFormatter,
            )
        if isinstance(parser, _SubParsersAction):
            parser = parser.add_parser(
                name=cls.name,
                description=cls.description,
                help=cls.help,
                formatter_class=RawDescriptionHelpFormatter,
            )

        cls.add_arguments_to_argparser(parser)

        return parser

    @classmethod
    def main(cls) -> None:
        """Parse arguments, construct tool, and call tool."""
        parser = cls.construct_argparser()
        kwargs = vars(parser.parse_args())

        tool = cls(**kwargs)
        tool()

    @classmethod
    @property
    def description(cls) -> str:
        """Long description of this tool displayed below usage."""
        return cleandoc(cls.__doc__) if cls.__doc__ is not None else ""

    @classmethod
    @property
    def help(cls) -> str:
        """Short description of this tool used when it is a subparser."""
        # noinspection PyTypeChecker
        return re.split(r"\.\s+", cls.description)[0].rstrip(".")

    @classmethod
    @property
    def name(cls) -> str:
        """Name of this tool used to define it when it is a subparser."""
        return cls.__name__

    @staticmethod
    def float_arg(
        min_value: Optional[float] = None, max_value: Optional[float] = None
    ) -> Callable[[Any], float]:
        """Validate a float argument.

        Arguments:
            min_value: Minimum permissible value
            max_value: Maximum permissible value
        Returns:
            Value validator function
        """

        def func(value: Any) -> float:
            try:
                return validate_float(value, min_value, max_value)
            except TypeError as error:
                raise ArgumentTypeError from error

        return func

    @staticmethod
    def get_optional_arguments_group(
        parser: Union[ArgumentParser, _SubParsersAction],
    ) -> _ArgumentGroup:
        """Get the 'optional arguments' group from a nascent argparser."""
        return next(
            ag for ag in parser._action_groups if ag.title == "optional arguments"
        )

    @staticmethod
    def get_required_arguments_group(
        parser: Union[ArgumentParser, _SubParsersAction],
    ) -> _ArgumentGroup:
        """Get or create a 'required arguments' group from a nascent argparser."""
        if any(
            (required := ag).title == "required arguments"
            for ag in parser._action_groups
        ):
            return required
        optional = parser._action_groups.pop()
        required = parser.add_argument_group("required arguments")
        parser._action_groups.append(optional)
        return required

    @staticmethod
    def input_path_arg(
        file_ok: bool = True,
        directory_ok: bool = False,
        default_directory: Optional[str] = None,
    ) -> Callable[[Any], str]:
        """Validate an input path argument.

        Arguments:
            file_ok: Whether  file paths are permissible
            directory_ok: Whether  directory paths are permissible
            default_directory: Default directory to prepend to *value* if not absolute;
              default: current working directory
        Returns:
            Value validator function
        """

        def func(value: Any) -> str:
            try:
                return validate_input_path(
                    value, file_ok, directory_ok, default_directory
                )
            except TypeError as error:
                raise ArgumentTypeError from error

        return func

    @staticmethod
    def int_arg(
        min_value: Optional[int] = None, max_value: Optional[int] = None
    ) -> Callable[[Any], int]:
        """Validate an int argument.

        Arguments:
            min_value: Minimum permissible value
            max_value: Maximum permissible value
        Returns:
            Value validator function
        """

        def func(value: Any) -> int:
            try:
                return validate_int(value, min_value, max_value)
            except TypeError as error:
                raise ArgumentTypeError from error

        return func

    @staticmethod
    def ints_arg(
        length: Optional[int] = None,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
    ) -> Callable[[Any], tuple[int]]:
        """Validate a tuple of ints argument.

        Arguments:
            length: Number of values required
            min_value: Minimum permissible value
            max_value: Maximum permissible value
        Returns:
            Value validator function
        """

        def func(value: Any) -> tuple[int]:
            try:
                return validate_ints(value, length, min_value, max_value)
            except TypeError as error:
                raise ArgumentTypeError from error

        return func

    @staticmethod
    def output_path_arg(
        file_ok: bool = True,
        directory_ok: bool = False,
        default_directory: Optional[str] = None,
    ) -> Callable[[Any], str]:
        """Validate an output path argument.

        Arguments:
            file_ok: Whether file paths are permissible
            directory_ok: Whether directory paths are permissible
            default_directory: Default directory to prepend to *value* if not absolute;
              default: current working directory
        Returns:
            Value validator function
        """

        def func(value: Any) -> str:
            try:
                return validate_output_path(
                    value, file_ok, directory_ok, default_directory
                )
            except TypeError as error:
                raise ArgumentTypeError from error

        return func

    @staticmethod
    def str_arg(options: Iterable[str]) -> Callable[[Any], str]:
        """Validate a string argument.

        Arguments:
            options: Permissible values
        Returns:
            Value validator function
        """

        def func(value: Any) -> str:
            try:
                return validate_str(value, options)
            except TypeError as error:
                raise ArgumentTypeError from error

        return func

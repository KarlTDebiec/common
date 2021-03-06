#!/usr/bin/env python
#   common/cltool.py
#
#   Copyright (C) 2017-2021 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""General-purpose command-line tool base class not tied to a particular
project."""
####################################### MODULES ########################################
from abc import ABC, abstractmethod
from argparse import (
    ArgumentParser,
    ArgumentTypeError,
    RawDescriptionHelpFormatter,
    _SubParsersAction,
)
from typing import Any, Callable, Optional, Union

from .validation import (
    validate_float,
    validate_input_path,
    validate_int,
    validate_output_path,
)


####################################### CLASSES ########################################
class CLTool(ABC):
    """Abstract base class for command line tools."""

    # region Builtins

    def __init__(self, verbosity: int = 1, **kwargs: Any) -> None:
        """Initialize, including argument validation and value storage."""
        self.verbosity = validate_int(verbosity, min_value=0)

    @abstractmethod
    def __call__(self) -> Any:
        """Perform operations."""
        raise NotImplementedError()

    # endregion

    # region Class Methods

    @classmethod
    def construct_argparser(cls, **kwargs: Any) -> ArgumentParser:
        """
        Constructs argument parser.

        Args:
            kwargs (Any): Additional keyword arguments

        Returns:
            ArgumentParser: Argument parser
        """
        description = kwargs.get("description", __doc__.strip())
        # noinspection PyTypeChecker
        parser: Union[ArgumentParser, _SubParsersAction] = kwargs.get(
            "parser",
            ArgumentParser(
                description=description, formatter_class=RawDescriptionHelpFormatter
            ),
        )
        if isinstance(parser, _SubParsersAction):
            parser = parser.add_parser(
                name=cls.__name__.lower(),
                description=description,
                help=description,
                formatter_class=RawDescriptionHelpFormatter,
            )

        # General
        verbosity = parser.add_mutually_exclusive_group()
        verbosity.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=1,
            dest="verbosity",
            help="enable verbose output, may be specified " "more than once",
        )
        verbosity.add_argument(
            "-q",
            "--quiet",
            action="store_const",
            const=0,
            dest="verbosity",
            help="disable verbose output",
        )

        return parser

    @classmethod
    def main(cls) -> None:
        """Parses arguments, constructs tool, and calls tool."""
        parser = cls.construct_argparser()
        kwargs = vars(parser.parse_args())
        tool = cls(**kwargs)
        tool()

    # endregion

    # region Static methods

    @staticmethod
    def float_arg(
        min_value: Optional[float] = None, max_value: Optional[float] = None
    ) -> Callable[[Any], float]:
        """
        Validates a float argument.

        Args:
            min_value (Optional[float]): Minimum permissible value
            max_value (Optional[float]): Maximum permissible value

        Returns:
            Callable[[Any], float]: Value validator function
        """

        def func(value: Any) -> float:
            try:
                return validate_float(value, min_value, max_value)
            except TypeError as e:
                raise ArgumentTypeError(e)

        return func

    @staticmethod
    def input_path_arg(
        file_ok: bool = True,
        directory_ok: bool = False,
        default_directory: Optional[str] = None,
    ) -> Callable[[Any], str]:
        """
        Validates an input path argument.

        Args:
            file_ok (bool): Whether or not file paths are permissible
            directory_ok (bool): Whether or not directory paths are permissible
            default_directory (Optional[str]): Default directory to prepend to *value*
               if not absolute (default: current working directory)

        Returns:
            Callable[[Any], str]: Value validator function
        """

        def func(value: Any) -> str:
            try:
                return validate_input_path(
                    value, file_ok, directory_ok, default_directory
                )
            except TypeError as e:
                raise ArgumentTypeError(e)

        return func

    @staticmethod
    def int_arg(
        min_value: Optional[int] = None, max_value: Optional[int] = None
    ) -> Callable[[Any], int]:
        """
        Validates an int argument.

        Args:
            min_value (Optional[int]): Minimum permissible value
            max_value (Optional[int]): Maximum permissible value

        Returns:
            Callable[[Any], int]: Value validator function
        """

        def func(value: Any) -> int:
            try:
                return validate_int(value, min_value, max_value)
            except TypeError as e:
                raise ArgumentTypeError(e)

        return func

    @staticmethod
    def output_path_arg(
        file_ok: bool = True,
        directory_ok: bool = False,
        default_directory: Optional[str] = None,
    ) -> Callable[[Any], str]:
        """
        Validates an output path argument.

        Args:
            file_ok (bool): Whether or not file paths are permissible
            directory_ok (bool): Whether or not directory paths are permissible
            default_directory (Optional[str]): Default directory to prepend to *value*
               if not absolute (default: current working directory)

        Returns:
            Callable[[Any], str]: Value validator function
        """

        def func(value: Any) -> str:
            try:
                return validate_output_path(
                    value, file_ok, directory_ok, default_directory
                )
            except TypeError as e:
                raise ArgumentTypeError(e)

        return func

    # endregion

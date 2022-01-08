#!/usr/bin/env python
#   common/command_line_tool.py
#
#   Copyright (C) 2017-2022 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""General-purpose command-line tool base class not tied to a particular project"""
import logging
from abc import ABC, abstractmethod
from argparse import (
    ArgumentParser,
    ArgumentTypeError,
    RawDescriptionHelpFormatter,
    _SubParsersAction,
)
from inspect import cleandoc
from typing import Any, Callable, Iterable, List, Optional, Tuple, Union

from .validation import (
    validate_float,
    validate_input_path,
    validate_int,
    validate_ints,
    validate_output_path,
    validate_str,
)


class CommandLineTool(ABC):
    """General-purpose command-line tool base class not tied to a particular project"""

    def __init__(self, verbosity: int = 1, **kwargs: Any) -> None:
        """
        Validate and store static configuration

        Args:
            verbosity: Verbosity of logging
            **kwargs: Additional keyword arguments
        """
        self.verbosity = validate_int(verbosity, min_value=0)
        if self.verbosity <= 0:
            logging.basicConfig(level=logging.ERROR)
        elif self.verbosity == 1:
            logging.basicConfig(level=logging.WARNING)
        elif self.verbosity == 2:
            logging.basicConfig(level=logging.INFO)
        elif self.verbosity >= 3:
            logging.basicConfig(level=logging.DEBUG)

    @abstractmethod
    def __call__(self, **kwargs: Any) -> Any:
        """Perform operations"""
        raise NotImplementedError()

    @classmethod
    def construct_argparser(cls, **kwargs: Any) -> ArgumentParser:
        """
        Construct argument parser

        Arguments:
            **kwargs: Additional keyword arguments

        Returns:
            Argument parser
        """
        description = kwargs.pop(
            "description", cleandoc(cls.__doc__) if cls.__doc__ is not None else ""
        )
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

        return parser

    @classmethod
    def main(cls) -> None:
        """Parse argument, construct tool, and call tool"""
        parser = cls.construct_argparser()
        kwargs = vars(parser.parse_args())

        tool = cls(**kwargs)
        tool()

    @staticmethod
    def float_arg(
        min_value: Optional[float] = None, max_value: Optional[float] = None
    ) -> Callable[[Any], float]:
        """
        Validates a float argument.

        Arguments:
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

        Arguments:
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

        Arguments:
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
    def ints_arg(
        length: Optional[int] = None,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
    ) -> Callable[[Any], Tuple[int]]:
        """
        Validates a tuple of ints argument.

        Arguments:
            length (Optional[int]): Number of values required
            min_value (Optional[int]): Minimum permissible value
            max_value (Optional[int]): Maximum permissible value

        Returns:
            Callable[[Any], int]: Value validator function
        """

        def func(value: Any) -> Tuple[int]:
            try:
                return validate_ints(value, length, min_value, max_value)
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

        Arguments:
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

    @staticmethod
    def str_arg(options: Iterable[str]) -> Callable[[Any], str]:
        """
        Validates a string argument.

        Arguments:
            options (List[str]): Permissible values

        Returns:
            Callable[[Any], float]: Value validator function
        """

        def func(value: Any) -> str:
            try:
                return validate_str(value, options)
            except TypeError as e:
                raise ArgumentTypeError(e)

        return func
"""
This class make plotting more convenient.
It caches which color/symbol combination was already used in
"""
import pickle
from typing import Any, Dict, List, Tuple
from pathlib import Path
import json
import logging


class PlotHelper:
    """A Class to help get uniform colors and symbols across many plots."""

    _color_dict: Dict[str, str]
    _symbol_dict: Dict[str, str]
    _colors: List[str]
    _colors_index: int
    _symbols: List[str]
    _symbols_index: int
    _save_path: Path

    def __init__(self, config: Dict[str, Any]) -> None:
        self._color_dict = {}
        self._symbol_dict = {}
        self._colors = config["colors"]
        self._colors_index = 0
        self._symbols = config["symbols"]
        self._symbols_index = 0
        self._save_path = Path(config["save_path"])
        self._unique_timeout = config["unique_timeout"]

        if not self._save_path.exists():
            self._save_path.touch()

        for sequence in config["initialization_sequences"]:
            self.get_symbol(sequence)
            self.get_color(sequence)

        self._color_dict.update(config["color_overrides"])
        self._symbol_dict.update(config["symbol_overrides"])

        self.save()

    def get_color(self, key: str) -> str:
        """
        returns the color associated with a given key.
        """
        if key not in self._color_dict:
            self._color_dict.update(
                {key: self._colors[self._colors_index % len(self._colors)]}
            )
            self._colors_index += 1
            self.save()
        return self._color_dict[key]

    def get_symbol(self, key: str) -> str:
        """
        returns the symbol associated with a given key.
        """
        if key not in self._symbol_dict:
            self._symbol_dict.update(
                {key: self._symbols[self._symbols_index % len(self._symbols)]}
            )
            self._symbols_index += 1
            self.save()
        return self._symbol_dict[key]

    def get_both(self, key: str) -> Tuple[str, str]:
        """
        Returns both color and symbol for key.
        """
        return (self.get_color(key), self.get_symbol(key))

    def save(self) -> None:
        """
        Saves the plot helper to its save_path.
        Should not be necessary to call as the get functions will save.
        """
        with open(self._save_path, "wb+") as file:
            pickle.dump(self, file)


def get_plot_helper(
    plot_helper_config_path: Path,
) -> PlotHelper:
    "Returns a plot helper if it exists, and a fresh one if it doesn't"

    with open(plot_helper_config_path, "r", encoding="utf-8") as file:
        config = json.load(file)

    save_path = Path(config["save_path"])

    if save_path.is_file():
        logging.info("Loading Plothelper at %s", save_path)
        with open(save_path, "rb") as file:
            return pickle.load(file)
    else:
        return PlotHelper(config)

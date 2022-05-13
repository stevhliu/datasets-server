from typing import Any, List

from datasets import Audio
from numpy import ndarray  # type:ignore

from worker.models.asset import create_audio_files
from worker.models.column.default import (
    Cell,
    CellTypeError,
    Column,
    ColumnInferenceError,
    ColumnType,
    ColumnTypeError,
)


def check_value(value: Any) -> None:
    if value is not None:
        try:
            path = value["path"]
            array = value["array"]
        except Exception as e:
            raise CellTypeError("audio cell must contain 'path' and 'array' fields") from e
        if type(path) != str:
            raise CellTypeError("'path' field must be a string")
        if type(array) != ndarray:
            raise CellTypeError("'array' field must be a numpy.ndarray")


def infer_from_values(values: List[Any]) -> None:
    for value in values:
        check_value(value)
    if values and all(value is None for value in values):
        raise ColumnInferenceError("all the values are None, cannot infer column type")


class AudioColumn(Column):
    def __init__(self, name: str, feature: Any, values: List[Any]):
        if feature:
            if not isinstance(feature, Audio):
                raise ColumnTypeError("feature type mismatch")
        else:
            infer_from_values(values)
        self.name = name
        self.type = ColumnType.AUDIO_RELATIVE_SOURCES

    def get_cell_value(self, dataset_name: str, config_name: str, split_name: str, row_idx: int, value: Any) -> Cell:
        if value is None:
            return None
        check_value(value)
        array = value["array"]
        sampling_rate = value["sampling_rate"]
        # this function can raise, we don't catch it
        return create_audio_files(dataset_name, config_name, split_name, row_idx, self.name, array, sampling_rate)
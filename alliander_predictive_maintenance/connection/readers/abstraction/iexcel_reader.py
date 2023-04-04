import abc
from pathlib import Path

from alliander_predictive_maintenance.connection.readers.abstraction.dataframe_validator import DataFrameValidator


class IExcelReader(DataFrameValidator, metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load') and
                callable(subclass.load) or
                NotImplemented)

    @abc.abstractmethod
    def load(self, absolute_data_file_path: Path) -> None:
        """Load the data set
        :param absolute_data_file_path: path to the Excel data file
        """
        raise NotImplementedError

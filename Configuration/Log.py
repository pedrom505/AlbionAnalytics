from Configuration import Config
import os


class LogConfiguration(Config):

    def log_path(self) -> str:
        file_path = self._get_property("LOG:Path")
        file_name = self._get_property("LOG:FileName")
        log_path = os.path.join(file_path, file_name)
        return log_path

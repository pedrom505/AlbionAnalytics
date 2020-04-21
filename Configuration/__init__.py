import configparser
import logging
import Errors
import os


class Config:
    """
    This class uses the singletone design patters and your goal is provide some methods to access and edit the
    configuration file of application
    """
    _instance = None

    def __init__(self, file_location: str = "setup.ini"):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"<file_location> = {file_location}")
        if Config._instance is None:
            if os.path.exists(file_location):
                self.logger.debug(f"File {file_location} founded!")
                self.__file_path = file_location
                self.__config = configparser.ConfigParser()
                self.__config.read(file_location)
                Config._instance = self
            else:
                raise Errors.FileNotFounded("The configuration file wasn't founded")

    def _set_property(self, property_path: str, property_value):
        property_path_split = property_path.split(":")

        if len(property_path_split) == 2:

            section_name = property_path_split[0]
            node_name = property_path_split[1]

            if section_name in self.__config:
                self.__config[section_name][node_name] = f"{property_value}"
            else:
                self.__config[section_name] = {}
                self.__config[section_name][node_name] = f"{property_value}"

            with open(self.__file_path, 'w') as config_file:
                self.__config.write(config_file)
        else:
            raise Errors.InvalidParameter

    def _get_property(self, property_path: str):
        property_path_split = property_path.split(":")

        if len(property_path_split) == 2:

            section_name = property_path_split[0]
            node_name = property_path_split[1]
            try:
                node = self.__config[section_name][node_name]
                node = self._replace_expression(node)
                return node
            except KeyError:
                raise Errors.InvalidParameter("The specified property does not exist in the configuration file!")
        else:
            raise Errors.InvalidParameter("Invalid property structure for the configuration file!")

    @staticmethod
    def _replace_expression(content: str) -> str:
        if "$(root_dir)" in content:
            content = content.replace("$(root_dir)", os.getcwd())
        return content



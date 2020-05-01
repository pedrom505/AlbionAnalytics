import os
from typing import IO
import Errors


class Items:

    items = dict({"items": []})

    def __init__(self):
        root_path = os.getcwd()
        items_template_path = os.path.join(root_path, "AlbionOnlineData", "Templates", "Items.txt")
        fd = open(items_template_path)
        self._load_file(fd)
        fd.close()

    def _load_file(self, file_descriptor: IO):
        for line in file_descriptor:
            line_splited = line.split(":")
            for count in range(len(line_splited), 3):
                line_splited.append("")
            item_descriptor = line_splited[1].replace(" ", "").replace("\n", "")
            item_name = line_splited[2].replace("\n", "")

            self.items["items"].append({"descriptor": item_descriptor, "name": item_name})

    def get_item_by_id(self, item_id: int) -> dict:
        if item_id <= len(self.items["items"]):
            item = self.items["items"][item_id]
            return item
        else:
            raise Errors.InternalError("Item not found")

    def get_item_by_descriptor(self, item_descriptor: str) -> dict:
        for item in self.items["items"]:
            if item["descriptor"] in item_descriptor:
                return item
        raise Errors.InternalError("Item not found")

    def get_item_by_name_piece(self, name_piece: str) -> list:
        item_list = []
        for item in self.items["items"]:
            if name_piece.lower() in item["name"].lower():
                item_list.append(item)

        if len(item_list) > 0:
            return item_list
        else:
            raise Errors.InternalError("Item not found")

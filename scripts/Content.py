from datetime import datetime
from .sql import execute
import hashlib
import base64
import json

DATABASE = "data/piratebay.db"
TABLE = "courses"

class Content:

    def __init__(self, data:str):
        self.type=data.get("type")
        self.name=data["title"].get("name")
        self.link=data["title"].get("link")
        self.uploaded=self.convert_date(data.get("uploaded"))
        self.magnet_url=data['magnet'].get("magnet")
        self.magnet=False
        self.trusted=False
        self.vip=False
        self.size_str=data.get("size")
        self.size=self.calculate_size(data.get("size"))
        self.se=int(data.get("SE"))
        self.le=int(data.get("LE"))
        self.uled=data.get("ULed")
        self.define_icons(data['magnet'].get("icons"))
        self.generate_id(self.magnet_url)

    def generate_id(self,text:str):
        self.id_ = hashlib.md5(bytes(text,"utf-8")).hexdigest()

    def convert_date(self, date:str) -> int:
        try:
            date = datetime.strptime(date,"%m-%d %Y")
        except:
            date = datetime.strptime(date,"%m-%d %H:%M")
            date = date.replace(year=datetime.now().year)
        return date.strftime("%Y-%m-%d")

    def calculate_size(self, text:str) -> int:
        units = dict(
            KiB=1e3,
            MiB=1e6,
            GiB=1e9
        )
        key = text.split(" ")[-1]
        filesize = text.replace(key,"*"+str(units[key]))
        return int(eval(filesize))

    def insert(self):
        keys = list(self.__dict__.keys())
        keys = ",".join(keys)
        values = list(self.__dict__.values())
        fields = ",".join(["?" for _ in range(len(values))])
        cmd = f"INSERT or IGNORE INTO {TABLE}({keys}) VALUES({fields})"
        execute(cmd,DATABASE,values=values,mode="insert")

    def define_icons(self,icons):
        for icon in icons:
            if "magnet" in icon:
                self.magnet=True
            elif "trusted" in icon:
                self.trusted=True
            elif "vip" in icon:
                self.vip=True

if __name__ == "__main__":

    from pprint import pprint

    data = json.load(open("example.json",encoding="utf-8"))
    # pprint(data[0],sort_dicts=False)
    content = Content(data[0])
    pprint(content.__dict__,sort_dicts=False)

    # insert into database
    # content.insert()
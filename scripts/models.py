from pandas import DataFrame

class Model:
    def __init__(self, entry) -> None:
        self.id=entry[0]
        self.type=entry[1]
        self.name=entry[2]
        self.link=entry[3]
        self.uploaded=entry[4]
        self.magnet_url=entry[5]
        self.magnet=entry[6]
        self.trusted=entry[7]
        self.vip=entry[8]
        self.size_str=entry[9]
        self.size=entry[10]
        self.se=entry[11]
        self.le=entry[12]
        self.uled=entry[13]

    def __str__(self):
        attrs = [
            self.id,
            self.type,
            self.name,
            self.uploaded,
            self.size_str,
            "SE:"+str(self.se),
            "LE:"+str(self.le),
            "ULed:"+str(self.uled)
        ]
        return "|".join(attrs)

class Object:
    def __init__(self, entries) -> None:
        self.models = []
        for entry in entries:
            model = Model(entry)
            self.models.append(model)

    def sort_by(self,sort_value):
        new_models = [model.__dict__ for model in self.models]
        df = DataFrame(new_models)
        if sort_value != "uploaded":
            df = df.sort_values([sort_value,'uploaded'],ascending=False)
        else:
            df = df.sort_values(sort_value,ascending=False)
        self.models = [df.loc[i] for i in df.index]
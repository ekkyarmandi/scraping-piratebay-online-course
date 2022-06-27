from sqlite3 import connect
# from models import Object

def execute(cmd:str, database:str, values:str=[], mode=False) -> None:
    with connect(database) as con:
        cur = con.cursor()
        if mode == "insert":
            cur.execute(cmd,values)
            con.commit()
        elif mode == "query":
            cur.execute(cmd)
            return cur.fetchall()
        else:
            cur.execute(cmd)

def query(cmd:str,database:str) -> list:
    data = execute(cmd,database,mode="query")
    return data

def update():
    pass

def delete():
    pass

# if __name__ == "__main__":

#     cmd = "SELECT * FROM courses;"
#     data = query(cmd,"data/piratebay.db")
#     models = Object(data).models
#     items = [{'id':model.id,'uploaded':model.uploaded} for model in models]
#     items = sorted(items, key=lambda x: x['uploaded'],reverse=True)
#     new_models = []
#     for item in items:
#         new_model = next((model for model in models if model.id == item['id']), None)
#         if new_model:
#             new_models.append(new_model)

#     for model in new_models:
#         print(model.uploaded,model.id)
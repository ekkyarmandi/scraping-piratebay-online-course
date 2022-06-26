from sqlite3 import connect

def execute(cmd:str, database:str, values:str=[], mode=False) -> None:
    with connect(database) as con:
        cur = con.cursor()
        if mode == "insert":
            cur.execute(cmd,values)
            con.commit()
        else:
            cur.execute(cmd)

def update():
    pass

def delete():
    pass

from sql import execute

def create_table(database:str, table:str, fields:dict) -> None:
    fields = ",".join([key+" "+value for key,value in fields.items()])
    cmd = f"CREATE TABLE {table} ({fields})"
    try:
        execute(cmd,database)
        print(f"new table {table} has been created insde {database}")
    except:
        print(f"{table} has been exists")

def drop_table(database:str, table:str) -> None:
    cmd = f"DROP TABLE {table}"
    execute(cmd,database)
    print(f"{table} droped successfully from {database}")

if __name__ == "__main__":

    drop_table("data/piratebay.db","courses")

    fields = dict(
        id_="TEXT PRIMARY KEY",
        type="TEXT",
        name="TEXT",
        link="TEXT UNIQUE",
        uploaded="NUMERIC",
        magnet_url="TEXT",
        magnet="BOOL",
        vip="BOOL",
        trusted="BOOL",
        size_str="TEXT",
        size="INTEGER",
        se="INTEGER",
        le="INTEGER",
        uled="TEXT"
    )
    create_table("data/piratebay.db","courses",fields)

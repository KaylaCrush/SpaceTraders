import psycopg2
from settings import DATABASE, DB_USER

conn = psycopg2.connect(database = DATABASE, user = DB_USER)
cursor = conn.cursor()

def build_from_record(Class, record):
    if not record: return None
    obj = Class(**record)
    return obj

def build_from_records(Class, records):
   return [build_from_record(Class, record) for record in records]

def query(Class, condition):
    sql_str = f"SELECT * FROM {Class.__table__} IF {condition}"
    records = fetch(sql_str)
    return build_from_records(Class, records)
    
def find_all(Class):
    sql_str = f"SELECT * FROM {Class.__table__}"
    records = fetch(sql_str)
    return [build_from_record(Class, record) for record in records]

def fetch(sql_str):
    cursor.execute(sql_str)
    return cursor.fetchall()

def fetch_one(sql_str):
    cursor.execute(sql_str)
    return cursor.fetchone()

def commit(sql_str):
    cursor.execute(sql_str)
    conn.commit()

#takes an instantiated object, checks if it exists already. if it does, update it. otherwise, instantiate it
def save(obj):
    if exists(obj):
        update(obj)
    else:
        insert(obj)

#returns true if the primary keys of the object are already present in the database, otherwise false
def exists(obj):
    sql_str = f"SELECT * FROM {obj.__table__} WHERE {asl(p_key_equality(obj))}"
    if fetch_one(sql_str):
        return True
    return False
    
#takes an instantiated object, and creates a new database entry for it
def insert(obj):
    sql_str = f"""INSERT INTO {obj.__table__} ({csl(keys(obj))}) VALUES ({csl(stringify(values(obj)))});"""
    commit(sql_str)

#takes in an instantiated object, and updates the database with it
def update(obj):
    if update_key_equality(obj):
        sql_str = f"""UPDATE {obj.__table__} SET {csl(update_key_equality(obj))} WHERE {asl(p_key_equality(obj))}"""
        commit(sql_str)

# converts ints to str's, wraps str's in ' ' 's
def stringify(some_list):
    string_list = []
    for element in some_list:
        if type(element) == str:
            string_list.append(f"'{element}'")
        else:
            string_list.append(str(element))
    return string_list

#turns a list into a comma separated string
def csl(some_list):
    return ", ".join(some_list)

# turns a list into a string seperated by AND 's
def asl(some_list):
    return " AND ".join(some_list)

#builds an equality test for primary keys, ie "Key1='Value1' AND Key2='Value2'"
def p_key_equality(obj):
    return [f"{key}='{value}'" for key, value in zip(primary_keys(obj), primary_values(obj))]

def update_key_equality(obj):
    return [f"{key}='{value}'" for key, value in zip(keys(obj), values(obj)) if key not in primary_keys(obj)]

def values(obj):
    obj_attrs = obj.__dict__
    return [obj_attrs[attr] for attr in obj.columns if attr in obj_attrs.keys()]

def keys(obj):
    obj_attrs = obj.__dict__
    return [attr for attr in obj.columns if attr in obj_attrs.keys()]

def primary_keys(obj):
    return [attr for attr in obj.columns if attr in obj.primary_keys]

def primary_values(obj):
    obj_attrs = obj.__dict__
    return [obj_attrs[attr] for attr in obj.columns if attr in obj.primary_keys]


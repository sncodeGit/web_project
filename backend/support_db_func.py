import db_config as dbc
import pymysql
import logging

logger = logging.getLogger() 
logger.setLevel(logging.INFO)

def db_connect():
    try:
        conn = pymysql.connect(dbc.rds_host, user=dbc.name, passwd=dbc.password, db=dbc.db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance")
        logger.error(e)
        sys.exit()
    
    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
    return conn

def create_users_table():
    conn = db_connect()
    
    with conn.cursor() as cur:
        cur.execute(f'''create table web_user (
            id int not null auto_increment,
            login varchar(30) not null unique,
            password varchar(30) not null,
            email varchar(30) not null,
            primary key (id));''')
        conn.commit()
        
    return

def create_ssh_table():
    conn = db_connect()
    
    with conn.cursor() as cur:
        cur.execute(f'''create table ssh_servers (
            serv_id int not null auto_increment,
            user_id int not null,
            ssh_host varchar(30) not null,
            ssh_password varchar(30) not null,
            ssh_login varchar(30) not null,
            ssh_port smallint unsigned not null,
            primary key (serv_id),
            foreign key (user_id) references web_user (id));''')
        conn.commit()
        
    return

def drop_table(name):
    conn = db_connect()
    
    with conn.cursor() as cur:
        cur.execute('DROP TABLE ' + name + ';')
        conn.commit()
        
    return

def log_db_table(table_name):
    conn = db_connect()
    
    query = "select * from " + table_name + ";"
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()
        
    for row in cur:
        logger.info(row)

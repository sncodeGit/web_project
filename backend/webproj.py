import json
import sys
import logging
import pymysql

rds_host = "projectdb.cmaxlnftke4s.us-east-1.rds.amazonaws.com"
name = 'admin'
password = 'Fab}~fZWLf'
db_name = 'projectDB'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ret = {}
ret['statusCode'] = 404
ret['headers'] = {
    'Content-Type': 'text/html'
}
ret['body'] = f'''
        <html>
        <head>
        <meta charset="UTF-8">
        <title>Не найдено</title>
        </head>
        <body>
            Мы не нашли запрошенного вами документа :( <br>
            Пожалуйста, попробуйте вернуться назад
        </body>
        </html>
        '''

def lambda_handler(event, context):
    data = event['queryStringParameters']
    #create_users_table()
    
    if (len(data) == 4):
       registry(data)
    elif (len(data) == 2):
        auth(data)
    #data = {}
    #data['login'] = 'd'
    #data['password'] = 'd'
    #auth(data)
    
    return ret

def create_users_table():
    try:
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit()
    
    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
    
    with conn.cursor() as cur:
        cur.execute(f'''create table web_user (
            login varchar(30),
            password varchar(30),
            email varchar(30) not null,
            primary key (email));''')
        conn.commit()
    return

def registry(data):
    try:
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance")
        logger.error(e)
        sys.exit()
    
    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
    
    query = "insert into web_user values ('"+ str(data['login']) + "', '" + str(data['first_password']) + "', '" + str(data['email']) + "');"
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()
    
    body = f'''
            <html>
            <head>
            <meta charset="UTF-8">
            <title>Завершение регистрации</title>
            </head>
            <body>
                Благодарим за регистрацию!
            </body>
            </html>
            '''
    ret['body'] = body
    ret['statusCode'] = 200
    return
    
def auth(data):
    try:
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance")
        logger.error(e)
        sys.exit()
    
    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
    
    query = "select password from web_user where login='"+ str(data['login']) + "';"
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()
    
    real_pass = ''
    for row in cur:
        real_pass = row[0]
    
    if (real_pass == data['password']):
        ret['statusCode'] = 200
        body = f'''
            <html>
            <head>
            <meta charset="UTF-8">
            <title>Внутренняя часть сайта</title>
            </head>
            <body>
                Вы успешно авторизованы. Поздравляем!
            </body>
            </html>
            '''
    else:
        ret['statusCode'] = 401
        body = f'''
            <html>
            <head>
            <meta charset="UTF-8">
            <title>Неавторизованный запрос</title>
            </head>
            <body>
                Логин или пароль введены некорректно.<br>
                Также возможно, что вы ещё не зарегистрировались.<br>
                Тогда рекомендуем перейти на страницу регистрации и сделать это!
            </body>
            </html>
            '''
    ret['body'] = body
    return

import json
import sys
import logging
import pymysql
import support_db_func as dbfunc

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
    main(event)
    return ret
    
def main(event):
    data = event['queryStringParameters']
    
    if (len(data) == 4):
       registry(data)
    elif (len(data) == 2):
        auth(data)
        
    return

def registry(data):
    conn = dbfunc.db_connect()
    
    query = "insert into web_user values ('"+ str(data['login']) + "', '" + str(data['first_password']) + "', '" + str(data['email']) + "');"
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()
        
    ret['statusCode'] = 200
    ret['body'] = f'''
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
    return
    
def auth(data):
    conn = dbfunc.db_connect()
    
    query = "select password from web_user where login='"+ str(data['login']) + "';"
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()
    
    real_pass = ''
    for row in cur:
        real_pass = row[0]
    
    if (real_pass == data['password']):
        ret['statusCode'] = 200
        ret['body'] = f'''
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
        ret['body'] = f'''
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
    return

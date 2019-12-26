import json
import sys
import logging
import pymysql
import support_db_func as dbfunc
import config
import css

logger = logging.getLogger() 
logger.setLevel(logging.INFO)
ret = {}
html_param = {}

ret['statusCode'] = 404
ret['headers'] = {
    'Content-Type': 'text/html'
}

html_param['title'] = "Не найдено"
html_param['text'] = '''
        Мы не нашли запрошенного вами документа :( <br><br>
        Пожалуйста, попробуйте вернуться назад или перейдите на <a href="%s%s">главную</a>.
        ''' % (config.site_protocol, config.site_url)

def lambda_handler(event, context):
    main(event)
    html_formatting()
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
    html_param['title'] = "Завершение регистрации"
    html_param['text'] = '''
            Благодарим за регистрацию! <br><br>
            Переходите на страницу <a href="%s%s">авторизации</a>.
            ''' % (config.site_protocol, config.site_url)
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
        html_param['title'] = "Внутренняя часть сайта"
        html_param['text'] = '''
                Вы успешно авторизованы. Поздравляем!
            '''
    else:
        ret['statusCode'] = 401
        html_param['title'] = "Неавторизованный запрос"
        html_param['text'] = '''
                Логин или пароль введены некорректно
                или вы просто ещё не зарегистрированы.<br><br>
                Рекомендуем попробовать <a href="%s%s">авторизоваться снова</a>
                или перейти на <a href="%s%s/registry.html">страницу регистрации</a>.
            ''' % (config.site_protocol, config.site_url, config.site_protocol, config.site_url)
    return

def html_formatting():
    ret['body'] = f'''
        <html>
        <head>
        <meta charset="UTF-8">
        %s
        <title>%s</title>
        </head>
        <body>
            <div class="form">
                %s
            </div>
        </body>
        </html>
        ''' % (css.auth_css, html_param['title'], html_param['text'])

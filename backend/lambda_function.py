import json
import sys
import logging
import pymysql
import support_db_func as dbfunc
import config
import css
import paramiko

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
    
    if (len(data) == 5):
        add_serv_base(data)
    elif (len(data) == 4):
        registry(data)
    elif (len(data) == 2):
        if 'password' in data.keys():
            auth(data)
        elif 'mode' in data.keys():
            if (data['mode'] == 'add_serv'):
                add_serv_page(data['login'])
            elif (data['mode'] == 'vis_serv'):
                vis_serv(data['login'])
    elif (len(data) == 1):
        back_to_main(data['login'])
    
    return

def registry(data):
    conn = dbfunc.db_connect()
    
    query = f'''
    insert into web_user (login, password, email) values ('%s', '%s', '%s');
    ''' %  (str(data['login']), str(data['first_password']), str(data['email']))
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
        html_param['title'] = "Главная"
        html_param['text'] = f'''
            Добро пожаловать, %s<br><br>
            <form method="get" action="https://sd1i2zzpx2.execute-api.us-east-1.amazonaws.com/default/webproj">
                <input type="hidden" name="mode" value="add_serv">
                <input type="hidden" name="login" value="%s">
                <button class="form_button">Загрузить новый сервер</button>
            </form>
            <form method="get" action="https://sd1i2zzpx2.execute-api.us-east-1.amazonaws.com/default/webproj">
                <input type="hidden" name="mode" value="vis_serv">
                <input type="hidden" name="login" value="%s">
                <button class="form_button">Отобразить логи</button>
            </form>
            ''' % (data['login'], data['login'], data['login'])
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
        
def add_serv_page(login):
    html_param['title'] = "Добавление сервера"
    html_param['text'] = f'''
        Параметры SSH:<br><br><br>
        <form method="get" action="https://sd1i2zzpx2.execute-api.us-east-1.amazonaws.com/default/webproj">
        <div class="form_grup">
            <label class="form_label">Логин для ssh-доступа</label>
            <input class="form_input" type="text" name="ssh_login">
        </div>
        <div class="form_grup">
            <label class="form_label">Пароль для ssh-доступа</label>
            <input class="form_input" type="password" name="ssh_password">
        </div>
        <div class="form_grup">
            <label class="form_label">Хост</label>
            <input class="form_input" type="text" name="ssh_host">
        </div>
        <div class="form_grup">
            <label class="form_label">Порт</label>
            <input class="form_input" type="text" name="ssh_port">
        </div>
        <input type="hidden" name="login" value="%s">
        <button class="form_button">Добавить сервер</button>
        </form>
        ''' % login
        
def add_serv_base(data):
    data['ssh_port'] = int(data['ssh_port'])   
    
    conn = dbfunc.db_connect()
    
    user_id = dbfunc.get_user_id(data['login'])
        
    query = f'''
    insert into ssh_servers(user_id, ssh_host, ssh_password, ssh_login, ssh_port) 
    values(%d, '%s', '%s', '%s', %d)
    ''' %  (user_id, data['ssh_host'], data['ssh_password'], data['ssh_login'], data['ssh_port'])
    
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()
    
    ret['statusCode'] = 200
    html_param['title'] = "Успех!"
    html_param['text'] = '''
            Сервер успешно добавлен! <br><br>
            <form method="get" action="https://sd1i2zzpx2.execute-api.us-east-1.amazonaws.com/default/webproj">
            <input type="hidden" name="login" value="%s">
                <button class="form_button">Вернуться на главную</button>
            </form>
            ''' % data['login']
    return
        
def vis_serv(login):
    conn = dbfunc.db_connect()
    servers = ''
    
    user_id = dbfunc.get_user_id(login)
    
    query = f'''
    select ssh_host, ssh_login from ssh_servers where user_id='%s';
    ''' % user_id
    
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()
        
    button = f'''
    <form method="get" action="https://sd1i2zzpx2.execute-api.us-east-1.amazonaws.com/default/webproj">
                <button class="form_button2">Перейти</button>
            </form>
        '''
        
    for row in cur:
        servers = servers + row[0] + ' : ' + row[1]
        servers = servers + button
    
    html_param['title'] = "Список серверов"
    html_param['text'] = f'''
        <div class="center">
            Ваши серверы, %s: <br> <br>
            %s
        </div>
        ''' % (login, servers)
        
def back_to_main(login):
    ret['statusCode'] = 200
    html_param['title'] = "Главная"
    html_param['text'] = f'''
        С возвращением, %s<br><br>
        <form method="get" action="https://sd1i2zzpx2.execute-api.us-east-1.amazonaws.com/default/webproj">
            <input type="hidden" name="mode" value="add_serv">
            <input type="hidden" name="login" value="%s">
            <button class="form_button">Загрузить новый сервер</button>
        </form>
        <form method="get" action="https://sd1i2zzpx2.execute-api.us-east-1.amazonaws.com/default/webproj">
            <input type="hidden" name="mode" value="vis_serv">
            <input type="hidden" name="login" value="%s">
            <button class="form_button">Отобразить логи</button>
        </form>
        ''' % (login, login, login)
        
    return

<?php
	$server = 'projectdb.cmaxlnftke4s.us-east-1.rds.amazonaws.com';
	$user = 'admin';
	$password = 'Fab}~fZWLf';
	$dblink = mysqli_connect($server, $user, $password);
	if($dblink)
	echo 'Соединение установлено.';
	else
	die('Ошибка подключения к серверу баз данных.');
	$database = 'projectDB';
	$selected = mysqli_select_db($database, $dblink);
	if($selected)
	echo ' Подключение к базе данных прошло успешно.';
	else
	die(' База данных не найдена или отсутствует доступ.');
?>

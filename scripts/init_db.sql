CREATE DATABASE django_json_null_expr_repro;
CREATE USER 'django_json_null_expr_repro'@'localhost' identified with mysql_native_password by 'testing123';
GRANT ALL PRIVILEGES ON django_json_null_expr_repro.* TO 'django_json_null_expr_repro'@'localhost';

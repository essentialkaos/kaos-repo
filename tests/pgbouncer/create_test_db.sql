CREATE USER pgbtest WITH superuser login password 'Test1234!';
CREATE DATABASE pgbtest OWNER pgbtest;
\c pgbtest;
CREATE TABLE test(id integer, value text);
INSERT INTO test VALUES (1,'Test'),(2,'1234');

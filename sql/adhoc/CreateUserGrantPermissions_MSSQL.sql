-- Make SQL Server Authentication on. 
use master ;
CREATE LOGIN db_user WITH PASSWORD = N'db_pwd', CHECK_EXPIRATION=OFF, CHECK_POLICY=OFF;

create user db_user_test for login db_user;
exec sp_addrolemember db_owner,db_user_test;

-- Enable TCP - IP 
-- https://www.papercut.com/support/resources/manuals/ng-mf/common/topics/ext-db-specific-ms-sql-express.html

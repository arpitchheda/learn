-- Kill the query.
select
   c.owner,
   c.object_name,
   c.object_type,
   b.sid,
   b.serial#,
   b.status,
   b.osuser,
   b.machine,
   ' alter system kill session ''' || b.sid || ',' || b.serial# || ''' ; ' as kill_query
from
   v$locked_object a ,
   v$session b,
   dba_objects c
where
  b.sid = a.session_id
and
   a.object_id = c.object_id;
   
   
-- Add Temp Table Space 

alter tablespace users add datafile 'F:\APP\ORADATA\ORA\USERS02.DBF' size 2G autoextend on next 1024m maxsize unlimited;


-- Table Space Usage 
select 
   srt.tablespace, 
   srt.segfile#, 
   srt.segblk#, 
   srt.blocks, 
   a.sid, 
   a.serial#, 
   a.username, 
   a.osuser, 
   a.status 
from 
   v$session    a,
   v$sort_usage srt 
where 
   a.saddr = srt.session_addr 
order by 
   srt.tablespace, srt.segfile#, srt.segblk#, 
   srt.blocks;
   
--- Check the dependencies of View or Table
SELECT * from user_dependencies where referenced_name = upper(' < Table or View Name > ')

--- Check Space usage 
select inst_id, tablespace_name, total_blocks, used_blocks, free_blocks
from gv$sort_segment;

select TABLESPACE_NAME, BYTES_USED, BYTES_FREE from V$TEMP_SPACE_HEADER;

with da as (
 SELECT owner, segment_name, SUM(bytes)/1024/1024 size_mb
   FROM dba_extents
   group by rollup(owner, segment_name)
) select owner, segment_name, size_mb, round(size_mb/total_mb*100)
  from da 
    cross join (
      select size_mb as total_mb 
      from da t where owner is null and segment_name is null
    )
order by size_mb desc;

--- Oracle Admin UI 
-- https://docs.oracle.com/en/cloud/paas/database-dbaas-cloud/csdbi/access-em-database-express-12c.html
-- https://docs.oracle.com/cd/B16276_01/doc/server.102/b14196/em_manage003.htm
-- http://hostname:portnumber/em
-- http://localhost:8181/em/

select name, cdb, con_id from v$database;
select instance_name,status,con_id from v$instance; 
select dbms_xdb_config.getHttpsPort() from dual;
select dbms_xdb_config.getHttpPort() from dual;
-- Exec DBMS_XDB.SETHTTPPORT(8181);

-- Shrink Table 
alter table <TableName> enable row movement;
alter table <TableName> shrink space  ;

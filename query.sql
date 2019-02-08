--QUERIES IN PROGRESS. WILL WORK ON FRIDAY 8TH 4:00PM


--REPEATING FOR SOME REASON, NOT WORKING.NOT SELECTING ADJACENT--
SELECT DISTINCT A.TREASURE_ID, B.ZONE_ID
FROM s1889111.TREASURES A, s1889111.ZONE B, s1889111.ZONE C
WHERE SDO_CONTAINS(B.GEOM, A.GEOM) = 'TRUE'
AND B.ZONE_ID = '&ZONE';

--Select treasure from start point
SELECT DISTINCT B.TREASURE_ID
FROM s1889111.ZONE A, s1889111.TREASURES B, s1889111.STARTPOINT C
WHERE B.ZONE_ID = A.ZONE_ID
AND A.STARTPOINT_ID = '&START';

--Select start/end point from treasure 
SELECT DISTINCT A.STARTPOINT_ID
FROM s1889111.ZONE A, s1889111.TREASURES B, s1889111.STARTPOINT C
WHERE A.STARTPOINT_ID = B.ZONE_ID
AND B.TREASURE_ID = '&TREASURE'

--Distance spatial query needs to find out if it doubles...
SELECT SDO_GEOM.SDO_LENGTH(c.geom, m.diminfo
FROM s1889111.paths c, user_sdo_geom_metadata m 
WHERE m.table_name = 'PATHS' 
AND m.column_name = 'GEOM';

--Next node on network 

--Euclidean distance

--Intersect query


SELECT SDO_GEOM.RELATE(A.GEOM, 'ANYINTERACT', B.GEOM, 0.005)
FROM s1889111.ZONE A, s1889111.ZONE B
WHERE A.ZONE_ID = '1' AND B.ZONE_ID = '2';


'get_treasure_pts' : 'select c.penalty_id, t.x, t.y from s1889111.treasure c, table(sdo_util.getvertices(c.geom)) t'
'get_link_pts' : 'select c.path_id, t.x, t.y from s1889111.path c, table(sdo_util.getvertices(c.geom)) t'
'get_risk_pts' : 'select c.risk_id, t.x, t.y from s1889111.risks c, table(sdo_util.getvertices(c.geom)) t'

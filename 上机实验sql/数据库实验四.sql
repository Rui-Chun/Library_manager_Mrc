
--1)
INSERT INTO TPB16001775(Title,title_id,price)
    VALUES ('Digtal Image Processing','S7028',36.00);

--2)
DELETE
FROM TPB16001775
WHERE Title='Fortran程序设计';

--3)
DELETE
From TPB16001775
WHERE title_id LIKE  'H%';

--4）
UPDATE TPB16001775
SET price=price*0.9;

--5）
UPDATE TPB16001775
SET price=price-2
WHERE title_id LIKE 'D%';

--6）
UPDATE TPB16001775
SET title_id='S1125'
WHERE Title='计算机原理';

--7）
INSERT INTO SPB16001775(title_id, pages, storage, storenum)
    VALUES ('A21018',233,211,3);

UPDATE SPB16001775
SET pages=pages+10
WHERE title_id='A21018';

DELETE  FROM student..SPB16001775
WHERE pages<220;

--8）
SELECT *FROM pubs..cjdzb

create PROCEDURE PB16001775 @s_gr int ,@Gpa FLOAT OUTPUT ,@s_rank CHAR(2) OUTPUT
  AS
BEGIN
  if(@s_gr>100 OR @s_gr<0)
    return -1;
  ELSE
  SELECT @Gpa=jd,@s_rank=djcj FROM  pubs..cjdzb
  WHERE @s_gr<endfz AND @s_gr>=startfz;
  return 0;
END;


DECLARE @GPA FLOAT,@Rank CHAR(2);
EXECUTE PB16001775 95,@GPA OUTPUT ,@Rank OUTPUT ;
SELECT @GPA,@Rank;

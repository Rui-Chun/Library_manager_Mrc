--1
--1)
SELECT *FROM authors;
--2)
SELECT * FROM sales;

--2
--1)
SELECT title_id,title FROM titles;
--2)
SELECT title FROM titles
WHERE price<15 AND price>10;
--3)
SELECT title_id,title FROM titles
WHERE title LIKE 'T%';
--4)
SELECT au_lname,au_fname FROM authors
WHERE au_lname LIKE '%son%' OR au_fname LIKE '%son%';

--3
--1)
SELECT title,title_id,price FROM titles
WHERE title NOT LIKE 'T%' AND price>16;
--2)
SELECT title_id,ytd_sales FROM titles
WHERE ytd_sales IS NOT NULL ;
--3)
SELECT pub_name from publishers
WHERE country = 'USA' AND city IN ('Boston','Berkeley');

--4.
--1)
SELECT  COUNT(DISTINCT type) types  FROM titles
--)
SELECT  COUNT(DISTINCT price) pricetypes  FROM titles
--3)
SELECT  MAX(price) max_price  FROM titles
--4)
SELECT  SUM(ytd_sales) sales  FROM titles
--5)
SELECT  AVG(price) avg_price,MAX(price) max_price,MIN(price) min_price  FROM titles
--6)
SELECT  pub_id,SUM(ytd_sales) sales  FROM titles
GROUP BY pub_id
--7)
SELECT  COUNT(DISTINCT title) types  FROM titles
--8)
SELECT  COUNT(qty) qty,payterms  FROM sales
GROUP BY payterms
/*
8	Net 30
9	Net 60
4	ON invoice
*/

--5.
--1)
SELECT au_lname,au_fname,phone FROM authors
ORDER BY au_lname DESC ;
--2)
SELECT title,price FROM titles
ORDER BY price DESC ;
--3)
SELECT type,AVG(price) avg_price FROM titles
WHERE type LIKE '%cook%'
GROUP BY type;
--4)
SELECT COUNT(stor_id) storeNUm FROM stores
WHERE stor_address LIKE '%St.';
/*
3
 */


--6.
--1)
SELECT pub_name,title FROM titles,publishers
WHERE titles.pub_id=publishers.pub_id;
--2)
SELECT au_lname,au_fname,title FROM authors,titleauthor,titles
WHERE authors.au_id=titleauthor.au_id AND titleauthor.title_id=titles.title_id;
--3)
SELECT title,price,qty FROM sales,titles
WHERE titles.title_id=sales.title_id
AND qty>=ALL(
  SELECT qty FROM sales
) ;
--4)
SELECT stor_name,qty FROM sales,stores
WHERE sales.stor_id=stores.stor_id
AND sales.qty<=ALL(
  SELECT qty FROM sales
);
/*
Eric the Read Books	3
Barnum's	3
News & Brews	3
Doc-U-Mat: Quality Laundry and Books	3
Fricative Bookshop	3
Bookbeat	3
 */





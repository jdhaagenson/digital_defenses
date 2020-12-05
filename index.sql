SELECT ("VULN_ID", "PAGE_ID", data)
FROM vulnerabilities
WHERE (SELECT "PAGE_ID"
       FROM pages
       WHERE (SELECT "WEBSITE_ID"
              FROM websites
              WHERE "Name" = 'foo'));


-- OUTPUT:
--
-- "(1,1,""SQL injection response blah"")"
-- "(2,1,""XXE response"")"
-- "(3,1,""Stored XSS response"")"

-- Question of Performance:
-- My answer assumes that there are indexes of everything already created inside the database.
-- The queries become much more powerful and much quicker with the use of indexes.

Digital Defenses Coding Challenge
=================================



Question 1:
-----------
Given a table that holds websites (WEBSITE_ID, Name, URL), 
website pages (PAGE_ID, WEBSITE_ID, path), 
and website vulnerabilities (VULN_ID, PAGE_ID, data), 
find all of the vulnerabilities on website foo.com that pertain to the login page login.html. 
Your SQL should be performant for larger data sets.


- Table websites:
WEBSITE_ID, Name, URL
1. foo, http://foo.com
2. bar, http://foo.com

Table pages:
PAGE_ID, WEBSITE_ID, path
1, 1, /login.html
2, 1, /logout.html
3, 1, /admin.html
4, 2, /login.html
5, 2, /logout.html
6, 2, /admin.html

- Table vulnerabilities
VULN_ID, PAGE_ID, data
1, 1, SQL injection response blah
2, 1, XXE response
3, 1, Stored XSS response
4, 2, Session hijack
5, 4, XXE response
6, 6, Default credentials resposne

- Input:
All vulnerabilities for foo.com on login.html page
Output:
1, 1, SQL injection response blah
2, 1, XXE response
3, 1, Stored XSS response

How do we make this performant when we have 10 billion unique vulnerabilities across hundreds of thousands of websites?

Answer
------
Refer to `index.sql` file inside repository.

Question 2:
-----------
Write a function that takes two lists as input and produces one list as output. 
The function should have the signature 
`def apply_port_exclusions(include_ports, exclude_ports)`. 
The function should expect that the input lists will be a list of low-high pairs which are lists of length two. 
The function should return a minimized and ordered list of include port ranges that result after processing the exclude port ranges.

Include whatever tests and comments you normally provide for completed code.

Examples:
input:
include_ports: [[80, 80], [22, 23], [8000, 9000]]
exclude_ports: [[1024, 1024], [8080, 8080]]
output:
[[22, 23], [80, 80], [8000, 8079], [8081, 9000]]

input:
include_ports: [[8000, 9000], [80, 80], [22, 23]]
exclude_ports: [[1024, 1024], [8080, 8080]]
output:
[[22, 23], [80, 80], [8000, 8079], [8081, 9000]]

input:
include_ports: [[1,65535]]
exclude_ports: [[1000,2000], [500, 2500]]
output:
[[1, 499], [2501, 65535]]

input:
include_ports: [[1,1], [3, 65535], [2, 2]]
exclude_ports: [[1000, 2000], [500, 2500]]
output:
[[1, 499], [2501, 65535]]

input:
include_ports: []
exclude_ports: [[8080, 8080]]
output:
[]

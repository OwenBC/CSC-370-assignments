-- Retrieve by name and frequency and ordered by increasing name
-- those unique Badges that have been awarded at least five times,
-- but never before 2014 and never after 2019
-- 1.1 marks: <6 operators
-- 1.0 marks: <8 operators
-- 0.8 marks: correct answer

SELECT Name, COUNT(Name) AS Frequency
FROM Badge
WHERE Name NOT IN (
  SELECT Name
  FROM Badge
  WHERE DATE<'2014-01-01' OR DATE>'2019-12-31')
GROUP BY Name HAVING COUNT(Name)>4
ORDER BY Name;

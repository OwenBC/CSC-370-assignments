-- Retrieve the name and count of the Badge awarded
-- the second-most number of times
-- 1.1 marks: <10 operators
-- 1.0 marks: <12 operators
-- 0.9 marks: <15 operators
-- 0.8 marks: correct answer

SELECT *
FROM (
  SELECT Name, COUNT(Name) AS Frequency
  FROM Badge
  GROUP BY Name
  ORDER BY COUNT(Name) DESC
  LIMIT 2) AS TopTwo
ORDER BY Frequency
LIMIT 1;

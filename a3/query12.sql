-- Retrieve the display names of every user
-- who has received the Badge that has been
-- awarded the most times, excluding those badges
-- that have been awarded over ten thousand times.
-- Order the result in descending order.
-- 1.1 marks: <12 operators
-- 1.0 marks: <15 operators
-- 0.9 marks: <20 operators
-- 0.8 marks: correct answer

SELECT DisplayName
FROM User
INNER JOIN (
  SELECT DISTINCT UserId
  FROM Badge
  WHERE Name=(
    SELECT Name
    FROM Badge
    GROUP BY Name HAVING COUNT(Name)<10001
    ORDER BY COUNT(Name) DESC
    LIMIT 1)) AS UsersWithBadge
  ON User.Id=UserId
GROUP BY DisplayName
ORDER BY DisplayName DESC;

-- Retrieve the display name of all users who have
-- posted at least one post, ordered ascending
-- 1.1 marks: <5 operators
-- 1.0 marks: <7 operators
-- 0.8 marks: correct answer

SELECT DisplayName
FROM Post
  INNER JOIN User ON Post.OwnerUserId=User.Id
GROUP BY DisplayName
ORDER BY DisplayName;

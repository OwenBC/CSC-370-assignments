-- Retrieve the post id of all posts before July 2010 that
-- have never been linked to, ordered descending
-- 1.1 marks: <6 operators
-- 1.0 marks: <8 operators
-- 0.8 marks: correct answer

SELECT Id
FROM Post
WHERE CreationDate<'2010-07-01' AND Id NOT IN (
  SELECT RelatedPostId
  FROM Link)
ORDER BY Id DESC;

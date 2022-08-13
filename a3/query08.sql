-- Note: Aspects of this are *very* tricky
-- Retrieve the display name of all users who have
-- never posted a post that has been linked by another post
-- ordered ascending
-- 1.1 marks: <8 operators
-- 1.0 marks: <10 operators
-- 0.8 marks: correct answer

SELECT DisplayName
FROM User
WHERE Id NOT IN (
  SELECT Post.OwnerUserId
  FROM Link
    INNER JOIN Post ON (Link.RelatedPostId=Post.Id)
  WHERE OwnerUserId IS NOT NULL)
ORDER BY DisplayName;

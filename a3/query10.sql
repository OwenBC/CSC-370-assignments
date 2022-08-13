-- Retrieve the postid and display name of the user who posted it
-- for *all* posts that have linked to at least twenty other posts,
-- ordered by postId
-- 1.1 marks: <8 operators
-- 1.0 marks: <9 operators
-- 0.9 marks: <11 operators
-- 0.8 marks: correct answer

SELECT PostId, User.DisplayName
FROM (Link LEFT JOIN Post ON (Link.PostId=Post.Id))
  LEFT JOIN User ON (OwnerUserId=User.Id)
GROUP BY PostId HAVING COUNT(RelatedPostId)>19
ORDER BY PostId;

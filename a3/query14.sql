-- Retrieve the Post that has the highest
-- score, summed over itself and all its children
-- 1.1 marks: <8 operators
-- 1.0 marks: <10 operators
-- 0.9 marks: <12 operators
-- 0.8 marks: correct answer

SELECT Parent.Id, Parent.Score+SUM(Child.Score) AS FamilyScore
FROM Post as Child INNER JOIN Post as Parent 
  ON Parent.Id=Child.ParentId
GROUP BY Parent.Id
ORDER BY Parent.Score+SUM(Child.Score) DESC
LIMIT 1;

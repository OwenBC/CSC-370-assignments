-- Retrieve the five posts with the most votes
-- 1.1 marks: <5 operators
-- 1.0 marks: <6 operators
-- 0.8 marks: correct answer

SELECT PostId
FROM Vote
GROUP BY PostId
ORDER BY COUNT(PostId) DESC
LIMIT 5;

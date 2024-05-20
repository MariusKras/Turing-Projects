query_1 = """
SELECT 
    CASE 
        WHEN a1.AnswerText = 'Possibly' THEN 'Uncertain'
        WHEN a1.AnswerText = 'Don''t Know' THEN 'Uncertain'
        ELSE a1.AnswerText
    END AS Question_6,
    CASE 
        WHEN a83.AnswerText = 'Possibly' THEN 'Uncertain'
        WHEN a83.AnswerText = 'Don''t Know' THEN 'Uncertain'
        ELSE a83.AnswerText
    END AS Question_83,
    CASE 
        WHEN a14.AnswerText = 'Possibly' THEN 'Uncertain'
        WHEN a14.AnswerText = 'Don''t Know' THEN 'Uncertain'
        ELSE a14.AnswerText
    END AS Question_14,
    CASE 
        WHEN a19.AnswerText = 'Possibly' THEN 'Uncertain'
        WHEN a19.AnswerText = 'Don''t Know' THEN 'Uncertain'
        ELSE a19.AnswerText
    END AS Question_19,
    CASE 
        WHEN a18.AnswerText = 'Possibly' THEN 'Uncertain'
        WHEN a18.AnswerText = 'Don''t Know' THEN 'Uncertain'
        ELSE a18.AnswerText
    END AS Question_18 
FROM 
    (SELECT UserID, AnswerText, SurveyID 
     FROM answer 
     WHERE QuestionID = 6 AND SurveyID NOT IN (2014, 2016)) AS a1
INNER JOIN 
    (SELECT UserID, AnswerText 
     FROM answer 
     WHERE QuestionID = 83 AND SurveyID NOT IN (2014, 2016) 
     AND AnswerText NOT IN ("I've always been self-employed", "-1")) AS a83 ON a1.UserID = a83.UserID 
INNER JOIN 
    (SELECT UserID, AnswerText 
     FROM answer 
     WHERE QuestionID = 14 AND SurveyID NOT IN (2014, 2016)) AS a14 ON a1.UserID = a14.UserID 
INNER JOIN 
    (SELECT UserID, AnswerText 
     FROM answer 
     WHERE QuestionID = 19 AND SurveyID NOT IN (2014, 2016)) AS a19 ON a1.UserID = a19.UserID 
INNER JOIN 
    (SELECT UserID, AnswerText 
     FROM answer 
     WHERE QuestionID = 18 AND SurveyID NOT IN (2014, 2016)) AS a18 ON a1.UserID = a18.UserID;
"""

query_2 = """
SELECT 
    CASE 
        WHEN a1.AnswerText = 'Possibly' THEN 'Uncertain'
        WHEN a1.AnswerText = 'Don''t Know' THEN 'Uncertain'
        ELSE a1.AnswerText
    END AS Question_6,
    CASE 
        WHEN a83.AnswerText = 'Possibly' THEN 'Uncertain'
        WHEN a83.AnswerText = 'Don''t Know' THEN 'Uncertain'
        ELSE a83.AnswerText
    END AS Question_83,
    CASE 
        WHEN a14.AnswerText = 'Possibly' THEN 'Uncertain'
        WHEN a14.AnswerText = 'Don''t Know' THEN 'Uncertain'
        ELSE a14.AnswerText
    END AS Question_14,
    CASE 
        WHEN a19.AnswerText = 'Possibly' THEN 'Uncertain'
        WHEN a19.AnswerText = 'Don''t Know' THEN 'Uncertain'
        ELSE a19.AnswerText
    END AS Question_19,
    CASE 
        WHEN a18.AnswerText = 'Possibly' THEN 'Uncertain'
        WHEN a18.AnswerText = 'Don''t Know' THEN 'Uncertain'
        ELSE a18.AnswerText
    END AS Question_18,
    CASE 
        WHEN a33.AnswerText = 'Possibly' THEN 'Uncertain'
        WHEN a33.AnswerText = 'Don''t Know' THEN 'Uncertain'
        ELSE a33.AnswerText
    END AS Question_33
FROM 
    (SELECT UserID, AnswerText, SurveyID FROM answer WHERE QuestionID = 6 AND SurveyID NOT IN (2014, 2016)) AS a1
INNER JOIN 
    (SELECT UserID, AnswerText 
     FROM answer 
     WHERE QuestionID = 83 AND SurveyID NOT IN (2014, 2016) 
     AND AnswerText NOT IN ("I've always been self-employed", "-1")) AS a83 ON a1.UserID = a83.UserID 
INNER JOIN 
    (SELECT UserID, AnswerText FROM answer WHERE QuestionID = 14 AND SurveyID NOT IN (2014, 2016)) AS a14 ON a1.UserID = a14.UserID 
INNER JOIN 
    (SELECT UserID, AnswerText FROM answer WHERE QuestionID = 19 AND SurveyID NOT IN (2014, 2016)) AS a19 ON a1.UserID = a19.UserID 
INNER JOIN 
    (SELECT UserID, AnswerText FROM answer WHERE QuestionID = 18 AND SurveyID NOT IN (2014, 2016)) AS a18 ON a1.UserID = a18.UserID 
INNER JOIN 
    (SELECT UserID, AnswerText FROM answer WHERE QuestionID = 33 AND SurveyID NOT IN (2014, 2016)) AS a33 ON a1.UserID = a33.UserID
"""
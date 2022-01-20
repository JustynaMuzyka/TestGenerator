CREATE TABLE IF NOT EXISTS test (
	id_test INTEGER PRIMARY KEY AUTOINCREMENT,
	test_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS question (
	id_question INTEGER PRIMARY KEY AUTOINCREMENT,
	question_text TEXT NOT NULL,
	question_type TEXT NOT NULL,
	question_time INTEGER NOT NULL,
	
	id_test INTEGER,
	FOREIGN KEY(id_test) REFERENCES test(id_test)
);

CREATE TABLE IF NOT EXISTS answer (
	id_answer INTEGER PRIMARY KEY AUTOINCREMENT,
	answer_text TEXT NOT NULL,
	is_correct BOOLEAN NOT NULL,
	
	id_question INTEGER,
	FOREIGN KEY(id_question) REFERENCES question(id_question)
);

--select * from test;
--select * from answer;
--select * from question;

--drop table test;
--drop table answer;
--drop table question;

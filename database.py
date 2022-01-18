from sqlite3 import connect, Error

class Test():
    def __init__(self, testName):
        self.testName = testName

class Question():
    def __init__(self, questionId=None, questionText=None, questionType=None):
        self.questionId = questionId
        self.questionText = questionText
        self.questionType = questionType

class Answer():
    def __init__(self, answerText, isCorrect=False):
        self.answerText = answerText
        self.isCorrect = isCorrect

class TestsDatabase():
    def __init__(self):
        self.connection = None
        try:
            self.connection = connect('tests.db')
        except Error as e:
            print(e)

        with open('create_tests_database.sql', 'r') as inFile:
                createDatabaseScript = inFile.readlines()
                createDatabaseScript = ''.join(createDatabaseScript)

        self.cursor = self.connection.cursor()
        self.cursor.executescript(createDatabaseScript)

    def commit(self):
        self.connection.commit()

    def query_test_names(self):
        QUERY_TEST_NAMES = """
        SELECT test_name FROM test;
        """
        testNames = []

        self.cursor.execute(QUERY_TEST_NAMES)
        rows = self.cursor.fetchall()
        for row in rows:
            testNames.append(row[0])

        return testNames

    def insert_test(self, test):
        QUERY_TEST = """
        SELECT id_test FROM test WHERE test_name = (?);
        """
        
        INSERT_TEST = """
        INSERT INTO test (test_name) VALUES (?);
        """

        if test.testName in self.query_test_names():
            self.cursor.execute(QUERY_TEST, (test.testName,))
            rows = self.cursor.fetchall()
            return rows[0][0]
        
        self.cursor.execute(INSERT_TEST, (test.testName,))
        return self.cursor.lastrowid

    def insert_question(self, question, idTest):
        INSERT_QUESTION = """
        INSERT INTO question (question_text, question_type, id_test) VALUES (?, ?, ?);
        """

        self.cursor.execute(INSERT_QUESTION, (question.questionText, question.questionType, idTest))
        return self.cursor.lastrowid

    def insert_answer(self, answer, idQuestion):
        INSERT_ANSWER = """
        INSERT INTO answer (answer_text, is_correct, id_question) VALUES (?, ?, ?);
        """

        self.cursor.execute(INSERT_ANSWER, (answer.answerText, answer.isCorrect, idQuestion))
        return self.cursor.lastrowid

database = TestsDatabase()


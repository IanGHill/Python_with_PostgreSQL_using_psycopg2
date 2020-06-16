import psycopg2

class Student:
    def __init__(self, first_name, surname, age):
        self.id = 0
        self.first_name = first_name
        self.surname = surname
        self.age = age

    def insert_student(self):
        connection = psycopg2.connect(dbname="students_db", user="postgres", password="")
        cursor = connection.cursor()
        sql = """
            INSERT INTO students (first_name, surname, age)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        inserted_values = (self.first_name, self.surname, self.age)
        cursor.execute(sql, inserted_values)
        self.id = cursor.fetchone()[0]
        print(self.id)
        connection.commit()
        connection.close()

    def get_all_students():
        connection = psycopg2.connect(dbname="students_db", user="postgres", password="")
        cursor = connection.cursor()
        sql = "SELECT * FROM students;"
        cursor.execute(sql)
        rows = cursor.fetchall()
        connection.close()
        student_array = []
        for student_row in rows:
            fetched_student = Student(*student_row[1:])
            fetched_student.id = student_row[0]
            student_array.append(fetched_student)
        return student_array

    def student_search(surname):
        connection = psycopg2.connect(dbname="students_db", user="postgres", password="")
        cursor = connection.cursor()
        sql = "SELECT * FROM students WHERE surname= %s;"
        cursor.execute(sql, (surname,))
        student_row = cursor.fetchone()
        connection.close()
        if student_row is not None:
            fetched_student = Student(*student_row[1:])
            fetched_student.id = student_row[0]
            return fetched_student
        else:
            return student_row

    def update_student(id, new_age):
        connection = psycopg2.connect(dbname="students_db", user="postgres", password="")
        cursor = connection.cursor()
        sql = "UPDATE students SET age=%s WHERE id=%s"
        cursor.execute(sql, (new_age, id))
        connection.commit()
        connection.close()

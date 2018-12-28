import cx_Oracle

import PySimpleGUI as sg


def do_it(course):
    sg.ChangeLookAndFeel('DarkBlue')

    con = cx_Oracle.connect('system/earluser@127.0.0.1/xe')
    cur = con.cursor(scrollable=True)

    student_numbers = []

    def get_name(x):
        cur.execute("select * from EOM_STUDENTS")
        for row in cur:
            if x == (row[0]):
                return str(row[2] + " " + row[3])

    def get_rows(x):
        cur.execute("select * from EOM_STUDENTS")
        v_row = 0
        for row in cur:
            if row[1] == x:
                v_row += 1
                student_numbers.append(row[0])

        return v_row

    number_of_students = get_rows(course)

    for x in range(int(number_of_students) - 1):
        scrollable_column = scrollable_column + [[sg.Input(), sg.Input()]]

    layout = [[sg.Stretch(), sg.Text('Add Students', font=("Helvetica", 25)), sg.Stretch()],
              [sg.Text("                              First Name"), sg.Text("                                                      Last Name")],
              [sg.Column(scrollable_column, scrollable=True, size=(650, 500), vertical_scroll_only=True)],

              [sg.Stretch(), sg.ReadButton('Add Students', key='key_add_students', size=(20, 2),
                                           bind_return_key=True), sg.Text("Save occurs only once 'Add Student' button is pressed"), sg.Stretch() ]
              ]

    window = sg.Window('Add New Courses', default_element_size=(40, 2)).Layout(layout)

    while 'key_add_students':
        event, values = window.Read()
        if event is None or event == 'Exit':
            break

        for x in range(1, (int(number_of_students) + 1)):
            v_pos = x * 2 + 1
            student_first_name = values[v_pos]
            student_last_name = values[v_pos + 1]

            # Note: Correct class must be fetched, set outside for loop and inserted into SQL query below!
            cur.execute(
                """INSERT INTO EOM_STUDENTS (STUDENT_ID, CLASS, FIRST_NAME, LAST_NAME) VALUES (EOM_STUDENTS_S.nextval, 
                :course_code, :student_first_name, :student_last_name)""",
                course_code=course,
                student_first_name=student_first_name,
                student_last_name=student_last_name
            )

        con.commit()
        sg.Popup("Student names have been stored in database")
        break

    window.Close()

# author: Mike Dong, Early January
# version: 1.1

import PySimpleGUI as sg
import marking_first
import cx_Oracle
import sys
from input_checker import check_expectation
from input_checker import check_mark


def run_program(course, student_number):  # the function that runs everything
    marking_first.run_program(course, 'single')

    mark = [[],
            []]

    column = []  # part of the layout

    def get_name(x):
        cur.execute("select * from EOM_STUDENTS")
        for row in cur:
            if x == (row[0]):
                return str(row[2] + " " + row[3])

    con = cx_Oracle.connect('EOM/EOM@127.0.0.1/xe')  # connects to the database
    cur = con.cursor(scrollable=True)

    for x in range(int(marking_first.numberOfMark)):
        mark[0].append("")
        mark[1].append("")

    if not marking_first.quit_option:

        open_variable = True
        student_name = get_name(student_number)

        for z in range(int(marking_first.numberOfMark)):
            column.append(
                [sg.Text('Expectation  ', text_color='black', justification='left'),
                 sg.InputText(mark[0][z], size=(10, 1))], )
            column.append(
                [sg.Text('Mark            ', text_color='black', justification='left'),
                 sg.InputText('', size=(10, 1))], )
            column.append([sg.Text('_' * 100, size=(23, 1))], )

        mark = [[], []]

        layout = [[sg.Text('Mark entry - ' + student_name, size=(25, 1),
                           font=("Helvetica", 15), justification='center')],
                  [sg.Column(column, scrollable=True, size=(225, 300), vertical_scroll_only=True)],
                  [sg.Button('Finish Marking', key='key_finish')]]

        window = sg.Window('Mark ', auto_size_text=True, default_element_size=(40, 1)).Layout(layout)

        while open_variable:
            event, values = window.Read()
            saved = False
            do = False
            if event == 'key_finish':
                for x in range(int(marking_first.numberOfMark)):
                    tracker = x * 2
                    if values[tracker + 0] is not None and check_expectation(values[tracker + 0]):
                        if values[tracker + 1] is not None and check_mark(values[tracker + 1]):
                            mark[0].append(values[tracker + 0])
                            mark[1].append(values[tracker + 1])
                            do = True
                        else:
                            sg.Popup('Invalid mark' + values[tracker + 1])
                            do = False
                            break
                    else:
                        sg.Popup('Invalid expectation' + values[tracker + 0])
                        do = False
                        break

                if do:
                    for y in range(int(marking_first.numberOfMark)):
                        cur.execute("""
                            insert into EOM_MARKS (STUDENT_ID, COLOUR, TASK, EXPECTATION, MARK, COMMENTS, ANOMALY, DELETED_FLAG)
                            values (:studentID, :color, :nameOfMark, :task_variable, :mark_variable, :null_variable,
                            :No_variable, :No_variable_second)""",

                                task_variable=mark[0][y],
                                mark_variable=mark[1][y],
                                null_variable='',
                                studentID=student_number,
                                No_variable='N',
                                No_variable_second='N',
                                color=marking_first.color,
                                nameOfMark=marking_first.nameOfMark
                                    )

                        con.commit()
                        saved = True

                if saved:
                    break

            if values is None:
                sys.exit()

            window.Close()  # Don't forget to close your window!
        sg.Popup('You have just finished marking ' + marking_first.nameOfMark + ' for ' + student_name + "!")


#run_program('ICS4U-01/2018', 1)

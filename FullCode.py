from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import sys
import pymysql as MySQLdb
import datetime


MainUI,_ = loadUiType('Design.ui')

class Main(QMainWindow , MainUI):
    def __init__(self,parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Db_Connect()
        self.Handle_Buttons()
        self.Ui_Changes()
        self.Show_All_Categories()
        self.Show_All_Branches()
        self.Show_All_Authors()
        self.Show_All_Publishers()
        self.Show_All_Books()
        self.Show_All_Clients()
        self.Return_ToDay_work()
        self.Show_Employee()
        self.groupBox_7.hide()
        self.groupBox_8.hide()
        self.pushButton_38.hide()

    def Ui_Changes(self):
        # UI Changes zy mslan t5fy 7aga aw lma tdos 3la button mo3yan yft7 7aga
        #hna fe project da 3awzen n5fy el bars bta3t el tab widgets w n5ly el
        #buttons ely 3la el gnb de heya ely t- control da
        self.tabWidget.tabBar().setVisible(False)


    def Db_Connect(self):
        #connection between app and data base
        self.db = MySQLdb.connect(user='root', password='1997',host='localhost', port=3306, db='library')
        self.cur = self.db.cursor()


    def Handle_Buttons(self):
        #to handle any button in GUI
        self.pushButton.clicked.connect(self.Open_Daily_Movements_Tab)
        self.pushButton_2.clicked.connect(self.Open_Books_Tab)
        self.pushButton_3.clicked.connect(self.Open_Clients_Tab)
        self.pushButton_9.clicked.connect(self.Open_Settings_Tab)
        self.pushButton_7.clicked.connect(self.Handle_Today_Work)
        self.pushButton_19.clicked.connect(self.Add_New_Branch)
        self.pushButton_20.clicked.connect(self.Add_Publisher)
        self.pushButton_21.clicked.connect(self.Add_Author)
        self.pushButton_22.clicked.connect(self.Add_Category)
        self.pushButton_27.clicked.connect(self.Add_Employee)
        self.pushButton_10.clicked.connect(self.Add_New_Book)
        self.pushButton_15.clicked.connect(self.Add_New_Client)
        self.pushButton_12.clicked.connect(self.Edit_Book_Search)
        self.pushButton_11.clicked.connect(self.Edit_Book)
        self.pushButton_17.clicked.connect(self.Edit_Client_Search)
        self.pushButton_16.clicked.connect(self.Edit_Client)
        self.pushButton_13.clicked.connect(self.Delete_Book)
        self.pushButton_18.clicked.connect(self.Delete_Client)
        self.pushButton_8.clicked.connect(self.All_Books_Filter)
        self.pushButton_29.clicked.connect(self.Check_Employee)
        self.pushButton_28.clicked.connect(self.Edit_Employee_data)
        self.pushButton_30.clicked.connect(self.Add_Employee_Permissions)
        self.pushButton_40.clicked.connect(self.User_Login_Permissions)
        self.pushButton_41.clicked.connect(self.Open_Sign_Up_Tab)
        self.pushButton_35.clicked.connect(self.Open_Login_Tab)
        self.pushButton_36.clicked.connect(self.Retry_Sign_Up)
        self.pushButton_34.clicked.connect(self.Handle_Sign_Up)
        self.pushButton_38.clicked.connect(self.Logout)
        self.pushButton_14.clicked.connect(self.All_Clients_Filter)
        self.pushButton_23.clicked.connect(self.Cancel_Book_Fillter)
        self.pushButton_24.clicked.connect(self.Cancel_Client_Fillter)
        self.pushButton_31.clicked.connect(self.Show_All_Employees_Permissions)




    def Handle_Today_Work(self):
        client_ID =self.lineEdit.text()
        book_tile = self.lineEdit_38.text()
        type = self.comboBox.currentIndex()
        date = datetime.datetime.now()
        from_date = str(date.today())
        to = str(self.dateEdit_6.date())
        index = to.find('(')
        book_to = to[index+1:len(to)-1]
        book_to2 = ""
        for i in range(len(book_to)):
            if book_to[i] != ',':
                book_to2 = book_to2 + book_to[i]
            elif book_to[i] == ',':
                book_to2 = book_to2 + "-"
            else:
                book_to2 = book_to2
        if type == 0 :
            to = book_to2
        else:
            to = '-----------'

        if client_ID != '' and book_tile != '':
            try:
                self.cur.execute('''SELECT name FROM clients WHERE national_id = %s''',[(client_ID)])
                check = self.cur.fetchone()
                client_name= check[0]
                self.cur.execute('''
                INSERT INTO daily_movements (book_title , client_id , type , date , book_from , book_to ,
                client_name)
                VALUES (%s , %s , %s , %s , %s , %s , %s ) ''',
                                 (book_tile, client_ID, type, date, from_date, to, client_name))
            except:
                QMessageBox.information(self, "Warning", "Invalid Client National ID !")

            self.db.commit()
            self.Return_ToDay_work()
        else:
            QMessageBox.information(self, "Warning", "Please enter client ID and Book title")





    def Return_ToDay_work(self):
        #an actual client must be registered in the system
        try:
            self.cur.execute(''' SELECT book_title ,client_name, client_id, type  ,book_from ,book_to
                 FROM daily_movements''')
            data = self.cur.fetchall()
            self.tableWidget.setRowCount(0)
            self.tableWidget.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    if column == 3:
                        if item == 0:
                            self.tableWidget.setItem(row, column, QTableWidgetItem('Rent'))
                        else:
                            self.tableWidget.setItem(row, column, QTableWidgetItem('Retrieve'))

                    else:
                        self.tableWidget.setItem(row , column ,QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.tableWidget.rowCount()  # el satren dol 3lashn yzwd satr w ykrr nfs ely 3mlo fo2
                self.tableWidget.insertRow(row_position)
        except:
            print("daily_movements table is emtpy in DB !")


    def Show_All_Books(self):
        self.pushButton_23.hide()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)

        self.cur.execute('''SELECT code , title , category_id ,author_id, price FROM books''')
        data = self.cur.fetchall()
        for row , form in enumerate(data):
            for column , item in enumerate(form):
                if column == 2:
                    sql = '''SELECT category_name FROM category WHERE id = %s'''
                    self.cur.execute(sql, [(item)])
                    category_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(category_name[0])))
                elif column == 3 :
                    sql = '''SELECT name FROM author WHERE id = %s'''
                    self.cur.execute(sql, [(item)])
                    author_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(author_name[0])))

                else:
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)


    def All_Books_Filter(self):
        book_data = self.lineEdit_2.text()
        combo = self.comboBox_13.currentIndex()
        if book_data != '' :
            try:

                if combo == 0 :
                    self.cur.execute('''SELECT code ,title,category_id,author_id,price FROM books WHERE title = %s'''
                                     , [(book_data)])
                elif combo == 1 :
                    self.cur.execute('''SELECT code,title,category_id,author_id,price FROM books WHERE code = %s'''
                                     , [(book_data)])

                data = self.cur.fetchall()
                if len(data[0])>1:
                    self.tableWidget_2.setRowCount(0)
                    self.tableWidget_2.insertRow(0)
                    for row, form in enumerate(data):
                        for column, item in enumerate(form):
                            if column == 2 :
                                self.cur.execute('''SELECT category_name FROM category WHERE id =%s''',[(item)])
                                category_name = self.cur.fetchone()

                                self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(category_name[0])))
                            elif column == 3 :
                                sql = '''SELECT name FROM author WHERE id = %s'''
                                self.cur.execute(sql, [(item)])
                                author_name = self.cur.fetchone()
                                self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(author_name[0])))
                            else :
                                self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))

                            column += 1
                        row_position = self.tableWidget_2.rowCount()
                        self.tableWidget_2.insertRow(row_position)
                    self.pushButton_23.show()
                else :
                    QMessageBox.information(self, "Warning", "This book is not exist !")

            except:
                QMessageBox.information(self, "Warning", "This book is not exist !")

        else:

            QMessageBox.information(self, "Warning", "Please enter book information to search")

    def Cancel_Book_Fillter(self):
        self.pushButton_23.show()
        self.Show_All_Books()


    def Cancel_Client_Fillter(self):
        self.pushButton_24.show()
        self.Show_All_Clients()








    def Add_New_Book(self):
        book_title = self.lineEdit_3.text()
        category = self.comboBox_3.currentText()
        description = self.textEdit.toPlainText()
        price = self.lineEdit_4.text()
        code = self.lineEdit_5.text()
        publisher = self.comboBox_5.currentText()
        author = self.comboBox_4.currentText()
        status = self.comboBox_6.currentIndex()
        part_order = self.lineEdit_6.text()
        date = datetime.datetime.now()
        if book_title != '' :
            try:
                self.cur.execute('''SELECT id FROM category WHERE category_name =%s''',[(category)])
                data1 = self.cur.fetchone()
                category_id = int(data1[0])

                self.cur.execute('''SELECT id FROM author WHERE name =%s''', [(author)])
                data2 = self.cur.fetchone()
                author_id = int(data2[0])

                self.cur.execute('''SELECT id FROM publisher WHERE name =%s''', [(publisher)])
                data3 = self.cur.fetchone()
                publisher_id = int(data3[0])

                self.cur.execute('''
                INSERT INTO books( title ,description ,category_id ,code ,part_order ,price ,author_id ,publisher_id
                ,status ,date )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                ''' ,(book_title,description,category_id,code,part_order,price,author_id,publisher_id,status,date))
                self.statusBar().showMessage('The book has been added successfully',5000)
            except:
                QMessageBox.information(self, "Warning", "This title or code is already exist !")

            self.db.commit()
            self.Show_All_Books()
        else:
            QMessageBox.information(self, "Warning", "please enter book information")

    def Edit_Book_Search(self):
        book_code = self.lineEdit_7.text()
        if book_code != '' :
            try:
                sql = (''' SELECT * FROM books WHERE code = %s ''')
                self.cur.execute(sql,[(book_code)])

                data = self.cur.fetchone()
                author_id = data[11]
                publisher_id = data[10]
                category_id = data[9]

                self.cur.execute('''SELECT category_name FROM category WHERE id = %s''', [(category_id)])
                data1 = self.cur.fetchone()
                category = data1[0]

                self.cur.execute('''SELECT name FROM publisher WHERE id = %s''', [(publisher_id)])
                data2 = self.cur.fetchone()
                publisher = data2[0]

                self.cur.execute('''SELECT name FROM author WHERE id = %s''', [(author_id)])
                data3 = self.cur.fetchone()
                author = data3[0]

                self.lineEdit_8.setText(data[1])
                self.lineEdit_26.setText(category)
                self.lineEdit_30.setText(author)
                self.lineEdit_31.setText(publisher)
                self.lineEdit_10.setText(str(data[5]))
                self.comboBox_8.setCurrentIndex(int(data[7]))
                self.lineEdit_9.setText(str(data[4]))
                self.textEdit_2.setPlainText(data[2])




            except:
                QMessageBox.information(self, "Warning", "This code is not exist !")


        else:
            QMessageBox.information(self, "Warning", "Please enter book code")

    def Edit_Book(self):
        book_title = self.lineEdit_8.text()
        category = self.lineEdit_26.text()
        description = self.textEdit_2.toPlainText()
        price = self.lineEdit_10.text()
        code = self.lineEdit_7.text()
        publisher = self.lineEdit_31.text()
        author = self.lineEdit_30.text()
        status = self.comboBox_8.currentIndex()
        part_order = self.lineEdit_9.text()
        date = datetime.datetime.now()
        if book_title !='' and code !='' :
            try :
                self.cur.execute('''SELECT id FROM category WHERE category_name =%s''', [(category)])
                data1 = self.cur.fetchone()
                category_id = int(data1[0])

                self.cur.execute('''SELECT id FROM author WHERE name =%s''', [(author)])
                data2 = self.cur.fetchone()
                author_id = int(data2[0])

                self.cur.execute('''SELECT id FROM publisher WHERE name =%s''', [(publisher)])
                data3 = self.cur.fetchone()
                publisher_id = int(data3[0])

                self.cur.execute(''' UPDATE books SET title = %s , description = %s ,code = %s, part_order =%s
                 ,price =%s ,status=%s , category_id=%s ,publisher_id=%s ,author_id=%s ,date=%s WHERE code =%s''',
                             (book_title, description, code, part_order, price, status, category_id,
                              publisher_id, author_id,date, code))
            except:
                QMessageBox.information(self, "Warning", "Invalid informations!")



            self.statusBar().showMessage('Book informations have been updated sccessfully',5000)
            self.db.commit()

            self.Show_All_Books()

        else:
            QMessageBox.information(self, "Warning", "Please enter book code and book title")





    def Delete_Book(self):
        book_code = self.lineEdit_7.text()
        if book_code != '' :
            try:
                delete_message =  QMessageBox.question(self, 'Warning',
                                            "Are you sure you want to remove this book?!",
                        QMessageBox.Yes , QMessageBox.No)

                if delete_message == QMessageBox.Yes:
                    self.cur.execute('''DELETE FROM books WHERE code = %s''',[(book_code)])
                    self.statusBar().showMessage('The book has been removed successfully!',5000)
                    self.db.commit()
                    self.Show_All_Books()

                    self.lineEdit_8.clear()
                    self.lineEdit_26.clear()
                    self.textEdit_2.clear()
                    self.lineEdit_10.clear()
                    self.lineEdit_7.clear()
                    self.lineEdit_31.clear()
                    self.lineEdit_30.clear()
                    self.comboBox_8.setCurrentIndex(0)
                    self.lineEdit_9.clear()



            except:
                QMessageBox.information(self, "Warning", "Failed to remove this book!")

        else :
            QMessageBox.information(self, "Warning", "Please enter book code to remove")




    def Show_All_Clients(self):
        self.pushButton_24.hide()
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.insertRow(0)

        self.cur.execute('''SELECT name , mail , phone ,national_id, date FROM clients''')
        data = self.cur.fetchall()
        for row, form in enumerate(data): # row = iteration .... form = data ely b- loop 3leha
            for column, item in enumerate(form):
                self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(row_position)


    def Add_New_Client(self):
        client_name = self.lineEdit_12.text()
        client_mail = self.lineEdit_13.text()
        client_phone = self.lineEdit_14.text()
        client_national_id = self.lineEdit_15.text()
        date = datetime.datetime.now()
        if client_name != '' and client_national_id != '' :
            try :

                self.cur.execute('''
                INSERT INTO clients (name , mail, phone,date,national_id)
                VALUES (%s ,%s ,%s ,%s, %s)''',(client_name,client_mail,client_phone,date,client_national_id))
                self.statusBar().showMessage('The client has been added successfully', 5000)
                self.db.commit()
                self.Show_All_Clients()

            except:
                QMessageBox.information(self, "Warning", "This national ID is already exist !")


        else:
            QMessageBox.information(self, "Warning", "Please enter client information completely ")

    def Edit_Client_Search(self):
        client_data = self.lineEdit_20.text()
        if client_data != '' :
            try:

                if self.comboBox_11.currentIndex() == 0 :
                    sql = (''' SELECT * FROM clients WHERE name = %s ''')
                    self.cur.execute(sql, [(client_data)])
                    data = self.cur.fetchone()

                elif self.comboBox_11.currentIndex() == 1 :
                    sql = (''' SELECT * FROM clients WHERE mail = %s ''')
                    self.cur.execute(sql, [(client_data)])
                    data = self.cur.fetchone()

                elif self.comboBox_11.currentIndex() == 2 :
                    sql = (''' SELECT * FROM clients WHERE phone = %s ''')
                    self.cur.execute(sql, [(client_data)])
                    data = self.cur.fetchone()

                elif self.comboBox_11.currentIndex() == 3 :
                    sql = (''' SELECT * FROM clients WHERE national_id = %s ''')
                    self.cur.execute(sql, [(client_data)])
                    data = self.cur.fetchone()

                self.lineEdit_17.setText(str(data[1]))
                self.lineEdit_16.setText(str(data[2]))
                self.lineEdit_19.setText(str(data[3]))
                self.lineEdit_18.setText(str(data[5]))
            except:
                QMessageBox.information(self, "Warning", "Invalid input information !")

        else:
            QMessageBox.information(self, "Warning", "Please enter client informations !")

    def Edit_Client(self):
        client_name = self.lineEdit_17.text()
        client_mail = self.lineEdit_16.text()
        client_phone = self.lineEdit_19.text()
        client_national_id = self.lineEdit_18.text()
        parent = self.lineEdit_20.text()
        combo = self.comboBox_11.currentIndex()

        if client_name != '' and client_national_id != '' :
            try :

                if combo == 0 :
                    self.cur.execute(''' UPDATE clients SET name = %s ,mail = %s ,phone = %s , national_id = %s
                     WHERE name = %s''',
                                 (client_name ,client_mail ,client_phone ,client_national_id,parent))
                    self.db.commit()

                elif combo == 1:
                    self.cur.execute(''' UPDATE clients SET name = %s ,mail = %s ,phone = %s , national_id = %s
                           WHERE mail = %s''',
                                     (client_name, client_mail, client_phone, client_national_id, parent))
                    self.db.commit()

                elif combo == 2:
                    self.cur.execute(''' UPDATE clients SET name = %s ,mail = %s ,phone = %s , national_id = %s
                           WHERE phone = %s''',
                                     (client_name, client_mail, client_phone, client_national_id, parent))
                    self.db.commit()

                elif combo == 3:
                    self.cur.execute(''' UPDATE clients SET name = %s ,mail = %s ,phone = %s , national_id = %s
                           WHERE national_id = %s''',
                                     (client_name, client_mail, client_phone, client_national_id, parent))
                    self.db.commit()
                self.statusBar().showMessage('Client information have been updated successfully!', 5000)
                self.Show_All_Clients()

            except:
                QMessageBox.information(self, "Warning", "This national ID is already exist !")

        else:
            QMessageBox.information(self, "Warning", "Please enter client informations completely")




    def Delete_Client(self):
        client_data = self.lineEdit_20.text()
        data_type = self.comboBox_11.currentIndex()
        if client_data != '' :
            delete_message = QMessageBox.question(self,
                 'Delete',"Are you sure you want to revome this client?!", QMessageBox.Yes, QMessageBox.No)

            if delete_message == QMessageBox.Yes :
                try:
                    if data_type == 0 :
                        self.cur.execute( ''' DELETE FROM clients WHERE name = %s''',[(client_data)])

                    if data_type == 1:
                        self.cur.execute(''' DELETE FROM clients WHERE mail = %s''', [(client_data)])

                    if data_type == 2:
                        self.cur.execute(''' DELETE FROM clients WHERE phone = %s''', [(client_data)])

                    if data_type == 3:
                        self.cur.execute(''' DELETE FROM clients WHERE national_id = %s''', [(client_data)])

                    self.db.commit()
                    self.statusBar().showMessage('The client has been removed successfully!',5000)
                    self.lineEdit_17.clear()
                    self.lineEdit_16.clear()
                    self.lineEdit_19.clear()
                    self.lineEdit_18.clear()
                    self.lineEdit_20.clear()
                    self.comboBox_11.setCurrentIndex(0)
                    self.Show_All_Clients()

                except :
                    QMessageBox.information(self, "success", "This client does not exist !")

        else:
            QMessageBox.information(self, "success", "Please enter client informations to remove")





    def All_Clients_Filter(self):
        client_data = self.lineEdit_11.text()
        combo = self.comboBox_12.currentIndex()
        if client_data != '' :
            try :

                if combo == 0 :
                    self.cur.execute('''SELECT name , mail , phone , national_id ,date FROM clients WHERE name = %s'''
                                     , [(client_data)])

                elif combo == 1 :
                    self.cur.execute('''SELECT name , mail , phone , national_id ,date FROM clients WHERE mail = %s'''
                                     , [(client_data)])

                elif combo == 2 :
                    self.cur.execute('''SELECT name , mail , phone , national_id ,date FROM clients WHERE phone = %s'''
                                     , [(client_data)])

                elif combo == 3 :
                    self.cur.execute('''SELECT name , mail ,phone, national_id ,
                    date FROM clients WHERE national_id = %s'''  , [(client_data)])

                data = self.cur.fetchall()
                if len(data[0]) > 1 :
                    self.tableWidget_3.setRowCount(0)
                    self.tableWidget_3.insertRow(0)
                    for row, form in enumerate(data):
                        for column, item in enumerate(form):
                            self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))

                            column += 1
                        row_position = self.tableWidget_3.rowCount()
                        self.tableWidget_3.insertRow(row_position)
                    self.pushButton_24.show()
                else:
                    QMessageBox.information(self, "Warning", "This client does not exist !")


            except :

                QMessageBox.information(self, "Warning", "This client does not exist !")


        else:
            QMessageBox.information(self, "Warning", "Please enter client information to search")




    ###############################################
    ##Settings
    def Add_New_Branch(self):
        branch_name = self.lineEdit_21.text()
        branch_code =self.lineEdit_22.text()
        branch_location = self.lineEdit_23.text()
        if branch_name != '' :
            try:
                self.cur.execute("""
                    INSERT INTO branch(name , code , location)
                    VALUES (%s , %s , %s)
                    """,(branch_name ,branch_code , branch_location))
                self.statusBar().showMessage('The branch has been add successfully', 5000)
            except:
                QMessageBox.information(self, "Warning", "This branch is already exist !")

        else :
            QMessageBox.information(self, "Warning", "Please enter branch name")



        self.db.commit()
        self.Show_All_Branches()

    def Add_Category(self):
        category_name = self.lineEdit_29.text()
        if category_name != '' :
            try:
                self.cur.execute('''
                INSERT INTO category(category_name)
                VALUES (%s) ''',(category_name))
                self.statusBar().showMessage('The category has been added successfully', 5000)

            except:
                QMessageBox.information(self, "Warning", "This category is already exist !")

            self.db.commit()
            self.Show_All_Categories()
        else :
            QMessageBox.information(self, "Warning", "Please enter category name")

    def Show_All_Categories(self):
        self.comboBox_3.clear()
        self.comboBox_3.addItem("    ")
        self.cur.execute('''SELECT category_name FROM category  ''')
        categories = self.cur.fetchall()
        for category in categories:
            self.comboBox_3.addItem(str(category[0]))



    def Show_All_Branches(self):
        self.comboBox_21.clear()
        self.comboBox_22.clear()
        self.comboBox_21.addItem("      ")
        self.comboBox_22.addItem("      ")
        self.cur.execute(''' SELECT name FROM branch ''')
        branches = self.cur.fetchall()
        for branch in branches:
            self.comboBox_21.addItem(branch[0])
            self.comboBox_22.addItem(branch[0])

    def Show_All_Publishers(self):
        self.comboBox_5.clear()
        self.comboBox_5.addItem("     ")

        self.cur.execute(''' SELECT name FROM publisher''')
        publishers = self.cur.fetchall() # it returns tuple of tuples ((dar el nashr,),(Tibaaa,))
        for publisher in publishers:
            self.comboBox_5.addItem(str(publisher[0]))



    def Show_All_Authors(self):
        self.comboBox_4.clear()
        self.comboBox_4.addItem("     ")

        self.cur.execute(''' SELECT name FROM author''')
        authors = self.cur.fetchall()

        for author in authors:
            self.comboBox_4.addItem(author[0])

    def Show_Employee(self):
        self.comboBox_19.clear()
        self.comboBox_19.addItem("   ")
        self.cur.execute('''SELECT name FROM employee''')
        employees = self.cur.fetchall()
        for employee in employees:
            self.comboBox_19.addItem(employee[0])



    def Add_Publisher(self):
        publisher_name = self.lineEdit_24.text()
        publisher_location = self.lineEdit_25.text()
        if publisher_name != '' :
            try:
                self.cur.execute('''
                INSERT INTO publisher(name ,location)
                VALUES (%s ,%s)
                ''' , (publisher_name , publisher_location))
                self.statusBar().showMessage('The publisher has been added successfully', 5000)

            except:
                QMessageBox.information(self, "Warning", "This publisher is already exist !")

            self.db.commit()
            self.Show_All_Publishers()

        else:
            QMessageBox.information(self, "Warning", "Please enter publisher name")


    def Add_Author(self):
        author_name = self.lineEdit_27.text()
        author_location = self.lineEdit_28.text()
        if author_name != '' :
            try :
                self.cur.execute('''
                INSERT INTO author(name , location)
                VALUES (%s , %s)''' ,(author_name , author_location))
                self.statusBar().showMessage('The Author has been added successfully', 5000)

            except:
                QMessageBox.information(self, "Warning", "This author is already exist !")

        else:
            QMessageBox.information(self, "Warning", "Please enter author name!")

        self.db.commit()
        self.Show_All_Authors()



    ##############################################
    def Add_Employee(self):
        employee_name = self.lineEdit_32.text()
        employee_mail = self.lineEdit_34.text()
        employee_phone = self.lineEdit_35.text()
        employee_branch = self.comboBox_21.currentIndex()
        employee_national_id = self.lineEdit_49.text()
        employee_periority =self.lineEdit_44.text()
        password = self.lineEdit_33.text()
        password_2 = self.lineEdit_36.text()
        date = datetime.datetime.now()
        if  employee_name != '' and employee_national_id != '':

            if password == password_2  :
                try:
                    self.cur.execute('''
                        INSERT INTO employee (name ,mail ,phone , date, national_id ,periority ,password ,branch)
                        VALUES ( %s, %s, %s, %s, %s, %s ,%s ,%s) '''
                         ,(employee_name,employee_mail,employee_phone,date,employee_national_id
                           ,employee_periority,password,employee_branch))
                    self.db.commit()
                    self.cur.execute('''INSERT INTO employee_permissions (employee_name,books_tab,clients_tab,
                    settings_tab, add_book,edit_book,delete_book,add_client,edit_client,delete_client,
                        add_branch,add_publisher,add_author,add_category,add_employee,edit_employee,is_admin)
                        VALUES ( %s ,%s , %s , %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s)'''
                                     , (employee_name, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
                    self.db.commit()
                    self.lineEdit_32.clear()
                    self.lineEdit_34.clear()
                    self.lineEdit_35.clear()
                    self.lineEdit_49.clear()
                    self.lineEdit_44.clear()
                    self.lineEdit_33.clear()
                    self.lineEdit_36.clear()
                    self.comboBox_21.setCurrentIndex(0)

                    self.statusBar().showMessage('Done Successfully',5000)

                except:
                    QMessageBox.information(self, "Warning", "This National ID is already exist")




            else:
                 QMessageBox.information(self, "Warning", "Password and confirm password does not match!")


            self.Show_Employee()
        else:
            QMessageBox.information(self, "Warning", "Please enter employee information ")

    def Check_Employee(self):
        self.groupBox_9.setEnabled(False)
        self.lineEdit_37.clear()
        self.lineEdit_40.clear()
        self.comboBox_22.setCurrentIndex(0)
        self.lineEdit_41.clear()
        self.lineEdit_50.clear()
        self.lineEdit_39.clear()
        self.lineEdit_51.clear()
        employee_name = self.lineEdit_42.text()
        employee_password = self.lineEdit_43.text()
        if employee_name != '' and employee_password != '' :

            self.cur.execute(''' SELECT * FROM employee''')
            data = self.cur.fetchall()
            for row in data :
                if row[1] == employee_name and row[7] == employee_password :
                    self.groupBox_9.setEnabled(True)
                    self.lineEdit_37.setText(row[2])
                    self.lineEdit_39.setText(row[3])
                    self.lineEdit_40.setText(str(row[5]))
                    self.comboBox_22.setCurrentIndex(int(row[8]))
                    self.lineEdit_41.setText(str(row[6]))
                    self.lineEdit_50.setText(str(row[7]))
                    self.lineEdit_51.setText(str(row[7]))

            if    self.groupBox_9.isEnabled() != 1 :
                QMessageBox.information(self, "Warning", "Invalid password or username !")

        else:
            QMessageBox.information(self, "Warning", "Please enter Username and password")



    def Edit_Employee_data(self):
        employee_name = self.lineEdit_42.text()
        employee_password = self.lineEdit_50.text()
        employee_mail = self.lineEdit_37.text()
        employee_phone = self.lineEdit_39.text()
        employee_id =self.lineEdit_40.text()
        branch = self.comboBox_22.currentIndex()
        periority = self.lineEdit_41.text()
        employee_password2 = self.lineEdit_51.text()
        if employee_name != '' and employee_id != '' :
            if employee_password == employee_password2 :
                print(employee_name,employee_password,employye_phone,employee_id,employee_mail,employee_password2
                      ,branch,periority)
                try:

                    self.cur.execute('''UPDATE employee SET mail =%s , phone =%s ,national_id =%s ,periority =%s
                    ,password =%s ,branch =%s WHERE name =%s ''',(employee_mail,employee_phone,employee_id,
                                                                  periority,employee_password,employee_name))
                    self.db.commit()
                    self.lineEdit_42.clear()
                    self.lineEdit_43.clear()
                    self.lineEdit_37.clear()
                    self.lineEdit_40.clear()
                    self.comboBox_22.setCurrentIndex(0)
                    self.lineEdit_41.clear()
                    self.lineEdit_50.clear()
                    self.lineEdit_39.clear()
                    self.lineEdit_51.clear()
                    self.groupBox_9.setEnabled(False)
                    self.statusBar().showMessage("Done Successfully", 5000)

                except:
                    QMessageBox.information(self, "Warning", "Invalid informations !")




            else :
                QMessageBox.information(self, "Warning", "Password and confirm password does not match!")



        else :
            QMessageBox.information(self, "Warning", "Missed username or national ID !")


    #############################################
    def Add_Employee_Permissions(self):
        employee_name = self.comboBox_19.currentText()
        if self.comboBox_19.currentIndex() != 0 :

            if self.checkBox_28.isChecked() == True:
                self.cur.execute(''' UPDATE  employee_permissions SET books_tab=%s ,clients_tab=%s,
                  settings_tab=%s ,add_book=%s,edit_book=%s,delete_book=%s,add_client=%s,edit_client=%s
                  ,delete_client=%s,add_branch=%s ,add_publisher=%s,add_author=%s,add_category=%s,add_employee=%s,
                  edit_employee=%s,is_admin=%s WHERE employee_name=%s'''
                                 , ( 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,employee_name))
                self.db.commit()
                self.statusBar().showMessage('Permissions added successfuly!',5000)

            else :
                books_tab = 0
                clients_tab = 0
                settings_tab = 0
                add_book = 0
                edit_book = 0
                delete_book = 0
                add_client = 0
                edit_client = 0
                delete_client = 0
                add_branch = 0
                add_publisher = 0
                add_auhor = 0
                add_category = 0
                add_employee = 0
                edit_employee = 0
                is_admin = 0

                if self.checkBox_19.isChecked() == True :
                    books_tab =1

                if self.checkBox_18.isChecked() == True:
                    clients_tab=1

                if self.checkBox_17.isChecked() == True :
                    settings_tab =1

                if self.checkBox.isChecked() == True :
                    add_book = 1

                if self.checkBox_2.isChecked() == True :
                    edit_book = 1

                if self.checkBox_3.isChecked() == True :
                    delete_book = 1

                if self.checkBox_15.isChecked() == True :
                    add_client = 1

                if self.checkBox_14.isChecked() == True :
                    edit_client = 1

                if self.checkBox_13.isChecked() == True :
                    delete_client = 1

                if self.checkBox_24.isChecked() == True :
                    add_branch = 1

                if self.checkBox_23.isChecked() == True :
                    add_publisher = 1

                if self.checkBox_22.isChecked() == True :
                    add_publisher = 1

                if self.checkBox_25.isChecked() == True :
                    add_category = 1

                if self.checkBox_26.isChecked() == True :
                    add_employee = 1

                if self.checkBox_27.isChecked() == True :
                    edit_employee = 1

                if self.checkBox_28.isChecked() == True :
                    is_admin = 1


                self.cur.execute('''UPDATE employee_permissions SET books_tab=%s ,clients_tab=%s,
                              settings_tab=%s ,add_book=%s,edit_book=%s,delete_book=%s,add_client=%s,edit_client=%s
                              ,delete_client=%s,add_branch=%s ,add_publisher=%s,add_author=%s,add_category=%s,
                              add_employee=%s,edit_employee=%s ,is_admin =%s WHERE employee_name=%s''',
                                 (books_tab, clients_tab, settings_tab,add_book,edit_book,delete_book
                                  ,add_client,edit_client,delete_client,add_branch,add_publisher,add_auhor
                                  ,add_category,add_employee,edit_employee,is_admin,employee_name))
                self.db.commit()
                self.statusBar().showMessage('Permissions added successfuly!',5000)

        else:
            QMessageBox.information(self, "Warning", "Please select an employee from the list above")



    def Show_All_Employees_Permissions(self):
        employee_name = self.comboBox_19.currentText()
        if self.comboBox_19.currentIndex() != 0:
            self.cur.execute('''SELECT books_tab,clients_tab,settings_tab,add_book,edit_book,delete_book,
            add_client,edit_client,delete_client,add_branch,add_publisher,add_author,add_category,
            add_employee,edit_employee , is_admin FROM employee_permissions  WHERE employee_name = %s ''',
                             [(employee_name)])
            data = self.cur.fetchone()
            self.checkBox_19.setChecked(data[0])
            self.checkBox_18.setChecked(data[1])
            self.checkBox_17.setChecked(data[2])
            self.checkBox.setChecked(data[3])
            self.checkBox_2.setChecked(data[4])
            self.checkBox_3.setChecked(data[5])
            self.checkBox_15.setChecked(data[6])
            self.checkBox_14.setChecked(data[7])
            self.checkBox_13.setChecked(data[8])
            self.checkBox_24.setChecked(data[9])
            self.checkBox_23.setChecked(data[10])
            self.checkBox_22.setChecked(data[11])
            self.checkBox_25.setChecked(data[12])
            self.checkBox_26.setChecked(data[13])
            self.checkBox_27.setChecked(data[14])
            self.checkBox_28.setChecked(data[15])


        else:
            self.checkBox_19.setChecked(0)
            self.checkBox_18.setChecked(0)
            self.checkBox_17.setChecked(0)
            self.checkBox.setChecked(0)
            self.checkBox_2.setChecked(0)
            self.checkBox_3.setChecked(0)
            self.checkBox_15.setChecked(0)
            self.checkBox_14.setChecked(0)
            self.checkBox_13.setChecked(0)
            self.checkBox_24.setChecked(0)
            self.checkBox_23.setChecked(0)
            self.checkBox_22.setChecked(0)
            self.checkBox_25.setChecked(0)
            self.checkBox_26.setChecked(0)
            self.checkBox_27.setChecked(0)
            self.checkBox_28.setChecked(0)










    #################Control Tabs######################
    def Open_Login_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_ResetPassword_Tab(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Daily_Movements_Tab(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Books_Tab(self):
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(3)

    def Open_Clients_Tab(self):
        self.tabWidget_3.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(4)


    def Open_Settings_Tab(self):
        self.tabWidget_4.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(5)

    def Open_Sign_Up_Tab(self):
        self.tabWidget.setCurrentIndex(1)
        self.lineEdit_57.clear()
        self.lineEdit_54.clear()
        self.lineEdit_56.clear()
        self.lineEdit_58.clear()
        self.lineEdit_55.clear()
        self.groupBox_8.hide()


    def Open_Login_Tab(self):
        self.tabWidget.setCurrentIndex(0)
        self.lineEdit_47.clear()
        self.lineEdit_48.clear()
        self.groupBox_7.hide()


    def User_Login_Permissions(self):
        self.groupBox_7.hide()
        self.pushButton_38.hide()
        user_name = self.lineEdit_47.text()
        password = self.lineEdit_48.text()
        if user_name != '' and password != '' :
            self.cur.execute(''' SELECT name , password FROM employee''')
            data = self.cur.fetchall()
            for row in data :
                if row[0] == user_name and row[1] == password :
                    self.Open_Daily_Movements_Tab()
                    self.groupBox_14.setEnabled(True)
                    self.pushButton.setEnabled(True)
                    self.pushButton_38.show()
                    self.cur.execute('''SELECT * FROM employee_permissions WHERE employee_name =%s''',(user_name))
                    user_permissions = self.cur.fetchone()
                    self.pushButton_2.setEnabled(False)
                    self.pushButton_3.setEnabled(False)
                    self.pushButton_9.setEnabled(False)
                    self.pushButton_10.setEnabled(False)
                    self.pushButton_11.setEnabled(False)
                    self.pushButton_13.setEnabled(False)
                    self.pushButton_15.setEnabled(False)
                    self.pushButton_16.setEnabled(False)
                    self.pushButton_18.setEnabled(False)
                    self.pushButton_19.setEnabled(False)
                    self.pushButton_20.setEnabled(False)
                    self.pushButton_21.setEnabled(False)
                    self.pushButton_22.setEnabled(False)
                    self.pushButton_27.setEnabled(False)
                    self.pushButton_28.setEnabled(False)




                    if user_permissions[2] == 1 :
                        self.pushButton_2.setEnabled(True)
                    if user_permissions[3] == 1 :
                        self.pushButton_3.setEnabled(True)
                    if user_permissions[4] == 1:           ## Settings
                        self.pushButton_9.setEnabled(True)
                    if user_permissions[5] == 1:  ## add_new_book
                        self.pushButton_10.setEnabled(True)
                    if user_permissions[6] == 1: # edit_book
                        self.pushButton_11.setEnabled(True)
                    if user_permissions[7] == 1 :  # Delete_book
                        self.pushButton_13.setEnabled(True)
                    if user_permissions[8] == 1 : #add client
                        self.pushButton_15.setEnabled(True)
                    if user_permissions[9] == 1 : #edit client
                        self.pushButton_16.setEnabled(True)
                    if user_permissions[10] == 1: #delete_client
                        self.pushButton_18.setEnabled(True)
                    if user_permissions[11] == 1:  #add_branch
                        self.pushButton_19.setEnabled(True)
                    if user_permissions[12] == 1:  #add_publisher
                        self.pushButton_20.setEnabled(True)
                    if user_permissions[13] == 1:  #add author
                        self.pushButton_21.setEnabled(True)
                    if user_permissions[14] == 1:  # add category
                        self.pushButton_22.setEnabled(True)
                    if user_permissions[15] == 1: #add employee
                        self.pushButton_27.setEnabled(True)
                    if user_permissions[16] == 1: #edit employee
                        self.pushButton_28.setEnabled(True)
                else:
                    self.groupBox_7.show()

        else:
            QMessageBox.information(self, "Warning", "Please enter your username and password")




    def Handle_Sign_Up(self):
        self.groupBox_8.hide()
        self.groupBox_7.hide()
        self.groupBox_8.hide()
        employee_name = self.lineEdit_57.text()
        employee_mail = self.lineEdit_54.text()
        employee_phone = self.lineEdit_56.text()
        password = self.lineEdit_58.text()
        password_2 = self.lineEdit_55.text()
        national_id = self.lineEdit_59.text()
        branch = 0
        date = datetime.datetime.now()

        if employee_name != " " and password != " "  and national_id != "":
            if password == password_2 and password != '':
                try:
                    self.cur.execute('''
                                INSERT INTO employee (name ,mail ,phone , date ,password,national_id,branch )
                                VALUES ( %s, %s, %s, %s, %s , %s ,%s ) ''', (employee_name, employee_mail,
                                  employee_phone,date , password,national_id,branch))
                    self.db.commit()
                    self.statusBar().showMessage('Your Account has been Created Successfully',5000)

                    self.cur.execute('''INSERT INTO employee_permissions (employee_name,books_tab,clients_tab,
                                            settings_tab, add_book,edit_book,delete_book,add_client,edit_client,
                                            delete_client,add_branch,add_publisher,add_author,add_category,
                                            add_employee,edit_employee,is_admin)
                             VALUES ( %s ,%s , %s , %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s)'''
                                     , (employee_name, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
                    self.db.commit()
                    self.Show_Employee()
                except:
                    QMessageBox.information(self, "Warning", "This National ID is already exist !")

            else :
                self.groupBox_8.show()

        else:
            QMessageBox.information(self, "Warning", "Please enter your informations completely")


    def Retry_Sign_Up(self):
        self.groupBox_8.hide()

    def Logout(self):
        logout_message = QMessageBox.question(self, 'Logout',
                                              "Are you sure you want to logout ?!",
                                              QMessageBox.Yes, QMessageBox.No)

        if logout_message == QMessageBox.Yes:
            self.Open_Login_Tab()
            self.groupBox_7.hide()
            self.pushButton_38.hide()
            self.groupBox_14.setEnabled(False)
            self.lineEdit_47.clear()
            self.lineEdit_48.clear()



def main():
    app=QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()


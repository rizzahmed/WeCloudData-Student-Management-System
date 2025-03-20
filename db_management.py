import mysql.connector
from mysql.connector import Error

# Config
from config import ConfigManager


class DBManager:
    def __init__(self):
        try:
            self.config_manager = ConfigManager()
            self.Connection = None
            self.ConnectionCredentials = self.config_manager.get_database_config()

        except Error as error:
            print("Failed to establish connection: {}".format(error))


    # ---------------------------- Read Student ----------------------------
    async def Read_Student(self, StudentID = None):
        try:
            self.Connection = mysql.connector.connect(
                host = self.ConnectionCredentials['host'],
                port = self.ConnectionCredentials['port'],
                user = self.ConnectionCredentials['user'],
                password = self.ConnectionCredentials['password'],
                database = self.ConnectionCredentials['database']
            )
            cursor = self.Connection.cursor()
            cursor.callproc('Proc_Read_Student', [ StudentID ])
            
            result_sets = list(cursor.stored_results())

            result_list = result_sets[0].fetchall()
            heading = ["ID", "Name", "Email", "Date of Birth"] #These are defining here, because the Heading might be different from the Database
            
            data = []
            for result in result_list:
                data.append({
                    "ID": result[0],
                    "StudentID": result[1],
                    "Name": result[2],
                    "Email": result[3],
                    "DOB": result[4].strftime("%Y-%m-%d") if result[4] is not None else None,
                })
            
            return heading, data

        except Error as error:
            print("Failed to Read Student: {}".format(error))
            self.Connection.rollback()
        finally:
            cursor.close()
            self.Connection.close()

    # ---------------------------- Delete Student ----------------------------
    async def Delete_Student(self, StudentID):
        try:
            self.Connection = mysql.connector.connect(
                host = self.ConnectionCredentials['host'],
                port = self.ConnectionCredentials['port'],
                user = self.ConnectionCredentials['user'],
                password = self.ConnectionCredentials['password'],
                database = self.ConnectionCredentials['database']
            )
            cursor = self.Connection.cursor()
            cursor.callproc('Proc_Delete_Student', [ StudentID ])
            
            result_sets = list(cursor.stored_results())

            if not result_sets:
                return {"status": False, "message": "No response from database"}

            result_list = result_sets[0].fetchall()

            # Debugging: Print the results
            print("Stored Procedure Output:", result_list)

            if result_list:
                message, status = result_list[0]
                if status == 1:
                    self.Connection.commit()
                return {"status": bool(status), "message": message}
            else:
                return {"status": False, "message": "Unexpected database response"}

        except Error as error:
            print("Failed to Update Student: {}".format(error))
            self.Connection.rollback()
        finally:
            cursor.close()
            self.Connection.close()
  
    # ---------------------------- Search Student ----------------------------
    async def Search_Student(self, obj):
        try:
            self.Connection = mysql.connector.connect(
                host = self.ConnectionCredentials['host'],
                port = self.ConnectionCredentials['port'],
                user = self.ConnectionCredentials['user'],
                password = self.ConnectionCredentials['password'],
                database = self.ConnectionCredentials['database']
            )
            cursor = self.Connection.cursor()
            cursor.callproc('Proc_Search_Student', [  obj.get('params') ])
            
            result_sets = list(cursor.stored_results())

            result_list = result_sets[0].fetchall()
            
            data = []
            for result in result_list:
                 data.append({
                    "ID": result[0],
                    "StudentID": result[1],
                    "Name": result[2],
                    "Email": result[3],
                    "DOB": result[4].strftime("%Y-%m-%d") if result[4] is not None else None,
                })
            
            return data

        except Error as error:
            print("Failed to Search Student: {}".format(error))
            self.Connection.rollback()
        finally:
            cursor.close()
            self.Connection.close()
    
    # ---------------------------- Save/Update Student ----------------------------
    async def Save_Student(self, obj):
        try:
            self.Connection = mysql.connector.connect(
                host = self.ConnectionCredentials['host'],
                port = self.ConnectionCredentials['port'],
                user = self.ConnectionCredentials['user'],
                password = self.ConnectionCredentials['password'],
                database = self.ConnectionCredentials['database']
            )
            cursor = self.Connection.cursor()
            cursor.callproc('Proc_Save_Student', 
            [  
                obj.get('id'),
                obj.get('studentid'),
                obj.get('name'),
                obj.get('email'),
                obj.get('dob')
              ])
            
            # Fetch results from the stored procedure
            result_sets = list(cursor.stored_results())

            if not result_sets:
                return {"status": False, "message": "No response from database"}

            result_list = result_sets[0].fetchall()

            # Debugging: Print the results
            print("Stored Procedure Output:", result_list)

            if result_list:
                message, status = result_list[0]
                if status == 1:
                    self.Connection.commit()
                return {"status": bool(status), "message": message}
            else:
                return {"status": False, "message": "Unexpected database response"}
           
        except Error as error:
            print("Failed to Search Student: {}".format(error))
            self.Connection.rollback()
        finally:
            cursor.close()
            self.Connection.close()



    
    # ---------------------------- Bar Graph ----------------------------
    async def Read_Bar_Chart(self):
        try:
            self.Connection = mysql.connector.connect(
                host = self.ConnectionCredentials['host'],
                port = self.ConnectionCredentials['port'],
                user = self.ConnectionCredentials['user'],
                password = self.ConnectionCredentials['password'],
                database = self.ConnectionCredentials['database']
            )
            cursor = self.Connection.cursor()
            cursor.callproc('Proc_Read_Bar_Chart')
            
            result_sets = list(cursor.stored_results())

            result_list = result_sets[0].fetchall()
            
            data = []
            for result in result_list:
                data.append({
                    "CourseName": result[0],
                    "StudentCount": result[1]
                })
            
            return data

        except Error as error:
            print("Failed to Read Bar Chart: {}".format(error))
            self.Connection.rollback()
        finally:
            cursor.close()
            self.Connection.close()
    
    
    # ---------------------------- Pie Graph ----------------------------
    async def Read_Pie_Chart(self):
        try:
            self.Connection = mysql.connector.connect(
                host = self.ConnectionCredentials['host'],
                port = self.ConnectionCredentials['port'],
                user = self.ConnectionCredentials['user'],
                password = self.ConnectionCredentials['password'],
                database = self.ConnectionCredentials['database']
            )
            cursor = self.Connection.cursor()
            cursor.callproc('Proc_Read_Pie_Chart')
            
            result_sets = list(cursor.stored_results())

            result_list = result_sets[0].fetchall()
            
            data = []
            for result in result_list:
                data.append({
                    "CourseName": result[0],
                    "StudentCount": result[1],
                    "Percentage": result[2]
                })
            
            return data

        except Error as error:
            print("Failed to Read Pie Chart: {}".format(error))
            self.Connection.rollback()
        finally:
            cursor.close()
            self.Connection.close()


    
    
    
    # ---------------------------- Read Course ----------------------------
    async def Read_Course(self, StudentID = None):
        try:
            self.Connection = mysql.connector.connect(
                host = self.ConnectionCredentials['host'],
                port = self.ConnectionCredentials['port'],
                user = self.ConnectionCredentials['user'],
                password = self.ConnectionCredentials['password'],
                database = self.ConnectionCredentials['database']
            )
            cursor = self.Connection.cursor()
            cursor.callproc('Proc_Read_Course', [ StudentID ])
            
            result_sets = list(cursor.stored_results())

            result_list = result_sets[0].fetchall()
            heading = ["Course Name", "Course Code", "Instructor", "Credits"] #These are defining here, because the Heading might be different from the Database
            
            data = []
            for result in result_list:
                data.append({
                    "ID": result[0],
                    "CourseName": result[1],
                    "CourseCode": result[2],
                    "Instructor": result[3],
                    "Credits": result[4]
                })
            
            return heading, data

        except Error as error:
            print("Failed to Read Student: {}".format(error))
            self.Connection.rollback()
        finally:
            cursor.close()
            self.Connection.close()

    # ---------------------------- Delete Course ----------------------------
    async def Delete_Course(self, StudentID):
        try:
            self.Connection = mysql.connector.connect(
                host = self.ConnectionCredentials['host'],
                port = self.ConnectionCredentials['port'],
                user = self.ConnectionCredentials['user'],
                password = self.ConnectionCredentials['password'],
                database = self.ConnectionCredentials['database']
            )
            cursor = self.Connection.cursor()
            cursor.callproc('Proc_Delete_Student', [ StudentID ])
            
            result_sets = list(cursor.stored_results())

            if not result_sets:
                return {"status": False, "message": "No response from database"}

            result_list = result_sets[0].fetchall()

            # Debugging: Print the results
            print("Stored Procedure Output:", result_list)

            if result_list:
                message, status = result_list[0]
                if status == 1:
                    self.Connection.commit()
                return {"status": bool(status), "message": message}
            else:
                return {"status": False, "message": "Unexpected database response"}

        except Error as error:
            print("Failed to Update Student: {}".format(error))
            self.Connection.rollback()
        finally:
            cursor.close()
            self.Connection.close()
  
    # ---------------------------- Search Course ----------------------------
    async def Search_Course(self, obj):
        try:
            self.Connection = mysql.connector.connect(
                host = self.ConnectionCredentials['host'],
                port = self.ConnectionCredentials['port'],
                user = self.ConnectionCredentials['user'],
                password = self.ConnectionCredentials['password'],
                database = self.ConnectionCredentials['database']
            )
            cursor = self.Connection.cursor()
            cursor.callproc('Proc_Search_Course', [  obj.get('params') ])
            
            result_sets = list(cursor.stored_results())

            result_list = result_sets[0].fetchall()
            
            data = []
            for result in result_list:
                 data.append({
                    "ID": result[0],
                    "CourseName": result[1],
                    "CourseCode": result[2],
                    "Instructor": result[3],
                    "Credits": result[4],
                })
            
            return data

        except Error as error:
            print("Failed to Search Student: {}".format(error))
            self.Connection.rollback()
        finally:
            cursor.close()
            self.Connection.close()
    
    # ---------------------------- Save/Update Course ----------------------------
    async def Save_Course(self, obj):
        try:
            self.Connection = mysql.connector.connect(
                host = self.ConnectionCredentials['host'],
                port = self.ConnectionCredentials['port'],
                user = self.ConnectionCredentials['user'],
                password = self.ConnectionCredentials['password'],
                database = self.ConnectionCredentials['database']
            )
            cursor = self.Connection.cursor()
            cursor.callproc('Proc_Save_Student', 
            [  
                obj.get('id'),
                obj.get('studentid'),
                obj.get('name'),
                obj.get('email'),
                obj.get('dob')
              ])
            
            # Fetch results from the stored procedure
            result_sets = list(cursor.stored_results())

            if not result_sets:
                return {"status": False, "message": "No response from database"}

            result_list = result_sets[0].fetchall()

            # Debugging: Print the results
            print("Stored Procedure Output:", result_list)

            if result_list:
                message, status = result_list[0]
                if status == 1:
                    self.Connection.commit()
                return {"status": bool(status), "message": message}
            else:
                return {"status": False, "message": "Unexpected database response"}
           
        except Error as error:
            print("Failed to Search Student: {}".format(error))
            self.Connection.rollback()
        finally:
            cursor.close()
            self.Connection.close()




    

if __name__ == '__main__':   
    DB = DBManager()
    DB.Read_Student()
 
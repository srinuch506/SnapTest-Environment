from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify
import pymysql
import pandas as pd
import io

db_config = {
    'host': 'localhost',
    'port': 3306,
    'db': 'codegnantest',
    'user': 'root',
    'password': 'CHsrinu@506',
    'charset': 'utf8mb4',
    'autocommit': True
}

app = Flask(__name__)


@app.route("/")
def landing():
    return render_template("home.html")

@app.route("/landing1")
def landing1():
    return render_template("home.html")

@app.route("/abc")
def abc():
    return render_template("abc.html")

@app.route("/adminlogin")
def adminlogin():
    return render_template("adminlogin.html")

@app.route("/studentlogin", methods=["GET", "POST"])
def studentlogin():
    if request.method == "POST":
        # Handle form submission - redirect to student dashboard
        return redirect(url_for('studentdashboard'))
    return render_template("studentlogin.html")

@app.route("/admindashboard", methods=["POST", "GET"])
def admindashboard():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username == "snaptest" and password == "snap@test":
            return render_template("adminpage.html")
        else:
            return render_template("adminlogin.html", error="Invalid credentials")
    return render_template("adminpage.html")

@app.route("/studentdashboard", methods=["POST", "GET"])
def studentdashboard():
    if request.method == "POST":
        rollno = request.form['rollnumber']
        name = request.form['name']
        batch = request.form['batch']
        conn = None
        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()

            # Check if student exists and get their status
            q_check = "SELECT rollnumber, name, batch, status FROM test WHERE rollnumber = %s"
            cursor.execute(q_check, (rollno,))
            existing_student = cursor.fetchone()
            
            if existing_student:
                student_status = existing_student[3]
                
                # Block if already completed or disqualified
                if student_status in ['Correct Submission', 'Exit Count Exceeded']:
                    return render_template("studentlogin.html", error="You have already completed this test and cannot retake it.")

                # Verify login credentials for registered users
                if existing_student[1] == name and existing_student[2] == batch:
                    # Login successful - get test content
                    q_select = "SELECT * FROM testcontent"
                    cursor.execute(q_select)
                    rows = cursor.fetchall()
                    x = [i[0] for i in rows]
                    
                    return render_template("testpage.html", data=x, rollno=rollno)
                else:
                    # Wrong credentials
                    return render_template("studentlogin.html", error="Invalid credentials. Please check your details.")
            else:
                # Student doesn't exist - create new entry and start test
                q_insert = "INSERT INTO test(rollnumber, name, batch, status) VALUES (%s, %s, %s, %s)"
                cursor.execute(q_insert, (rollno, name, batch, "Registered"))
                conn.commit()

                # Get test content for the test page
                q_select = "SELECT * FROM testcontent"
                cursor.execute(q_select)
                rows = cursor.fetchall()
                x = [i[0] for i in rows]
                
                return render_template("testpage.html", data=x, rollno=rollno)

        except pymysql.Error as e:
            print(f"PyMySQL Error in studentdashboard: {e}")
            return f"Database Error: {e}"
        except Exception as e:
            print(f"Error in studentdashboard: {e}")
            return f"Error Occurred: {e}"
        finally:
            if conn:
                conn.close()
    return redirect(url_for('studentlogin'))

@app.route("/get_test_content", methods=["POST"])
def get_test_content():
    if request.method == "POST":
        rollno = request.form['rollnumber']
        name = request.form['name']
        batch = request.form['batch']
        status = "Correct Submission"
        conn = None
        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()

            q_check = "SELECT rollnumber FROM test WHERE rollnumber = %s"
            cursor.execute(q_check, (rollno,))
            if cursor.fetchone():
                return jsonify({"error": "Student Already Exists with same roll number"})

            q_insert = "INSERT INTO test(rollnumber, name, batch, status) VALUES (%s, %s, %s, %s)"
            cursor.execute(q_insert, (rollno, name, batch, status))
            conn.commit()

            q_select = "SELECT * FROM testcontent"
            cursor.execute(q_select)
            rows = cursor.fetchall()
            images = [i[0] for i in rows]
            
            return jsonify({"success": True, "images": images, "rollno": rollno})
        except pymysql.Error as e:
            print(f"PyMySQL Error in get_test_content: {e}")
            return jsonify({"error": f"Database Error: {e}"})
        except Exception as e:
            print(f"Error in get_test_content: {e}")
            return jsonify({"error": f"Error Occured: {e}"})
        finally:
            if conn:
                conn.close()
    return jsonify({"error": "Invalid request method"})

@app.route("/testpage", methods=["POST"])
def testpage():
    rollno = request.form['exitcount']
    conn = None
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        q = "UPDATE test SET status = 'Exit Count Exceeded' WHERE rollnumber = %s"
        cursor.execute(q, (rollno,))
        conn.commit()
        return redirect(url_for('landing'))
    except Exception as e:
        print(f"Error in testpage: {e}")
        return "Error Occurred, Go back and Try Again"
    finally:
        if conn:
            conn.close()

@app.route("/testpage1", methods=["POST"])
def testpage1():
    rollno = request.form['exitcount']
    conn = None
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        q = "UPDATE test set status = 'Correct Submission' where rollnumber = %s"
        cursor.execute(q, (rollno,))
        conn.commit()
        return render_template("abc.html")
    except Exception as e:
        print(f"Error in testpage1: {e}")
        return "Error Occured, Go back and Try Again"
    finally:
        if conn:
            conn.close()

@app.route("/cleardata", methods=["POST"])
def cleardata():
    conn = None
    try:
        print("Clearing student data")
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        q = "TRUNCATE TABLE test"
        cursor.execute(q)
        conn.commit()
        return jsonify({"success": True, "message": "All student data cleared"})
    except Exception as e:
        print(f"Error in cleardata: {e}")
        return jsonify({"success": False, "message": "Error occurred while clearing data"})
    finally:
        if conn:
            conn.close()

@app.route("/cleartestcontent", methods=["POST"])
def cleartestcontent():
    conn = None
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        q = "TRUNCATE TABLE testcontent"
        cursor.execute(q)
        conn.commit()
        return jsonify({"success": True, "message": "All test content cleared successfully"})
    except Exception as e:
        print(f"Error in cleartestcontent: {e}")
        return jsonify({"success": False, "message": "Error occurred while clearing test content"})
    finally:
        if conn:
            conn.close()

@app.route("/testcontent", methods=["GET"])
def testcontent():
    return render_template("testcontent.html")

@app.route("/taketestcontent", methods=["POST"])
def taketestcontent():
    data = request.form['content']
    conn = None
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        q = "INSERT INTO testcontent VALUES (%s)"
        cursor.execute(q, (data,))
        conn.commit()
        return render_template("testcontent.html", x="Stored Successfully")
    except Exception as e:
        print(f"Error in taketestcontent: {e}")
        return render_template("testcontent.html", x="Error Occured Try again")
    finally:
        if conn:
            conn.close()

@app.route("/showstudentsdata", methods=["GET"])
def showstudentsdata():
    conn = None
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        q = "SELECT * FROM test"
        cursor.execute(q)
        rows = cursor.fetchall()
        return render_template("showstudentsdata.html", data=rows)
    except Exception as e:
        print(f"Error in showstudentsdata: {e}")
        return "Error Occured, Try again"
    finally:
        if conn:
            conn.close()

@app.route("/deletestudent", methods=["POST"])
def deletestudent():
    data = request.form['rollno']
    conn = None
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        # Check if student exists before deleting
        q_check = "SELECT rollnumber FROM test WHERE rollnumber = %s"
        cursor.execute(q_check, (data,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Student not found"})
        
        # Delete the student
        q_delete = "DELETE FROM test WHERE rollnumber = %s"
        cursor.execute(q_delete, (data,))
        conn.commit()
        
        # Return success response
        return jsonify({"success": True, "message": "Student deleted successfully"})
        
    except Exception as e:
        print(f"Error in deletestudent: {e}")
        return jsonify({"success": False, "message": "Error occurred while deleting student"})
    finally:
        if conn:
            conn.close()

@app.route('/download-excel', methods=["GET"])
def download_excel():
    conn = None
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        q = "SELECT * FROM test"
        cursor.execute(q)
        rows = cursor.fetchall()
        
        # Create DataFrame without explicit columns to avoid type issues
        df = pd.DataFrame(rows)
        df.columns = ["Roll Number", "Name", "Batch", "Status", "Exit Count"]
        
        # Create temporary file with proper cleanup
        import tempfile
        import os
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        temp_file.close()  # Close immediately to release the file handle
        
        try:
            # Write to the temporary file
            df.to_excel(temp_file.name, index=False, sheet_name='Sheet1', engine='openpyxl')
            
            # Read the file content
            with open(temp_file.name, 'rb') as f:
                file_data = f.read()
            
            # Create BytesIO object from file data
            output = io.BytesIO(file_data)
            output.seek(0)
            
            return send_file(
                output, 
                as_attachment=True, 
                download_name='test_data.xlsx', 
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file.name)
            except OSError:
                pass  # File might already be deleted
                
    except Exception as e:
        print(f"Error in download_excel: {e}")
        return "Error Occured, Go back and Try Again"
    finally:
        if conn:
            conn.close()

@app.route("/starttest", methods=["POST"])
def starttest():
    rollno = request.form['rollno']
    conn = None
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        q = "SELECT * FROM testcontent"
        cursor.execute(q)
        rows = cursor.fetchall()
        data = [i[0] for i in rows]
        return render_template("testpage.html", data=data, rollno=rollno)
    except Exception as e:
        print(f"Error in starttest: {e}")
        return "Error loading questions"
    finally:
        if conn:
            conn.close()

@app.route('/check_status/<string:rollno>')
def check_status(rollno):
    conn = None
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        q = "SELECT status FROM test WHERE rollnumber = %s"
        cursor.execute(q, (rollno,))
        result = cursor.fetchone()
        if result:
            return jsonify({'status': result[0]})
        else:
            return jsonify({'status': 'Not Found'})
    except Exception as e:
        print(f"Error in check_status: {e}")
        return jsonify({'status': 'Error'})
    finally:
        if conn:
            conn.close()

@app.route('/increment_exit_count', methods=['POST'])
def increment_exit_count():
    rollno = request.form['rollno']
    conn = None
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        # Get current exit count
        cursor.execute("SELECT exit_count FROM test WHERE rollnumber = %s", (rollno,))
        result = cursor.fetchone()
        if not result:
            return jsonify({'success': False, 'message': 'Student not found'})
        exit_count = result[0] + 1
        # If exit count exceeds 3, disqualify
        if exit_count > 3:
            cursor.execute("UPDATE test SET exit_count = %s, status = 'Exit Count Exceeded' WHERE rollnumber = %s", (exit_count, rollno))
            conn.commit()
            return jsonify({'success': True, 'blocked': True, 'exit_count': exit_count})
        else:
            cursor.execute("UPDATE test SET exit_count = %s WHERE rollnumber = %s", (exit_count, rollno))
            conn.commit()
            return jsonify({'success': True, 'blocked': False, 'exit_count': exit_count})
    except Exception as e:
        print(f"Error in increment_exit_count: {e}")
        return jsonify({'success': False, 'message': 'Error occurred'})
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    app.run(debug=True)
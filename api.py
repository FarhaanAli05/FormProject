from flask import Flask, request, render_template

app = Flask(__name__)

table = []
table_headers = {"First name": "", "Last name": "", "Gender": "", "Birthday": "", "Email": "", "Phone number": ""}
logged_in = False

@app.route('/form', methods=['GET'])
def get_form():
    # If the form page is accessed and the user has not logged in, prompt them with the login menu
    global logged_in
    if request.method == 'GET' and logged_in == False:
        return render_template('login.html')
    # If the user clicks update for a row, pre fill the form with the data they already filled in
    if request.method == 'GET' and request.args.get('update'):
        fname = ""
        lname = ""
        gender = ""
        bday = ""
        email = ""
        phone = ""
        index = request.args.get('update')
        # Error checking: Chek if the row index is greater than 0 and less than the length of the table list
        if 0 <= int(index) < len(table):
            for key in table[int(index)]:
                if key == 'fname':
                    fname = table[int(index)][key]
                elif key == 'lname':
                    lname = table[int(index)][key]
                elif key == 'gender':
                    gender = table[int(index)][key]
                elif key =='bday':
                    bday = table[int(index)][key]
                elif key == 'email':
                    email = table[int(index)][key]
                elif key == 'phone':
                    phone = table[int(index)][key]
        else:
            return render_template('table.html', table_headers=table_headers)
        update = True
        return render_template('form.html', fname=fname, lname=lname, gender=gender, bday=bday, email=email, phone=phone, update=update, index=index)
    # Display the form
    return render_template('form.html')

@app.route('/', methods=['GET', 'POST'])
def get_form_data():
    global logged_in
    incorrect = False
    # If the main page is accessed and the user has not logged in, prompt them with the login menu
    if request.method == 'GET' and logged_in == False:
        return render_template('login.html')
    # If the user attempts to log in...
    if request.method == 'POST' and logged_in == False:
        if request.form.get('username') == "JohnDoe":
            if request.form.get('password') == "John123":
                logged_in = True
                return render_template('table.html', table=table, table_headers=table_headers) # Show them the table (main page) if the user successfully logs in
            else:
                incorrect = True # Show an incorrect message if the user unsuccessfully logs in
                return render_template('login.html', incorrect=incorrect)
        else:
            incorrect = True
            return render_template('login.html', incorrect=incorrect)
    # Delete a table row according to its row index
    if request.method == 'GET' and request.args.get('delete'):
        index = request.args.get('delete')
        # Error checking: Chek if the row index is greater than 0 and less than the length of the table list
        if 0 <= int(index) < len(table):
            del table[int(index)]
        else:
            return render_template('table.html', table_headers=table_headers)
        return render_template('table.html', table=table, table_headers=table_headers)
    # If the user updates a row, update it and display it
    elif request.method == 'POST' and request.args.get('update'):
        index = request.args.get('update')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        gender = request.form.get('gender')
        if gender == None:
            gender = ""
        bday = request.form.get('bday')
        email = request.form.get('email')
        phone = request.form.get('phone')
        # Error checking: Chek if the row index is greater than 0 and less than the length of the table list
        if 0 <= int(index) < len(table):
            table[int(index)] = {'fname': fname, 'lname': lname, 'gender': gender, 'bday': bday, 'email': email, 'phone': phone}
        else:
            return render_template('table.html', table_headers=table_headers)
        return render_template('table.html', table=table, table_headers=table_headers)
    # If the user submits a form, display the data in a row in the table
    elif request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        gender = request.form.get('gender')
        if gender == None:
            gender = ""
        bday = request.form.get('bday')
        email = request.form.get('email')
        phone = request.form.get('phone')
        table_entry = {'fname': fname, 'lname': lname, 'gender': gender, 'bday': bday, 'email': email, 'phone': phone}
        table.append(table_entry)
        return render_template('table.html', table=table, table_headers=table_headers, table_entry=table_entry)
    else:
        # Display the table by default
        return render_template('table.html', table=table, table_headers=table_headers)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, render_template

app = Flask(__name__)

table = []
table_headers = {"First name": "", "Last name": "", "Gender": "", "Birthday": "", "Email": "", "Phone number": ""}

@app.route('/form', methods=['GET'])
def get_form():
    # View the form after a row has been updated
    if request.method == 'GET' and request.args.get('update'):
        fname = ""
        lname = ""
        gender = ""
        bday = ""
        email = ""
        phone = ""
        index = request.args.get('update')
        # Error checking: See if the row index is equal to or greater than zero and less than the length of the table
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
    # Delete a table row according to its row index
    if request.method == 'GET' and request.args.get('delete'):
        index = request.args.get('delete')
        # Error checking: See if row index is equal to or greater than zero and less than the length of the table
        if 0 <= int(index) < len(table):
            del table[int(index)]
        else:
            return render_template('table.html', table_headers=table_headers)
        return render_template('table.html', table=table, table_headers=table_headers)
    # If the form is updated, update the table row and display it
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
        # Error checking: See if row index is equal to or greater than zero and less than the length of the table
        if 0 <= int(index) < len(table):
            table[int(index)] = {'fname': fname, 'lname': lname, 'gender': gender, 'bday': bday, 'email': email, 'phone': phone}
        else:
            return render_template('table.html', table_headers=table_headers)
        return render_template('table.html', table=table, table_headers=table_headers)
    # If the form submits, retrieve the form data and display it in a table
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
        # Otherwise, display the table as is
        return render_template('table.html', table=table, table_headers=table_headers)

if __name__ == '__main__':
    app.run(debug=True)
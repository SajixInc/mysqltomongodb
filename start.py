from flask import Flask, request, render_template, flash
from table_connection import connection
import migrate


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  ## need to check
name = ''

@app.route('/', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            details = request.form.to_dict()
            mysql = details['mysql']
            mongo = details['mongo']
            myuser = details['user']
            mypassword = details['pass']
            connection(mysql, mongo, myuser, mypassword)
            flash(f'!!!!!!______tables migrated____!')
            for name in migrate.table_count_s:
                flash(name)

            flash(f'!!!!!!______tables not migrated(empty tables)___!')
            for name in migrate.table_count_e:
                flash(name)
            flash('/migrate successful/')
        else:
            error = "fail to fetch form data"
    except Exception as e:
        print(e)
    return render_template("dataMigrate.html")


if __name__ == '__main__':
    app.run(debug=True,  port=8080)

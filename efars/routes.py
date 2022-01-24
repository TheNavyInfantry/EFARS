from efars import app
from flask import Flask, render_template, redirect, url_for, request
from efars.forms import FileForm
from werkzeug.utils import secure_filename

@app.route('/', methods=['GET','POST'])
def index():
    form = FileForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        print(filename)
        return redirect(url_for('index'))

    return render_template('index.html', form=form)


@app.route('/about/', methods=['GET'])
def about():
    return render_template("about.html")

@app.route('/terms-and-conditions/', methods=['GET'])
def terms_conditions():
    return render_template("terms.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(413)
def file_size_exceed(e):
    return render_template('404.html'), 413
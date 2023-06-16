import subprocess

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask import Flask, render_template, redirect
import os
import uuid
import shutil


SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


class UrlForm(FlaskForm):
    urls = TextAreaField("Список URL для проверки", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ResultForm(FlaskForm):
    result = TextAreaField("Результаты")
    back = SubmitField("Назад")


@app.route('/', methods=['GET', 'POST'])
def red():
    return redirect('/check_urls')


@app.route('/check_urls', methods=['GET', 'POST'])
def submit():
    form = UrlForm()
    if form.validate_on_submit():
        urls = form.urls.data
        directory = str(uuid.uuid4())
        os.mkdir(directory)
        shutil.copyfile('check_bandwidth.py', f'{directory}/check_bandwidth.py')
        with open(f'{directory}/urls.txt', 'w', encoding='UTF-8') as file:
            file.write(urls)
        with open(f'{directory}/check_bandwidth.py', 'r') as pyfile:
            old_data = pyfile.read()
            new_data = old_data.replace("with open('urls.txt', 'r') as urls_file:",
                                        f"with open('{os.path.abspath(f'{directory}/urls.txt')}', 'r') as urls_file:")
            new_new_data = new_data.replace("with open('result.txt', 'a') as file:",
                                            f"with open('{os.path.abspath(f'{directory}/result.txt')}', 'a') as file:")
        with open(f'{directory}/check_bandwidth.py', 'w') as pyfile:
            pyfile.write(new_new_data)
        with open(f'{directory}/result.txt', 'w', encoding='UTF-8') as init_file:
            init_file.write('')
        with open('templates/result.html', 'r') as template:
            old_data = template.read()
            new_data = old_data.replace('/result', f'/result/{directory}')
        with open(f'templates/result_{directory}.html', 'w') as template:
            template.write(new_data)
        return redirect(f'/result/{directory}')
    return render_template('submit.html', form=form)


@app.route('/result/<directory>', methods=['GET', 'POST'])
def result(directory):
    form = ResultForm()
    if ('pid' in os.listdir(directory)) is False:
        p = subprocess.Popen(["python", f"{os.path.abspath(f'{directory}/check_bandwidth.py')}"])
        with open(f'{directory}/pid', 'w') as pid:
            pid.write(str(p.pid))
    with open(f'{directory}/result.txt', 'r') as file:
        text = file.read()
    try:
        last_string = text.splitlines()[-1]
    except IndexError:
        last_string = ''
    if last_string == 'Done!':
        form_text = text
        form.result.data = form_text
    else:
        form_text = text
        form.result.data = f'{form_text}\nПроверка ещё не завершена'
    if form.validate_on_submit():
        with open(f'{directory}/pid', 'r') as pid_file:
            pid = pid_file.read()
        os.system(f'kill {pid}')
        shutil.rmtree(directory)
        os.remove(f'templates/result_{directory}.html')
        return redirect('/check_urls')
    return render_template(f'result_{directory}.html', form=form)

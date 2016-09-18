from flask import current_app, Flask, render_template, request, send_from_directory
from lib import UniModHelper
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './mods'

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        UniModHelper(**request.form.to_dict())
        mods_path = os.path.join(current_app.root_path, 'mods')
        zip_file = '{0}.zip'.format(request.form['modname'])
        return send_from_directory(directory=mods_path, filename=zip_file)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

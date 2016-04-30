from flask import current_app, Flask, render_template, request, send_from_directory
from lib import initialize, init_conf
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = init_conf().get('base_paths', 'mods')

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        initialize(**request.form.to_dict())
        return send_from_directory(directory=os.path.join(current_app.root_path, 'mods'), filename='{0}.zip'.format(request.form['modname']))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

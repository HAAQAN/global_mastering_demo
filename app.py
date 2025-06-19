from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    name, ext = os.path.splitext(filename)
    # Gerçek mastering işlemi burada yapılacak, şimdilik dummy kopyalar:
    soft = f"{name}-GLOBAL MASTERED - Soft{ext}"
    normal = f"{name}-GLOBAL MASTERED - Normal{ext}"
    fast = f"{name}-GLOBAL MASTERED - Fast{ext}"

    soft_path = os.path.join(PROCESSED_FOLDER, soft)
    normal_path = os.path.join(PROCESSED_FOLDER, normal)
    fast_path = os.path.join(PROCESSED_FOLDER, fast)

    # Dummy olarak input dosyasını kopyalıyoruz (yerine FFmpeg master işlemi gelecek)
    for src, dst in [(input_path, soft_path), (input_path, normal_path), (input_path, fast_path)]:
        with open(src, 'rb') as fsrc:
            with open(dst, 'wb') as fdst:
                fdst.write(fsrc.read())

    return jsonify({
        'soft': f'/processed/{soft}',
        'normal': f'/processed/{normal}',
        'fast': f'/processed/{fast}'
    })

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)

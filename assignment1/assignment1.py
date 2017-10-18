from flask import Flask, request, jsonify
import rocksdb, os, random
import subprocess

UPLOAD_FOLDER = '/tmp'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = rocksdb.DB("assignment1.db", rocksdb.Options(create_if_missing=True))


@app.route('/api/v1/scripts', methods=['POST'])
def upload_file():
    if 'data' not in request.files:
        return jsonify({"Message": "Failed to upload."}), 400
    file = request.files['data']

    if file.filename == '':
        return jsonify({"Message": "File name is empty."}), 400

    if file.filename.rsplit('.', 1)[1].lower() != 'py':
        return jsonify({"Message": "Is not a python file."}), 400

    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)

    id = random.getrandbits(128)
    db.put(bytes(str(id), encoding='UTF-8'), bytes(path, encoding='UTF-8'))

    return jsonify({'script-id': id}), 201


@app.route('/api/v1/scripts/<int:script_id>', methods=['GET'])
def run_script(script_id):
    value = db.get(bytes(str(script_id), 'UTF-8'))

    if value is None:
        return 'ID is not correct.\n', 400
    subproc = subprocess.Popen(['python3.6', value], stdout=subprocess.PIPE)
    output, errs = subproc.communicate()
    return output


if __name__ == '__main__':
    app.run("0.0.0.0", 80)

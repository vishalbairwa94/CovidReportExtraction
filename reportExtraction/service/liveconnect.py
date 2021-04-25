import os

import flask_excel
import pytesseract
import spacy
from PIL import Image
from flasgger import Swagger, swag_from
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

spacy_nlp = spacy.load('en_core_web_sm')
from reportExtraction.utils.extraction import name_extraction, fetch_date, report_result, validation

# creating a Flask app
app = Flask(__name__)
swagger = Swagger(app)
flask_excel.init_excel(app)
CORS(app)


@app.route('/covidExtraction', methods=['POST'])
@swag_from('fileDownload.yml')
def covrex():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(filename)
    file_path = '/Users/vishalbairwa/IdeaProjects/CovidReportExtraction/reportExtraction/service/' + filename

    output = file_path
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'
    text = pytesseract.image_to_string(Image.open(output))
    text_splitted = text.splitlines()

    name = name_extraction(text_splitted)
    report_res = report_result(text_splitted)
    date = fetch_date(text_splitted)
    validation_report = validation(date)

    result = {}
    result['Name'] = name
    result['Result'] = report_res
    result['Date'] = date
    result['Validation'] = validation_report
    if report_res == 'POSITIVE':
        result['Validation'] = 'NOT VALIDATED'
    os.remove(output)

    return jsonify({'data': result})


if __name__ == '__main__':
    app.run(debug=True)

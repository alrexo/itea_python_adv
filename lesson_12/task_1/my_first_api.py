import csv
import json

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/add', methods=['POST'])
def add_csv():
    body = request.form
    product_name, amount = body['product_name'], body['amount']
    try:
        int(amount)
    except ValueError:
        return 'Amount value is invalid!', 400
    with open('data.csv', 'a+') as csvfile:
        csvfile.seek(0)
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if product_name == row[0]:
                return 'Product already exists!', 400
        csvfile.write(product_name + ',' + amount + '\n')
    return 'OK, got you.', 200


@app.route('/list', methods=['GET'])
def show_list():
    product_name = request.args.get('name')
    with open('data.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = []
        if product_name:
            for row in reader:
                if product_name == row[0]:
                    line = dict()
                    line['product_name'], line['amount'] = row[0], row[1]
                    data.append(line)
                    break
            if not data:
                return 'Product not found!', 400
        else:
            for row in reader:
                line = dict()
                line['product_name'], line['amount'] = row[0], row[1]
                data.append(line)
        json_data = json.dumps(data, indent=4)
        return str(json_data)


if __name__ == '__main__':
    app.run(port=9000)

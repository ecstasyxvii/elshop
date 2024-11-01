from flask import Flask, jsonify, request, render_template
import json
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

def load_products():
    with open("data/products.json", "r") as file:
        return json.load(file)
    
def load_orders():
    try:
        with open("data/orders.json", "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []
    
def save_order(order):
    orders = load_orders()
    orders.append(order)
    with open("data/orders.json", "w") as file:
        json.dump(orders, file, indent=4)
    
@app.route('/api/products', methods=['GET'])
def get_products():
    products = load_products()
    logging.info('Список товаров отправлен пользователю')
    return jsonify(products)

#создание заказа
@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data or not all(key in data for key in ("product_id", "quantity", "customer_name")):
        logging.warning("Получен некорректный запрос на создание заказа")
        return jsonify({"error": "Некорректные данные"}), 400

    # Создание нового заказа
    order = {
        "id": len(load_orders()) + 1,
        "product_id": data["product_id"],
        "quantity": data["quantity"],
        "customer_name": data["customer_name"]
    }
    save_order(order)
    logging.info(f"Создан новый заказ: {order}")
    return jsonify(order), 201

if __name__ == '__main__':
    app.run(debug=True)
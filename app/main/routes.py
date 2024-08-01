from app.main import bp
from app.models.cart import Cart
from app.extensions import db
from flask import request
from app.util.app_util import generate_response
from app.middleware.auth import authenticate_token

@bp.before_request
@authenticate_token()
def before_request():
    pass

@bp.route("/", methods=["GET"])
def getCart():
    user_id = request.args.get('user_id')
    if user_id:
        cart_products = Cart.query.filter_by(user_id=user_id).all()
    else:
        cart_products = Cart.query.all()
    response = []
    for cartp in cart_products: response.append(cartp.toDict())

    # print(response)
    cart_total = 0
    for eachR in response:
        # print(eachR)
        cart_total += eachR['product_price']

    return generate_response(success=True, message="cart fetched", data={"cart_items":response, "cart_total": cart_total}), 200

@bp.route("/", methods=["POST"])
def addCart():
    try:
        req = request.get_json()
        new_cart = Cart(
            product_id = req['product_id'],
            product_details = req['product_details'],
            product_price = req['product_price'],
            user_id = req['user_id']
        )

        db.session.add(new_cart)
        db.session.commit()
        return generate_response(success=True, message="cart crated", data=new_cart.toDict()), 201
    except ValueError as e:
        return generate_response(success=False, message="something went wrong", errors=str(e)), 400

@bp.route("/<int:cart_id>", methods=["PUT"])
def updateCart(cart_id):
    try:
        cartD = Cart.query.get(cart_id)
        req = request.get_json()
        print(req)
        if 'product_id' in req:
            cartD.product_id = req['product_id']
        
        if 'product_details' in req:
            cartD.product_details = req['product_details']
        
        if 'product_price' in req:
            cartD.product_price = req['product_price']
        
        db.session.commit()

        # return f"updated cart with id {cartD.id}", 200
        return generate_response(success=True, message="cart updated", data=cartD.toDict()), 200
    except:
        # return "not found the cart id", 200
        return generate_response(success=False, message="cart id not found", errors={"id":cart_id}), 404

@bp.route("/<int:cart_id>", methods=["DELETE"])
def deleteCart(cart_id):
    Cart.query.filter_by(id=cart_id).delete()
    db.session.commit()

    return generate_response(success=True, message="cart deleted", data={"id":cart_id}), 200

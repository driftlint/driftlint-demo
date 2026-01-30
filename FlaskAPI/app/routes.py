from flask import Blueprint, jsonify, request


def _sum_items(items):
    total = 0
    for item in items:
        if not isinstance(item, dict):
            return None
        price_cents = item.get("price_cents")
        qty = item.get("qty")
        if not isinstance(price_cents, int) or not isinstance(qty, int) or qty <= 0:
            return None
        total += price_cents * qty
    return total
from .models import OrderStore

api = Blueprint("api", __name__)
store = OrderStore()


@api.get("/health")
def health():
    return jsonify({"status": "ok"})


@api.get("/orders")
def list_orders():
    return jsonify([
        {
            "id": order.id,
            "customer": order.customer,
            "total_cents": order.total_cents,
            "created_at": order.created_at.isoformat() + "Z",
        }
        for order in store.list_orders()
    ])


@api.post("/orders")
def create_order():
    payload = request.get_json(silent=True) or {}
    customer = payload.get("customer")
    total_cents = payload.get("total_cents")
    items = payload.get("items")

    if not customer or not isinstance(total_cents, int):
        return jsonify({"error": "customer and total_cents required"}), 400

    if items is not None:
        if not isinstance(items, list):
            return jsonify({"error": "items must be a list"}), 400
        items_total = _sum_items(items)
        if items_total is None:
            return jsonify({"error": "items must include price_cents and qty"}), 400
        if items_total != total_cents:
            return jsonify({"error": "total_cents must match sum of items"}), 400

    order = store.create_order(customer, total_cents)
    return (
        jsonify(
            {
                "id": order.id,
                "customer": order.customer,
                "total_cents": order.total_cents,
                "created_at": order.created_at.isoformat() + "Z",
            }
        ),
        201,
    )

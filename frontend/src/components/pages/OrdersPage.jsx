import React, { useEffect, useState } from "react";
import { api } from "../../lib/api";
import { money } from "../../utils/shopHelpers";
import { useAuth } from "../../context/AuthContext";

export function OrdersPage() {
  const { user } = useAuth();
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    if (!user) return;
    api.get("/orders").then((res) => setOrders(res.data));
  }, [user]);

  if (!user) {
    return <div className="notice">Please login to see your orders.</div>;
  }

  return (
    <div className="container section">
      <h1 className="shop-title">MY ORDERS</h1>

      {orders.length === 0 && <div className="notice">No orders yet.</div>}

      {orders.map((o) => (
        <div key={o.id} className="order">
          <div className="row">
            <strong>Status:</strong> {o.status}
          </div>
          <div className="row">
            <strong>Total:</strong> {money(o.total)}
          </div>
          <ul>
            {o.items.map((i, idx) => (
              <li key={idx}>
                {i.name} × {i.quantity}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

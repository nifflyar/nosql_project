import React, { useEffect, useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { Navigate } from "react-router-dom";
import { money } from "../../utils/shopHelpers";


export function AccountPage() {
    const { user, logout, api } = useAuth();
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get("/orders/my")
            .then((res) => setOrders(res.data))
            .finally(() => setLoading(false));
    }, [api]);

    if (!user) {
        return <div className="notice">Please login</div>;
    }

    return (
        <div className="section">
            <div className="container">
                <h2 className="h1">My Account</h2>

                <div className="account-card">
                    <h3>Profile</h3>
                    <p><b>Name:</b> {user.name}</p>
                    <p><b>Email:</b> {user.email}</p>
                    <p><b>Address:</b> {user.address}</p>
                </div>

                <div className="account-card">
                    <h3>My Orders</h3>

                    {orders.length === 0 ? (
                        <div className="notice">You have no orders yet.</div>
                    ) : (
                        orders.map((order) => (
                            <div key={order.id || order._id} className="order-card">
                                <div className="order-header">
                                    <div>
                                        <div className="order-id">
                                            Order #{(order.id || order._id).slice(-6)}
                                        </div>
                                        <div className="order-date">
                                            {new Date(order.created_at).toLocaleDateString()}
                                        </div>
                                    </div>

                                    <div className={`order-status ${order.status}`}>
                                        {order.status}
                                    </div>
                                </div>

                                <div className="order-items">
                                    {order.items.map((it, idx) => (
                                        <div key={idx} className="order-item">
                                            <div>
                                                <div className="order-item-name">{it.name}</div>
                                                <div className="order-item-variant">
                                                    {it.variant.size} / {it.variant.color}
                                                </div>
                                            </div>

                                            <div className="order-item-right">
                                                <div className="order-item-qty">× {it.quantity}</div>
                                                <div className="order-item-price">
                                                    {money(it.price * it.quantity)}
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>

                                <div className="order-footer">
                                    <span>Total</span>
                                    <strong>{money(order.total)}</strong>
                                </div>
                            </div>
                        ))
                    )}
                </div>


                <button className="btn ghost" onClick={logout}>
                    Logout
                </button>
            </div>
        </div>
    );
}

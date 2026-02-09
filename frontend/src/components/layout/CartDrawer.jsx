import React, { useMemo, useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { api } from "../../lib/api";
import { money } from "../../utils/shopHelpers";




export function CartDrawer({ open, onClose, items, setItems }) {
    const { user, fetchMe } = useAuth();
    const [busy, setBusy] = useState(false);
    const [msg, setMsg] = useState("");

    const total = useMemo(
        () => items.reduce((s, it) => s + Number(it.product.price) * it.qty, 0),
        [items]
    );

    const inc = (id) =>
        setItems((prev) =>
            prev.map((x) => (x.key === id ? { ...x, qty: x.qty + 1 } : x))
        );

    const dec = (id) =>
        setItems((prev) =>
            prev
                .map((x) =>
                    x.key === id ? { ...x, qty: Math.max(1, x.qty - 1) } : x
                )
                .filter((x) => x.qty > 0)
        );

    const remove = (id) =>
        setItems((prev) => prev.filter((x) => x.key !== id));

    const checkout = async () => {
        setMsg("");
        if (!user) {
            setMsg("Firstly enter your account to place an order.");
            return;
        }
        try {
            setBusy(true);

            const payload = {
                user_id: user.id || user._id,
                total,
                items: items.map((it) => ({
                    product_id: it.product.id || it.product._id,
                    name: it.product.name,
                    price: Number(it.product.price),
                    quantity: it.qty,
                    variant: {
                        size: it.variant.size,
                        color: it.variant.color,
                    },
                })),
            };

            await api.post("/orders", payload);
            setMsg("Order created");
            setItems([]);
            await fetchMe();
        } catch (e) {
            setMsg(e?.response?.data?.detail || "Order placement error");
        } finally {
            setBusy(false);
        }
    };

    if (!open) return null;

    return (
        <div className="drawer-backdrop" onClick={onClose}>
            <div className="drawer" onClick={(e) => e.stopPropagation()}>
                <div
                    style={{
                        display: "flex",
                        justifyContent: "space-between",
                        gap: 10,
                        alignItems: "center",
                    }}
                >
                    <h3>Cart</h3>
                    <button
                        className="iconbtn"
                        style={{ borderColor: "#ddd", color: "#222" }}
                        onClick={onClose}
                    >
                        Close
                    </button>
                </div>

                <div className="cartlist">
                    {items.length === 0 ? (
                        <div className="notice">Cart is empty.</div>
                    ) : (
                        items.map((it) => (
                            <div key={it.key} className="citem">
                                <div className="citem-top">
                                    <div>
                                        <div className="citem-title">{it.product.name}</div>
                                        <div className="citem-variant">
                                            {it.variant.size} / {it.variant.color}
                                        </div>
                                    </div>
                                    <button
                                        className="citem-remove"
                                        onClick={() => remove(it.key)}
                                    >
                                        Remove
                                    </button>
                                </div>

                                <div className="citem-bottom">
                                    <div className="qtyrow">
                                        <button
                                            className="qtybtn"
                                            onClick={() => dec(it.key)}
                                        >
                                            -
                                        </button>
                                        <div className="qtyvalue">{it.qty}</div>
                                        <button
                                            className="qtybtn"
                                            onClick={() => inc(it.key)}
                                        >
                                            +
                                        </button>
                                    </div>
                                    <div className="citem-price">
                                        {money(Number(it.product.price) * it.qty)}
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>

                <div className="hr" style={{ margin: "12px 0" }} />
                <div className="row" style={{ marginBottom: 10 }}>
                    <div
                        style={{
                            color: "#666",
                            letterSpacing: 2,
                            textTransform: "uppercase",
                            fontSize: 12,
                        }}
                    >
                        Total
                    </div>
                    <div
                        style={{
                            fontFamily: "var(--serif)",
                            fontSize: 26,
                        }}
                    >
                        {money(total)}
                    </div>
                </div>

                {msg ? (
                    <div className="error" style={{ marginBottom: 10 }}>
                        {msg}
                    </div>
                ) : null}

                <button
                    className="btn"
                    disabled={busy || items.length === 0}
                    onClick={checkout}
                >
                    {busy ? "Checking out..." : "Place order"}
                </button>

                <div
                    style={{
                        marginTop: 10,
                        color: "#777",
                        fontSize: 12,
                    }}
                >
                </div>
            </div>
        </div>
    );
}

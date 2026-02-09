import React, { useEffect, useMemo, useState } from "react";
import { AdminLayout } from "./AdminLayout";
import { api } from "../../lib/api";
import { money } from "../../utils/shopHelpers";

const ORDER_STATUSES = ["pending", "shipped", "delivered", "canceled"];

const statusColors = {
  pending: "#fbbf24",
  shipped: "#3b82f6",
  delivered: "#22c55e",
  canceled: "#ef4444",
};

export function AdminOrdersPage() {
  const [orders, setOrders] = useState([]);
  const [statusFilter, setStatusFilter] = useState("all");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");
  const [updating, setUpdating] = useState({});

  const extractErrorMessage = (e, fallback) => {
    const detail = e?.response?.data?.detail;
    console.log("Orders error detail:", detail);

    if (Array.isArray(detail)) {
      const msgs = detail
        .map((d) => {
          const loc = Array.isArray(d.loc) ? d.loc.join(" -> ") : d.loc;
          const msg = d.msg || "Validation error";
          return loc ? `${loc}: ${msg}` : msg;
        })
        .filter(Boolean);
      if (msgs.length > 0) return msgs.join("; ");
    }

    if (typeof detail === "string") return detail;
    return fallback;
  };

  const loadOrders = async () => {
    try {
      setLoading(true);
      setErr("");

      const res = await api.get("/orders/", {
        params: {
          skip: 0,
          limit: 100,
          status: statusFilter === "all" ? undefined : statusFilter,
        },
      });

      console.log("ADMIN orders:", res.data, Array.isArray(res.data));
      setOrders(Array.isArray(res.data) ? res.data : []);
    } catch (e) {
      console.error("Failed to load orders", e);
      const msg = extractErrorMessage(e, "Failed to load orders");
      setErr(msg);
      setOrders([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOrders();

  }, [statusFilter]);

  const visibleOrders = useMemo(() => {
    if (statusFilter === "all") return orders;
    return orders.filter((o) => o.status === statusFilter);
  }, [orders, statusFilter]);

  const handleStatusChange = async (order, newStatus) => {
    if (!newStatus || newStatus === order.status) return;

    const orderId = order._id || order.id;
    if (!orderId) return;

    try {
      setUpdating((u) => ({ ...u, [orderId]: true }));
      setErr("");

      await api.patch(`/orders/${orderId}/status`, {
        status: newStatus,
      });

      setOrders((prev) =>
        prev.map((o) =>
          (o._id || o.id) === orderId ? { ...o, status: newStatus } : o
        )
      );
    } catch (e) {
      console.error("Failed to update order status", e);
      const msg = extractErrorMessage(e, "Failed to update status");
      setErr(msg);
    } finally {
      setUpdating((u) => {
        const copy = { ...u };
        delete copy[orderId];
        return copy;
      });
    }
  };

  const formatDate = (iso) => {
    if (!iso) return "—";
    const d = new Date(iso);
    return d.toLocaleString();
  };

  const formatTotal = (total) => {
    const num = Number(total) || 0;
    return money(num);
  };

  return (
    <AdminLayout title="Orders">
      <div
        className="row"
        style={{
          marginBottom: 16,
          alignItems: "center",
          justifyContent: "space-between",
          gap: 12,
        }}
      >
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          {["all", ...ORDER_STATUSES].map((st) => {
            const isActive = st === statusFilter;
            const label =
              st === "all"
                ? "All"
                : st.charAt(0).toUpperCase() + st.slice(1);
            return (
              <button
                key={st}
                type="button"
                className="btn ghost"
                onClick={() => setStatusFilter(st)}
                style={{
                  padding: "4px 10px",
                  borderRadius: 999,
                  borderColor: isActive ? "#111" : "#ddd",
                  background: isActive ? "#111" : "transparent",
                  color: isActive ? "#fff" : "#111",
                  fontSize: 13,
                }}
              >
                {label}
              </button>
            );
          })}
        </div>

        <div>
          <button
            type="button"
            className="btn ghost"
            onClick={loadOrders}
            disabled={loading}
          >
            {loading ? "Refreshing..." : "Refresh"}
          </button>
        </div>
      </div>

      {err && (
        <div className="error" style={{ marginBottom: 12 }}>
          {err}
        </div>
      )}

      <table className="admin-table">
        <thead>
          <tr>
            <th style={{ width: "12%" }}>ID</th>
            <th style={{ width: "18%" }}>Customer</th>
            <th style={{ width: "20%" }}>Created</th>
            <th style={{ width: "15%" }}>Status</th>
            <th style={{ width: "15%" }}>Total</th>
            <th style={{ width: "20%" }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {visibleOrders.map((o, index) => {
            const id = o._id || o.id || `row-${index}`;
            const shortId = (o.id || o._id || "").toString().slice(-8);
            const status = o.status || "pending";
            const color = statusColors[status] || "#ddd";
            const isUpdating = !!updating[id];

            return (
              <tr key={id}>
                <td>
                  <code>{shortId || "—"}</code>
                </td>
                <td>{o.customer_name || "—"}</td>
                <td>{formatDate(o.created_at)}</td>
                <td>
                  <span
                    style={{
                      display: "inline-block",
                      padding: "2px 8px",
                      borderRadius: 999,
                      backgroundColor: color,
                      color: "#fff",
                      fontSize: 12,
                    }}
                  >
                    {status.charAt(0).toUpperCase() + status.slice(1)}
                  </span>
                </td>
                <td>{formatTotal(o.total)}</td>
                <td>
                  <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                    <select
                      className="select"
                      value={status}
                      onChange={(e) =>
                        handleStatusChange(o, e.target.value)
                      }
                      disabled={isUpdating}
                      style={{ maxWidth: 140 }}
                    >
                      {ORDER_STATUSES.map((st) => (
                        <option key={st} value={st}>
                          {st.charAt(0).toUpperCase() + st.slice(1)}
                        </option>
                      ))}
                    </select>
                    {isUpdating && (
                      <span style={{ fontSize: 12, color: "#555" }}>
                        Saving…
                      </span>
                    )}
                  </div>
                </td>
              </tr>
            );
          })}

          {visibleOrders.length === 0 && (
            <tr>
              <td colSpan={6} style={{ textAlign: "center", color: "#777" }}>
                No orders found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </AdminLayout>
  );
}

import React, { useEffect, useState } from "react";
import { AdminLayout } from "./AdminLayout";
import { api } from "../../lib/api";
import { money } from "../../utils/shopHelpers";

export function AdminStatsPage() {
  const [byCategory, setByCategory] = useState([]);
  const [topProducts, setTopProducts] = useState([]);

  useEffect(() => {
    async function load() {
      const [catRes, topRes] = await Promise.all([
        api.get("/stats/sales-by-category"),
        api.get("/stats/top-products"),
      ]);
      setByCategory(catRes.data);
      setTopProducts(topRes.data);
    }
    load();
  }, []);

  return (
    <AdminLayout title="Statistics">
      <h3 style={{ marginTop: 0, marginBottom: 10 }}>Sales by category</h3>
      <table className="admin-table" style={{ marginBottom: 30 }}>
        <thead>
          <tr>
            <th>Category</th>
            <th>Items</th>
            <th>Revenue</th>
          </tr>
        </thead>
        <tbody>
          {byCategory.map((c) => (
            <tr key={c.category_id}>
              <td>{c.category_name || c.category_id}</td>
              <td>{c.total_items}</td>
              <td>{money(c.total_revenue)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3 style={{ marginBottom: 10 }}>Top products</h3>
      <table className="admin-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Qty</th>
            <th>Revenue</th>
          </tr>
        </thead>
        <tbody>
          {topProducts.map((p) => (
            <tr key={p.product_id}>
              <td>{p.name || p.product_id}</td>
              <td>{p.total_quantity}</td>
              <td>{money(p.total_revenue)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </AdminLayout>
  );
}

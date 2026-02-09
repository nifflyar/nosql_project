import React, { useEffect, useState } from "react";
import { AdminLayout } from "./AdminLayout";
import { api } from "../../lib/api";

export function AdminDashboard() {
  const [stats, setStats] = useState({
    revenue: 0,
    orders: 0,
    topCategory: null,
  });

  useEffect(() => {
    async function load() {
      const [revRes, catRes] = await Promise.all([
        api.get("/stats/revenue-by-month"),
        api.get("/stats/sales-by-category"),
      ]);

      const totalRevenue = revRes.data.reduce(
        (s, row) => s + Number(row.total_revenue),
        0
      );

      setStats({
        revenue: totalRevenue,
        orders: revRes.data.reduce(
          (s, row) => s + Number(row.orders_count),
          0
        ),
        topCategory: catRes.data[0] || null,
      });
    }
    load();
  }, []);

  return (
    <AdminLayout title="Admin Panel">
      <div className="admin-grid">

        <div className="tile">
          <div className="tile-mid">
            <div className="admin-card">
              <div className="admin-card-currency">KZT</div>
              <div className="admin-card-value">
                {stats.revenue.toLocaleString()}
              </div>
              <p>Total revenue</p>
            </div>
          </div>
        </div>

        <div className="tile">
          <div className="tile-mid">
            <div className="admin-card">
              <div className="admin-card-value">
                {stats.orders}
              </div>
              <p>Orders</p>
            </div>
          </div>
        </div>

        <div className="tile">
          <div className="tile-mid">
            <div className="admin-card">
              <div className="admin-card-value">
                {stats.topCategory?.category_name || "-"}
              </div>
              <p>Top category</p>
            </div>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
}

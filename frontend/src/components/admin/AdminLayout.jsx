import React from "react";
import { NavLink } from "react-router-dom";

export function AdminLayout({ title, children }) {
    return (
        <div className="section">
            <div className="container">
                <h1 className="h1" style={{ marginBottom: 24 }}>
                    {title}
                </h1>

            
                <div className="admin-tabs">
                    <NavLink to="/admin" end>
                        Overview
                    </NavLink>
                    <NavLink to="/admin/products">
                        Products
                    </NavLink>
                    <NavLink to="/admin/orders">
                        Orders
                    </NavLink>
                    <NavLink to="/admin/stats">
                        Statistics
                    </NavLink>
                </div>


                <div className="admin-card">{children}</div>
            </div>
        </div>
    );
}

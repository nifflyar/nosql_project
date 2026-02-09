import React, { useMemo, useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import { AuthProvider } from "./context/AuthContext";

import { TopBar } from "./components/layout/TopBar";
import { Footer } from "./components/layout/Footer";
import { CartDrawer } from "./components/layout/CartDrawer";

import { HomePage } from "./components/pages/HomePage";
import { ShopPage } from "./components/pages/ShopPage";
import { SalePage } from "./components/pages/SalePage";
import { OrdersPage } from "./components/pages/OrdersPage";
import { LoginPage } from "./components/pages/LoginPage";
import { SignupPage } from "./components/pages/SignupPage";
import { AccountPage } from "./components/pages/AccountPage";


import { AdminOrdersPage } from "./components/admin/AdminOrdersPage";
import { AdminDashboard } from "./components/admin/AdminDashboard";
import { AdminProductsPage } from "./components/admin/AdminProductsPage";
import { AdminStatsPage } from "./components/admin/AdminStatsPage";



function AppShell() {
  const [cartOpen, setCartOpen] = useState(false);
  const [cart, setCart] = useState([]);
  const { user } = useAuth();

  const cartCount = useMemo(
    () => cart.reduce((s, it) => s + it.qty, 0),
    [cart]
  );

  const addToCart = (item) => {
    setCart((prev) => {
      const found = prev.find((x) => x.key === item.key);
      if (found) {
        return prev.map((x) =>
          x.key === item.key ? { ...x, qty: x.qty + 1 } : x
        );
      }
      return [...prev, item];
    });
    setCartOpen(true);
  };

  function PrivateRoute({ children }) {
    const { user, loading } = useAuth();

    if (loading) {
      return (
        <div className="section">
          <div className="container">
            <div className="notice">Loading...</div>
          </div>
        </div>
      );
    }

    return user ? children : <Navigate to="/login" replace />;
  }

  function AdminRoute({ children }) {
    const { user, loading } = useAuth();

    if (loading) {
      return (
        <div className="section">
          <div className="container">
            <div className="notice">Loading...</div>
          </div>
        </div>
      );
    }

    if (!user) {
      return <Navigate to="/login" replace />;
    }

    if (user.role !== "admin") {
      return <Navigate to="/" replace />;
    }

    return children;
  }


  return (
    <>
      <TopBar
        cartCount={cartCount}
        onCartOpen={() => setCartOpen(true)}
      />
      <CartDrawer
        open={cartOpen}
        onClose={() => setCartOpen(false)}
        items={cart}
        setItems={setCart}
      />

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/shop" element={<ShopPage onAddToCart={addToCart} />} />
        <Route path="/sale" element={<SalePage onAddToCart={addToCart} />} />
        <Route path="/orders" element={<OrdersPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route
          path="*"
          element={
            <div className="section">
              <div className="container">
                <div className="notice">Page not found.</div>
              </div>
            </div>
          }
        />
        <Route
          path="/account"
          element={
            <PrivateRoute>
              <AccountPage />
            </PrivateRoute>
          }
        />

        <Route
          path="/admin"
          element={
            <AdminRoute>
              <AdminDashboard />
            </AdminRoute>
          }
        />
        <Route
          path="/admin/products"
          element={
            <AdminRoute>
              <AdminProductsPage />
            </AdminRoute>
          }
        />
        <Route
          path="/admin/stats"
          element={
            <AdminRoute>
              <AdminStatsPage />
            </AdminRoute>
          }
        />

        <Route
          path="/admin/orders"
          element={
            <AdminRoute>
              <AdminOrdersPage />
            </AdminRoute>
          }
        />

      </Routes>


      <Footer />
    </>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppShell />
      </BrowserRouter>
    </AuthProvider>
  );
}

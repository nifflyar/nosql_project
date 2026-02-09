import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";

import './styles/base.css';
import './styles/header.css';
import './styles/hero.css';
import './styles/sections.css';
import './styles/shop.css';
import './styles/auth.css';
import './styles/cart.css';
import './styles/orders.css';
import './styles/footer.css';
import './styles/admin.css';


ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

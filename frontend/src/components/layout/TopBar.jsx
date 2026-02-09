import React from "react";
import { Link, NavLink } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export function TopBar({ cartCount, onCartOpen }) {
    const { user, logout } = useAuth();

    const nav = [
        { to: "/", label: "MAIN MENU" },
        { to: "/shop", label: "SHOP" },
    ];

    return (
        <>
            <div className="topbar">
                <div className="container topbar-inner">
                    <Link to="/" className="brand">
                        SWAGSTORE
                    </Link>

                    <nav className="nav">
                        {nav.map((n) => (
                            <NavLink key={n.to} to={n.to} end={n.to === "/"}>
                                {n.label}
                            </NavLink>
                        ))}
                    </nav>

                    <div className="actions">
                        {user ? (
                            <>
                                <Link className="iconbtn" to="/account">
                                    {user.name}
                                </Link>
                                <button className="iconbtn" onClick={onCartOpen}>
                                    Cart <span className="badge">{cartCount}</span>
                                </button>
                                {user?.role === "admin" && (
                                    <Link className="iconbtn" to="/admin">
                                        Admin
                                    </Link>
                                )}
                                <button className="iconbtn" onClick={logout}>
                                    Logout
                                </button>
                            </>
                        ) : (
                            <>
                                <Link className="iconbtn" to="/login">
                                    Login
                                </Link>
                                <button className="iconbtn" onClick={onCartOpen}>
                                    Cart <span className="badge">{cartCount}</span>
                                </button>
                            </>
                        )}
                    </div>
                </div>
            </div>

            <div className="subbar">
                <div className="container">
                    <div className="msg">FREE SHIPPING IN KAZAKHSTAN</div>
                </div>
            </div>
        </>
    );
}

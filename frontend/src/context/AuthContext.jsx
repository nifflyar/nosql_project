import React, { createContext, useContext, useEffect, useState } from "react";
import { api } from "../lib/api";

const AuthCtx = createContext(null);

export function useAuth() {
    const ctx = useContext(AuthCtx);
    if (!ctx) throw new Error("useAuth must be used within AuthProvider");
    return ctx;
}

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [err, setErr] = useState("");

    const fetchMe = async () => {
        try {
            const res = await api.get("/auth/me");
            setUser(res.data);
            return res.data;
        } catch {
            setUser(null);
            return null;
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchMe();
    }, []);

    const login = async (email, password) => {
        setErr("");
        await api.post("/auth/login", { email, password });
        await fetchMe();
    };

    const register = async (payload) => {
        setErr("");
        await api.post("/auth/register", payload);
        await api.post("/auth/login", { email: payload.email, password: payload.password });
        await fetchMe();
    };

    const logout = async () => {
        setErr("");
        await api.post("/auth/logout");
        setUser(null);
    };

    const value = {
        user,
        loading,
        err,
        setErr,
        login,
        register,
        logout,
        fetchMe,
        api,
    };

    return <AuthCtx.Provider value={value}>{children}</AuthCtx.Provider>;

}

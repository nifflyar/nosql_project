import React, { useEffect, useMemo, useState } from "react";
import { api } from "../../lib/api";
import { fakeImg, money, pickFirstVariant } from "../../utils/shopHelpers";

export function ShopPage({ onAddToCart }) {
  const [products, setProducts] = useState([]);
  const [cats, setCats] = useState([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  const [categoryId, setCategoryId] = useState("");
  const [size, setSize] = useState("");
  const [color, setColor] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");

  const [q, setQ] = useState("");

  const SIZES = ["XS", "S", "M", "L", "XL"];
  const COLORS = [
    "black",
    "white",
    "beige",
    "gray",
    "brown",
    "red",
    "blue",
    "green",
    "pink",
  ];

  const load = async () => {
    try {
      setErr("");
      setLoading(true);

      const min = minPrice.trim();
      const max = maxPrice.trim();

      if (min && Number.isNaN(Number(min))) {
        setErr("Min price must be a number");
        setLoading(false);
        return;
      }

      if (max && Number.isNaN(Number(max))) {
        setErr("Max price must be a number");
        setLoading(false);
        return;
      }

      const minParam = min ? Number(min) : undefined;
      const maxParam = max ? Number(max) : undefined;

      const [cRes, pRes] = await Promise.all([
        api.get("/categories", { params: { skip: 0, limit: 100 } }),
        api.get("/products", {
          params: {
            skip: 0,
            limit: 100,
            category_id: categoryId || undefined,
            size: size || undefined,
            color: color || undefined,
            min_price: minParam,
            max_price: maxParam,
          },
        }),
      ]);

      setCats(cRes.data || []);
      setProducts(pRes.data || []);
    } catch (e) {
      const detail = e?.response?.data?.detail;

      if (Array.isArray(detail)) {
        const msg = detail
          .map((d) =>
            typeof d === "string"
              ? d
              : d?.msg || JSON.stringify(d)
          )
          .join("; ");
        setErr(msg || "Failed to load products");
      } else if (typeof detail === "string") {
        setErr(detail);
      } else {
        setErr("Failed to load products");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const visibleProducts = useMemo(() => {
    if (!q.trim()) return products;
    const qLower = q.toLowerCase();
    return products.filter((p) =>
      (p.name || "").toLowerCase().includes(qLower)
    );
  }, [products, q]);

  return (
    <>
      <div className="shop-head">
        <div className="container">
          <h1 className="shop-title">SHOP</h1>
        </div>
      </div>

      <div className="container">
        <div className="filters">
          <input
            className="input"
            style={{ minWidth: 220 }}
            placeholder="Search by name…"
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />

          <select
            className="select"
            value={categoryId}
            onChange={(e) => setCategoryId(e.target.value)}
          >
            <option value="">All categories</option>
            {cats.map((c) => (
              <option key={c.id || c._id} value={c.id || c._id}>
                {c.name}
              </option>
            ))}
          </select>

          <select
            className="select"
            value={size}
            onChange={(e) => setSize(e.target.value)}
          >
            <option value="">Size (S/M/L)</option>
            {SIZES.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>

          <select
            className="select"
            value={color}
            onChange={(e) => setColor(e.target.value)}
          >
            <option value="">Color</option>
            {COLORS.map((c) => (
              <option key={c} value={c}>
                {c.charAt(0).toUpperCase() + c.slice(1)}
              </option>
            ))}
          </select>

          <input
            className="input"
            value={minPrice}
            onChange={(e) => setMinPrice(e.target.value)}
            placeholder="Min price"
          />
          <input
            className="input"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
            placeholder="Max price"
          />

          <button className="btn" onClick={load} disabled={loading}>
            {loading ? "..." : "Filter"}
          </button>
          <button
            className="btn ghost"
            onClick={() => {
              setCategoryId("");
              setSize("");
              setColor("");
              setMinPrice("");
              setMaxPrice("");
              setQ("");
              setTimeout(load, 0);
            }}
          >
            Reset
          </button>
        </div>

        {err ? <div className="error">{err}</div> : null}

        <div className="grid">
          {visibleProducts.map((p) => {
            const id = p.id || p._id;
            const img = p.image_url || fakeImg(p.name);
            const v = pickFirstVariant(p);

            return (
              <div key={id} className="pcard">
                <div
                  className="pimg"
                  style={{ backgroundImage: `url("${img}")` }}
                />
                <div className="pbody">
                  <p className="pname">{p.name}</p>
                  <p className="price">{money(p.price)}</p>
                  <p className="small">
                    Variant: {v.size} / {v.color} (stock: {v.stock})
                  </p>

                  <button
                    className="pbtn"
                    onClick={() =>
                      onAddToCart({
                        key: `${id}-${v.size}-${v.color}`,
                        product: p,
                        variant: v,
                        qty: 1,
                      })
                    }
                  >
                    Add to cart
                  </button>
                </div>
              </div>
            );
          })}

          {visibleProducts.length === 0 && !loading && !err && (
            <p
              style={{
                gridColumn: "1 / -1",
                textAlign: "center",
                color: "#777",
              }}
            >
              No products found.
            </p>
          )}
        </div>
      </div>
    </>
  );
}

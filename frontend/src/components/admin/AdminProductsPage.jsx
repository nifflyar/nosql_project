import React, { useEffect, useMemo, useState } from "react";
import { AdminLayout } from "./AdminLayout";
import { api } from "../../lib/api";
import { money } from "../../utils/shopHelpers";


const SIZE_OPTIONS = ["XS", "S", "M", "L", "XL", "XXL"];
const COLOR_OPTIONS = [
  "Black",
  "White",
  "Red",
  "Blue",
  "Green",
  "Yellow",
  "Gray",
  "Brown",
];

export function AdminProductsPage() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);

  const [mode, setMode] = useState("none");

  const [form, setForm] = useState({
    id: null,
    name: "",
    description: "",
    price: "",
    category_id: "",
    image_url: "",
    variants: [], // { size, color, stock }
  });

  const [filters, setFilters] = useState({
    q: "",
    category_id: "",
    minPrice: "",
    maxPrice: "",
  });

  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");
  const [loadError, setLoadError] = useState("");

  const extractErrorMessage = (e, fallback) => {
    const detail = e?.response?.data?.detail;
    console.log("Server validation detail:", detail);

    if (Array.isArray(detail)) {
      const msgs = detail
        .map((d) => {
          const loc = Array.isArray(d.loc) ? d.loc.join(" -> ") : d.loc;
          const msg = d.msg || "Validation error";
          return loc ? `${loc}: ${msg}` : msg;
        })
        .filter(Boolean);
      if (msgs.length > 0) {
        return msgs.join("; ");
      }
    }

    if (typeof detail === "string") {
      return detail;
    }

    return fallback;
  };

  const isValidUrl = (value) => {
    try {
      const trimmed = value.trim();
      if (!trimmed.startsWith("http://") && !trimmed.startsWith("https://")) {
        return false;
      }
      new URL(trimmed);
      return true;
    } catch {
      return false;
    }
  };

  const loadProducts = async () => {
    try {
      setLoadError("");
      const res = await api.get("/products/", {
        params: { skip: 0, limit: 100 },
      });
      console.log("ADMIN products:", res.data, Array.isArray(res.data));
      setProducts(Array.isArray(res.data) ? res.data : []);
    } catch (e) {
      console.error("Failed to load products", e);
      const msg = extractErrorMessage(
        e,
        "Failed to load products from backend"
      );
      setLoadError(msg);
      setProducts([]);
    }
  };

  const loadCategories = async () => {
    try {
      const res = await api.get("/categories/", {
        params: { skip: 0, limit: 100 },
      });
      console.log("ADMIN categories:", res.data, Array.isArray(res.data));
      setCategories(Array.isArray(res.data) ? res.data : []);
    } catch (e) {
      console.error("Failed to load categories", e);
      setCategories([]);
    }
  };

  useEffect(() => {
    loadProducts();
    loadCategories();
  }, []);

  const resetForm = () =>
    setForm({
      id: null,
      name: "",
      description: "",
      price: "",
      category_id: "",
      image_url: "",
      variants: [],
    });

  const openCreate = () => {
    resetForm();
    setErr("");
    setMode("create");
  };

  const openEdit = (p) => {
    setForm({
      id: p.id || p._id,
      name: p.name || "",
      description: p.description || "",
      price: p.price ?? "",
      category_id: p.category_id || "",
      image_url: p.image_url || "",
      variants: Array.isArray(p.variants)
        ? p.variants.map((v) => ({
            size: v.size || "",
            color: v.color || "",
            stock: v.stock ?? 0,
          }))
        : [],
    });
    setErr("");
    setMode("edit");
  };

  const closeForm = () => {
    resetForm();
    setMode("none");
  };

  const handleFormChange = (field) => (e) => {
    const value = e.target.value;
    setForm((f) => ({ ...f, [field]: value }));
  };

  const handleFilterChange = (field) => (e) => {
    const value = e.target.value;
    setFilters((f) => ({ ...f, [field]: value }));
  };

  const getCategoryName = (id) => {
    if (!id) return "—";
    const idStr = String(id);
    const cat = categories.find((c) => String(c.id || c._id) === idStr);
    return cat ? cat.name : idStr;
  };

  const addVariant = () => {
    setForm((f) => ({
      ...f,
      variants: [...f.variants, { size: "", color: "", stock: 0 }],
    }));
  };

  const removeVariant = (index) => {
    setForm((f) => ({
      ...f,
      variants: f.variants.filter((_, i) => i !== index),
    }));
  };

  const updateVariant = (index, field, value) => {
    setForm((f) => ({
      ...f,
      variants: f.variants.map((v, i) =>
        i === index ? { ...v, [field]: value } : v
      ),
    }));
  };

  const visibleProducts = useMemo(() => {
    return products.filter((p) => {
      const price = Number(p.price) || 0;

      const productName = (p.name || "").toLowerCase();
      if (filters.q && !productName.includes(filters.q.toLowerCase())) {
        return false;
      }

      const productCategoryId =
        p.category_id != null ? String(p.category_id) : "";
      const filterCategoryId =
        filters.category_id != null ? String(filters.category_id) : "";

      if (filterCategoryId && productCategoryId !== filterCategoryId) {
        return false;
      }

      if (filters.minPrice && price < Number(filters.minPrice)) {
        return false;
      }

      if (filters.maxPrice && price > Number(filters.maxPrice)) {
        return false;
      }

      return true;
    });
  }, [products, filters]);

  const submit = async (e) => {
    e.preventDefault();
    setErr("");

    if (!form.name.trim()) {
      setErr("Name is required");
      return;
    }

    if (!form.price || Number(form.price) <= 0) {
      setErr("Price must be greater than 0");
      return;
    }

    if (!form.description.trim()) {
      setErr("Description is required");
      return;
    }

    if (!form.image_url.trim()) {
      setErr("Image URL is required");
      return;
    }

    if (!isValidUrl(form.image_url)) {
      setErr("Image URL must be a valid URL starting with http:// or https://");
      return;
    }

    if (!form.category_id) {
      setErr("Category is required");
      return;
    }

    if (!form.variants || form.variants.length === 0) {
      setErr("At least one variant is required");
      return;
    }

    for (let i = 0; i < form.variants.length; i++) {
      const v = form.variants[i];
      if (!v.size) {
        setErr(`Variant #${i + 1}: size is required`);
        return;
      }
      if (!v.color) {
        setErr(`Variant #${i + 1}: color is required`);
        return;
      }
      if (
        v.stock === "" ||
        v.stock == null ||
        Number.isNaN(Number(v.stock))
      ) {
        setErr(`Variant #${i + 1}: stock is required`);
        return;
      }
      if (Number(v.stock) < 0) {
        setErr(`Variant #${i + 1}: stock cannot be negative`);
        return;
      }
    }

    try {
      setLoading(true);

      const payload = {
        name: form.name.trim(),
        description: form.description.trim(),
        image_url: form.image_url.trim(),
        price: Number(form.price),
        category_id: form.category_id,
        variants: form.variants.map((v) => ({
          stock: Number(v.stock),
          size: v.size,
          color: v.color,
        })),
      };

      if (form.id && mode === "edit") {
        await api.patch(`/products/${form.id}`, payload);
      } else {
        await api.post("/products/", payload);
      }

      await loadProducts();
      closeForm();
    } catch (e2) {
      console.error("Save product error", e2);
      const msg = extractErrorMessage(e2, "Error saving product");
      setErr(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AdminLayout title="Products">
      <div
        className="row"
        style={{
          marginBottom: 16,
          alignItems: "flex-end",
          gap: 12,
          justifyContent: "space-between",
        }}
      >
        <div style={{ flex: 3 }}>
          <div className="label">Search</div>
          <input
            className="input"
            placeholder="Name contains…"
            value={filters.q}
            onChange={handleFilterChange("q")}
          />
        </div>

        <div style={{ flex: 2 }}>
          <div className="label">Category</div>
          <select
            className="select"
            value={filters.category_id}
            onChange={handleFilterChange("category_id")}
          >
            <option value="">All categories</option>
            {categories.map((c) => (
              <option key={c.id || c._id} value={c.id || c._id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>

        <div style={{ flex: 1 }}>
          <div className="label">Min price</div>
          <input
            className="input"
            type="number"
            min="0"
            step="0.01"
            value={filters.minPrice}
            onChange={handleFilterChange("minPrice")}
          />
        </div>

        <div style={{ flex: 1 }}>
          <div className="label">Max price</div>
          <input
            className="input"
            type="number"
            min="0"
            step="0.01"
            value={filters.maxPrice}
            onChange={handleFilterChange("maxPrice")}
          />
        </div>

        <div style={{ flexShrink: 0 }}>
          <button
            type="button"
            className="btn ghost"
            onClick={() =>
              setFilters({ q: "", category_id: "", minPrice: "", maxPrice: "" })
            }
            style={{ marginRight: 8 }}
          >
            Reset filters
          </button>
          <button type="button" className="btn" onClick={openCreate}>
            Create product
          </button>
        </div>
      </div>

      {loadError && (
        <div className="error" style={{ marginBottom: 16 }}>
          {loadError}
        </div>
      )}

      {mode !== "none" && (
        <div
          className="card"
          style={{ marginBottom: 24, padding: 20, maxWidth: 900 }}
        >
          <h3 style={{ marginTop: 0, marginBottom: 12 }}>
            {mode === "edit" ? "Edit product" : "Create product"}
          </h3>

          <form className="form" onSubmit={submit}>
            <div className="row" style={{ gap: 16 }}>
              <div style={{ flex: 2 }}>
                <div className="label">Name</div>
                <input
                  className="input"
                  value={form.name}
                  onChange={handleFormChange("name")}
                  required
                />
              </div>

              <div style={{ flex: 1 }}>
                <div className="label">Price</div>
                <input
                  className="input"
                  type="number"
                  min="0"
                  step="0.01"
                  value={form.price}
                  onChange={handleFormChange("price")}
                  required
                />
              </div>

              <div style={{ flex: 1 }}>
                <div className="label">Category</div>
                {categories.length > 0 ? (
                  <select
                    className="select"
                    value={form.category_id}
                    onChange={handleFormChange("category_id")}
                    required
                  >
                    <option value="">Select category</option>
                    {categories.map((c) => (
                      <option key={c.id || c._id} value={c.id || c._id}>
                        {c.name}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    className="input"
                    value={form.category_id}
                    onChange={handleFormChange("category_id")}
                    placeholder="Category ID"
                    required
                  />
                )}
              </div>
            </div>

            <div style={{ marginTop: 12 }}>
              <div className="label">Description</div>
              <textarea
                className="input"
                style={{ minHeight: 60, resize: "vertical" }}
                value={form.description}
                onChange={handleFormChange("description")}
                placeholder="Short description of the product"
                required
              />
            </div>

            <div style={{ marginTop: 12 }}>
              <div className="label">Image URL</div>
              <input
                className="input"
                value={form.image_url}
                onChange={handleFormChange("image_url")}
                placeholder="https://…"
                required
              />
            </div>

            <div style={{ marginTop: 16 }}>
              <div className="label">Variants</div>

              {form.variants.length === 0 && (
                <div style={{ fontSize: 12, color: "#777", marginBottom: 6 }}>
                  At least one variant is required.
                </div>
              )}

              {form.variants.map((v, index) => {
                const sizeOptions =
                  v.size && !SIZE_OPTIONS.includes(v.size)
                    ? [v.size, ...SIZE_OPTIONS]
                    : SIZE_OPTIONS;

                const colorOptions =
                  v.color && !COLOR_OPTIONS.includes(v.color)
                    ? [v.color, ...COLOR_OPTIONS]
                    : COLOR_OPTIONS;

                return (
                  <div
                    key={index}
                    className="row"
                    style={{
                      gap: 12,
                      marginBottom: 8,
                      alignItems: "flex-end",
                    }}
                  >
                    <div style={{ flex: 1 }}>
                      <div className="label">Size</div>
                      <select
                        className="select"
                        value={v.size || ""}
                        onChange={(e) =>
                          updateVariant(index, "size", e.target.value)
                        }
                        required
                      >
                        <option value="">Select size</option>
                        {sizeOptions.map((s) => (
                          <option key={s} value={s}>
                            {s}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div style={{ flex: 1 }}>
                      <div className="label">Color</div>
                      <select
                        className="select"
                        value={v.color || ""}
                        onChange={(e) =>
                          updateVariant(index, "color", e.target.value)
                        }
                        required
                      >
                        <option value="">Select color</option>
                        {colorOptions.map((c) => (
                          <option key={c} value={c}>
                            {c}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div style={{ flex: 1 }}>
                      <div className="label">Stock</div>
                      <input
                        className="input"
                        type="number"
                        min="0"
                        value={v.stock}
                        onChange={(e) =>
                          updateVariant(
                            index,
                            "stock",
                            e.target.value === ""
                              ? ""
                              : Number(e.target.value)
                          )
                        }
                        required
                      />
                    </div>

                    <button
                      type="button"
                      className="btn ghost"
                      onClick={() => removeVariant(index)}
                    >
                      ✕
                    </button>
                  </div>
                );
              })}

              <button
                type="button"
                className="btn ghost"
                onClick={addVariant}
              >
                + Add variant
              </button>
            </div>

            {err && (
              <div className="error" style={{ marginTop: 10 }}>
                {err}
              </div>
            )}

            <div style={{ marginTop: 12 }}>
              <button className="btn" type="submit" disabled={loading}>
                {loading
                  ? "Saving..."
                  : mode === "edit"
                  ? "Update product"
                  : "Create product"}
              </button>
              <button
                type="button"
                className="btn ghost"
                style={{ marginLeft: 8 }}
                onClick={closeForm}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <table className="admin-table">
        <thead>
          <tr>
            <th style={{ width: "24%" }}>Name</th>
            <th style={{ width: "12%" }}>Price</th>
            <th style={{ width: "18%" }}>Category</th>
            <th style={{ width: "18%" }}>Variants</th>
            <th style={{ width: "14%" }}>Image</th>
            <th style={{ width: "10%" }}>Created</th>
            <th style={{ width: "4%" }}></th>
          </tr>
        </thead>
        <tbody>
          {visibleProducts.map((p) => (
            <tr key={p.id || p._id}>
              <td>{p.name}</td>
              <td>{money(Number(p.price) || 0)}</td>
              <td>{getCategoryName(p.category_id)}</td>
              <td style={{ fontSize: 12 }}>
                {Array.isArray(p.variants) && p.variants.length > 0 ? (
                  p.variants.map((v, i) => (
                    <div key={i}>
                      {v.size && <strong>{v.size}</strong>}{" "}
                      {v.color && <span>({v.color})</span>} – stock: {v.stock}
                    </div>
                  ))
                ) : (
                  <span style={{ color: "#999" }}>no variants</span>
                )}
              </td>
              <td>
                {p.image_url ? (
                  <img
                    src={p.image_url}
                    alt={p.name}
                    style={{
                      maxWidth: 80,
                      maxHeight: 60,
                      objectFit: "cover",
                      borderRadius: 2,
                    }}
                  />
                ) : (
                  <span style={{ color: "#999", fontSize: 12 }}>no image</span>
                )}
              </td>
              <td>
                {p.created_at
                  ? new Date(p.created_at).toLocaleDateString()
                  : "—"}
              </td>
              <td>
                <button
                  className="btn ghost"
                  style={{ marginRight: 6 }}
                  onClick={() => openEdit(p)}
                >
                  Edit
                </button>
                <button
                  className="btn ghost"
                  onClick={() => {
                    if (window.confirm("Delete this product?")) {
                      api
                        .delete(`/products/${p.id || p._id}`)
                        .then(loadProducts)
                        .catch((e) => {
                          console.error("Failed to delete product", e);
                          alert(
                            extractErrorMessage(
                              e,
                              "Failed to delete product"
                            )
                          );
                        });
                    }
                  }}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}

          {visibleProducts.length === 0 && (
            <tr>
              <td colSpan={7} style={{ textAlign: "center", color: "#777" }}>
                No products found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </AdminLayout>
  );
}

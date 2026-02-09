export function money(v) {
  const n = Number(v || 0);
  return new Intl.NumberFormat("kk-KZ", {
    style: "currency",
    currency: "KZT",
  }).format(n);
}

export function pickFirstVariant(product) {
  const v = product?.variants?.[0];
  if (!v) return { size: "M", color: "black", stock: 1 };
  return { size: v.size, color: v.color, stock: v.stock };
}

function pickUnsplash(seed = "") {
  const ids = [
    "photo-1520975958225-9f31e85f7f34",
    "photo-1520975682085-31be9f39a3c1",
    "photo-1520975751880-2aa1d7f6f2ef",
    "photo-1520976018518-7b1a8cd3a2c9",
    "photo-1520975851399-2ea4c6be9f87",
  ];
  let h = 0;
  for (let i = 0; i < seed.length; i++) {
    h = (h * 31 + seed.charCodeAt(i)) >>> 0;
  }
  return ids[h % ids.length];
}

export function fakeImg(seed) {
  const id = pickUnsplash(seed || "fashion");
  return `https://images.unsplash.com/${id}?auto=format&fit=crop&w=900&q=70`;
}

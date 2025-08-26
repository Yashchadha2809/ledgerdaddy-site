// lib/shopify.ts
export const SHOP_DOMAIN = process.env.NEXT_PUBLIC_SHOPIFY_STORE_DOMAIN!;
export const SF_TOKEN   = process.env.NEXT_PUBLIC_SHOPIFY_STOREFRONT_TOKEN!;
export const API_VER    = process.env.NEXT_PUBLIC_SHOPIFY_API_VERSION!;

export async function sf<T>(
  query: string,
  variables?: Record<string, any>
): Promise<T> {
  const res = await fetch(`https://${SHOP_DOMAIN}/api/${API_VER}/graphql.json`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Shopify-Storefront-Access-Token": SF_TOKEN,
    },
    body: JSON.stringify({ query, variables }),
    // cache a bit for speed; remove if you want fully dynamic
    next: { revalidate: 60 },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Shopify error ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

// app/shop/page.tsx
import Link from "next/link";
import { sf } from "../../lib/shopify";

// Server component with search + pagination via URL params
export default async function Shop({
  searchParams,
}: {
  searchParams?: { q?: string; after?: string };
}) {
  const q = (searchParams?.q || "").trim();
  const after = searchParams?.after || null;

  // Build Shopify search query (optional)
  // You can enhance this later (tags, vendor, etc.)
  const query = q ? `title:*${q}*` : undefined;

  const { data }: any = await sf(
    `
    query Products($first: Int!, $after: String, $query: String) {
      products(first: $first, after: $after, query: $query, sortKey: UPDATED_AT) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          title
          handle
          featuredImage { url altText }
          variants(first: 1) {
            nodes {
              id
              availableForSale
              price { amount currencyCode }
            }
          }
        }
      }
    }
  `,
    { first: 24, after, query }
  );

  const conn = data?.products;
  const products = conn?.nodes ?? [];
  const hasNext = conn?.pageInfo?.hasNextPage;
  const endCursor = conn?.pageInfo?.endCursor;

  return (
    <main className="max-w-6xl mx-auto p-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-5">
        <h1 className="text-2xl font-bold">Shop</h1>

        {/* Search (GET -> /shop?q=...) */}
        <form className="flex gap-2" action="/shop" method="get">
          <input
            type="text"
            name="q"
            defaultValue={q}
            placeholder="Search products..."
            className="border rounded-lg px-3 py-2 w-64"
          />
          <button className="rounded-lg px-4 py-2 bg-black text-white">
            Search
          </button>
        </form>
      </div>

      {/* Grid */}
      {products.length === 0 ? (
        <div className="text-sm opacity-70">No products found.</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((p: any) => {
            const v = p.variants?.nodes?.[0];
            return (
              <Link
                key={p.id}
                href={`/products/${p.handle}`}
                className="border rounded-xl p-4 shadow-sm block hover:shadow-md transition"
              >
                <img
                  src={p.featuredImage?.url || "/placeholder.png"}
                  alt={p.featuredImage?.altText || p.title}
                  className="w-full h-56 object-cover rounded-lg border"
                />
                <div className="mt-3 flex items-center justify-between">
                  <h2 className="font-semibold">{p.title}</h2>
                  {v?.price && (
                    <span className="text-sm opacity-70">
                      {v.price.amount} {v.price.currencyCode}
                    </span>
                  )}
                </div>
                {v?.availableForSale === false && (
                  <div className="mt-1 text-xs text-red-600">Out of stock</div>
                )}
                <div className="mt-2 text-sm text-gray-500">View details →</div>
              </Link>
            );
          })}
        </div>
      )}

      {/* Load more */}
      {hasNext && (
        <div className="mt-8 flex justify-center">
          <Link
            href={{
              pathname: "/shop",
              query: { ...(q ? { q } : {}), after: endCursor },
            }}
            className="rounded-lg px-5 py-2 border"
          >
            Load more
          </Link>
        </div>
      )}
    </main>
  );
}

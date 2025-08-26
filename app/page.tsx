// app/page.tsx
import { sf } from "../lib/shopify";

export default async function Home() {
  const { data }: any = await sf(`
    query Products {
      products(first: 12, sortKey: UPDATED_AT) {
        nodes {
          id
          title
          handle
          featuredImage { url altText }
          variants(first: 1) { nodes { id price { amount currencyCode } } }
        }
      }
    }
  `);

  const products = data?.products?.nodes ?? [];

  return (
    <main className="max-w-6xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Latest Products</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {products.map((p: any) => {
          const price = p.variants.nodes[0]?.price;
          return (
            <a
              key={p.id}
              href={`/products/${p.handle}`}
              className="border rounded-xl p-4 shadow-sm block hover:shadow-md transition"
            >
              {/* using <img> so you don't need next/image config */}
              <img
                src={p.featuredImage?.url || "/placeholder.png"}
                alt={p.featuredImage?.altText || p.title}
                className="w-full h-56 object-cover rounded-lg border"
              />
              <div className="mt-3 flex items-center justify-between">
                <h2 className="font-semibold">{p.title}</h2>
                {price && (
                  <span className="text-sm opacity-70">
                    {price.amount} {price.currencyCode}
                  </span>
                )}
              </div>
              <div className="mt-2 text-sm text-gray-500">View details →</div>
            </a>
          );
        })}
      </div>
    </main>
  );
}

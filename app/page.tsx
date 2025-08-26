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
    <main className="max-w-6xl mx-auto p-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {products.map((p: any) => (
        <a key={p.id} href={`/products/${p.handle}`} className="border rounded-xl p-4 shadow-sm block">
          <img
            src={p.featuredImage?.url}
            alt={p.featuredImage?.altText || p.title}
            className="w-full h-56 object-cover rounded-lg"
          />
          <div className="mt-3 flex justify-between items-center">
            <h2 className="font-semibold">{p.title}</h2>
            <span className="text-sm opacity-70">
              {p.variants.nodes[0].price.amount} {p.variants.nodes[0].price.currencyCode}
            </span>
          </div>
        </a>
      ))}
    </main>
  );
}

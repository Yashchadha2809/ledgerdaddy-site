// app/products/[handle]/page.tsx
import { sf } from "../../../lib/shopify";

export default async function ProductPage({ params }: { params: { handle: string } }) {
  const { data }: any = await sf(`
    query Product($handle: String!) {
      productByHandle(handle: $handle) {
        id
        title
        descriptionHtml
        featuredImage { url altText }
        variants(first: 10) {
          nodes { id title availableForSale price { amount currencyCode } }
        }
      }
    }`,
    { handle: params.handle }
  );

  const p = data?.productByHandle;
  if (!p) return <div className="p-6">Product not found.</div>;

  const firstAvailable = p.variants.nodes.find((v: any) => v.availableForSale) ?? p.variants.nodes[0];

  return (
    <main className="max-w-5xl mx-auto p-6 grid gap-8 md:grid-cols-2">
      <img
        src={p.featuredImage?.url}
        alt={p.featuredImage?.altText || p.title}
        className="w-full h-[420px] object-cover rounded-xl"
      />
      <div>
        <h1 className="text-2xl font-bold">{p.title}</h1>
        <div className="prose mt-3" dangerouslySetInnerHTML={{ __html: p.descriptionHtml }} />
        <form action="/api/cart" method="post" className="mt-6 space-y-3">
          <input type="hidden" name="variantId" value={firstAvailable.id} />
          <input type="number" name="quantity" min={1} defaultValue={1}
                 className="border rounded-lg px-3 py-2 w-24" />
          <button className="block rounded-lg px-4 py-2 bg-black text-white">Add to cart</button>
        </form>
      </div>
    </main>
  );
}

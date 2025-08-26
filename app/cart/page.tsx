// app/cart/page.tsx
import { cookies } from "next/headers";
import { sf } from "../../lib/shopify";

export default async function CartPage() {
  const cartId = cookies().get("cartId")?.value;
  if (!cartId) return <div className="p-6">Your cart is empty.</div>;

  const { data }: any = await sf(`
    query GetCart($id: ID!) {
      cart(id: $id) {
        id
        totalQuantity
        cost { subtotalAmount { amount currencyCode } }
        lines(first: 50) {
          nodes {
            id
            quantity
            merchandise {
              ... on ProductVariant {
                id
                title
                product { title featuredImage { url } }
                price { amount currencyCode }
              }
            }
          }
        }
      }
    }`, { id: cartId });

  const cart = data?.cart;
  if (!cart) return <div className="p-6">Your cart is empty.</div>;

  return (
    <main className="max-w-4xl mx-auto p-6">
      <h1 className="text-xl font-bold mb-4">Your Cart</h1>
      <ul className="space-y-4">
        {cart.lines.nodes.map((l: any) => (
          <li key={l.id} className="flex gap-4 items-center border rounded-xl p-3">
            <img src={l.merchandise.product.featuredImage?.url} className="w-20 h-20 object-cover rounded-lg" />
            <div className="flex-1">
              <div className="font-medium">{l.merchandise.product.title}</div>
              <div className="text-sm opacity-70">{l.merchandise.title}</div>
            </div>
            <div>{l.merchandise.price.amount} {l.merchandise.price.currencyCode}</div>
            <div className="w-10 text-right">× {l.quantity}</div>
          </li>
        ))}
      </ul>

      <div className="mt-6 flex items-center justify-between">
        <div className="text-lg">
          Subtotal: {cart.cost.subtotalAmount.amount} {cart.cost.subtotalAmount.currencyCode}
        </div>
        <form action="/api/checkout" method="post">
          <button className="rounded-lg px-5 py-2 bg-black text-white">Checkout</button>
        </form>
      </div>
    </main>
  );
}

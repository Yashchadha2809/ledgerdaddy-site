// app/api/cart/route.ts
import { NextRequest, NextResponse } from "next/server";
import { sf } from "../../../lib/shopify";

export async function POST(req: NextRequest) {
  const form = await req.formData();
  const variantId = String(form.get("variantId") || "");
  const quantity  = Number(form.get("quantity") || 1);
  const cartId    = req.cookies.get("cartId")?.value;

  const query = cartId ? `
    mutation AddLines($cartId: ID!, $lines: [CartLineInput!]!) {
      cartLinesAdd(cartId: $cartId, lines: $lines) {
        cart { id totalQuantity }
        userErrors { message }
      }
    }` : `
    mutation CreateCart($input: CartInput!) {
      cartCreate(input: $input) {
        cart { id totalQuantity }
        userErrors { message }
      }
    }`;

  const variables = cartId
    ? { cartId, lines: [{ merchandiseId: variantId, quantity }] }
    : { input: { lines: [{ merchandiseId: variantId, quantity }] } };

  const { data }: any = await sf(query, variables);
  const cart = data?.cartLinesAdd?.cart ?? data?.cartCreate?.cart;

  if (!cart?.id) {
    return NextResponse.json({ error: "Cart error" }, { status: 500 });
  }

  const res = NextResponse.redirect(new URL("/cart", req.url), 303);
  res.cookies.set("cartId", cart.id, { httpOnly: true, path: "/" });
  return res;
}

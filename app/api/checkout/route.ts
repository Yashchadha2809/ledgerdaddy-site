// app/api/checkout/route.ts
import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";
import { sf } from "../../../lib/shopify";

export async function POST(req: NextRequest) {
  const cartId = cookies().get("cartId")?.value;
  if (!cartId) return NextResponse.redirect(new URL("/cart", req.url), 303);

  // Fetch the cart's checkoutUrl (it already exists on the Cart object)
  const { data }: any = await sf(`
    query GetCheckoutUrl($id: ID!) {
      cart(id: $id) { checkoutUrl }
    }`, { id: cartId });

  const url = data?.cart?.checkoutUrl;
  if (!url) return NextResponse.json({ error: "No checkoutUrl" }, { status: 500 });

  return NextResponse.redirect(url, 303);
}

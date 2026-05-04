import { NextResponse } from "next/server";
import { updateStock } from "@/lib/notion";

export async function PATCH(request: Request) {
  try {
    const { pageId, properties } = await request.json();
    
    if (!pageId || !properties) {
      return NextResponse.json({ error: "Missing pageId or properties" }, { status: 400 });
    }

    const result = await updateStock(pageId, properties);
    return NextResponse.json({ success: true, result });
  } catch (error: any) {
    console.error("API Update Error:", error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

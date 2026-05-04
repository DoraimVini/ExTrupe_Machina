import fs from "fs";
import path from "path";

const NOTION_TOKEN = process.env.NOTION_TOKEN;
const STOCK_DB_ID = process.env.NOTION_STOCK_DB_ID;
const CALENDAR_DB_ID = process.env.NOTION_CALENDAR_DB_ID;

const headers = {
  "Authorization": `Bearer ${NOTION_TOKEN}`,
  "Notion-Version": "2022-06-28",
  "Content-Type": "application/json"
};

export async function updateStock(pageId: string, properties: any) {
  try {
    const res = await fetch(`https://api.notion.com/v1/pages/${pageId}`, {
      method: "PATCH",
      headers,
      body: JSON.stringify({ properties })
    });
    
    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(`Notion Update Error: ${JSON.stringify(errorData)}`);
    }
    
    return await res.json();
  } catch (error) {
    console.error("updateStock error:", error);
    throw error;
  }
}

export async function getStock() {
  try {
    if (!STOCK_DB_ID) throw new Error("NOTION_STOCK_DB_ID is not defined");
    
    const res = await fetch(`https://api.notion.com/v1/databases/${STOCK_DB_ID}/query`, {
      method: "POST",
      headers,
      next: { revalidate: 3600 } // Cache for 1 hour
    });
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      console.error("Notion Stock Fetch Error:", errorData);
      throw new Error(`Failed to fetch stock: ${res.status} ${res.statusText}`);
    }
    
    const data = await res.json();
    
    return data.results.map((page: any) => ({
      id: page.id,
      name: page.properties.Nome?.title[0]?.text?.content || "Sem nome",
      category: page.properties.Categoria?.select?.name || "Outros",
      price: page.properties.Preço?.number || 0,
      status: page.properties.Status?.select?.name || "N/A",
      photo: page.properties.Foto?.rich_text[0]?.text?.content || ""
    }));
  } catch (error) {
    console.error("getStock error:", error);
    return []; // Return empty array to prevent dashboard crash
  }
}

export async function getFinanceSummary() {
  try {
    const filePath = path.join(process.cwd(), "data", "finance_summary.json");
    if (!fs.existsSync(filePath)) {
      return null;
    }
    const fileContent = fs.readFileSync(filePath, "utf-8");
    return JSON.parse(fileContent);
  } catch (error) {
    console.error("Error reading finance summary:", error);
    return null;
  }
}

export async function getCalendar() {
  try {
    if (!CALENDAR_DB_ID) throw new Error("NOTION_CALENDAR_DB_ID is not defined");

    const res = await fetch(`https://api.notion.com/v1/databases/${CALENDAR_DB_ID}/query`, {
      method: "POST",
      headers,
      next: { revalidate: 3600 }
    });
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      console.error("Notion Calendar Fetch Error:", errorData);
      throw new Error(`Failed to fetch calendar: ${res.status} ${res.statusText}`);
    }
    
    const data = await res.json();
    
    return data.results.map((page: any) => ({
      id: page.id,
      name: page.properties[""]?.title[0]?.text?.content || "Evento",
      date: page.properties["Data de Postagem"]?.date?.start || "",
      type: page.properties["Tipo"]?.rich_text[0]?.text?.content || "Feira",
      platform: page.properties["Plataforma"]?.rich_text[0]?.text?.content || "Presencial"
    })).sort((a: any, b: any) => new Date(a.date).getTime() - new Date(b.date).getTime());
  } catch (error) {
    console.error("getCalendar error:", error);
    return [];
  }
}

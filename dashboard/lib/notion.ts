const NOTION_TOKEN = process.env.NOTION_TOKEN;
const STOCK_DB_ID = process.env.NOTION_STOCK_DB_ID;
const CALENDAR_DB_ID = process.env.NOTION_CALENDAR_DB_ID;

const headers = {
  "Authorization": `Bearer ${NOTION_TOKEN}`,
  "Notion-Version": "2022-06-28",
  "Content-Type": "application/json"
};

export async function getStock() {
  const res = await fetch(`https://api.notion.com/v1/databases/${STOCK_DB_ID}/query`, {
    method: "POST",
    headers,
    next: { revalidate: 3600 } // Cache for 1 hour
  });
  
  if (!res.ok) throw new Error("Failed to fetch stock");
  const data = await res.json();
  
  return data.results.map((page: any) => ({
    id: page.id,
    name: page.properties.Nome?.title[0]?.text?.content || "Sem nome",
    category: page.properties.Categoria?.select?.name || "Outros",
    price: page.properties.Preço?.number || 0,
    status: page.properties.Status?.select?.name || "N/A",
    photo: page.properties.Foto?.rich_text[0]?.text?.content || ""
  }));
}

export async function getCalendar() {
  const res = await fetch(`https://api.notion.com/v1/databases/${CALENDAR_DB_ID}/query`, {
    method: "POST",
    headers,
    next: { revalidate: 3600 }
  });
  
  if (!res.ok) throw new Error("Failed to fetch calendar");
  const data = await res.json();
  
  return data.results.map((page: any) => ({
    id: page.id,
    name: page.properties[""]?.title[0]?.text?.content || "Evento",
    date: page.properties["Data de Postagem"]?.date?.start || "",
    type: page.properties["Tipo"]?.rich_text[0]?.text?.content || "Feira",
    platform: page.properties["Plataforma"]?.rich_text[0]?.text?.content || "Presencial"
  })).sort((a: any, b: any) => new Date(a.date).getTime() - new Date(b.date).getTime());
}

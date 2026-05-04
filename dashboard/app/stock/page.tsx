import Sidebar from "@/components/Sidebar";
import StockManager from "@/components/StockManager";
import { getStock } from "@/lib/notion";

export default async function StockPage() {
  const stock = await getStock();

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-8 overflow-y-auto">
        <header className="flex justify-between items-center mb-10">
          <div>
            <h1 className="text-4xl font-bold text-white tracking-tight">Estoque</h1>
            <p className="text-sand/60 mt-1">Gerencie seu inventário e status de produção.</p>
          </div>
        </header>
        
        <StockManager initialData={stock} />
      </main>
    </div>
  );
}

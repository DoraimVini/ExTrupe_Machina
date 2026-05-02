import Sidebar from "@/components/Sidebar";
import StatCard from "@/components/StatCard";
import { getStock, getCalendar } from "@/lib/notion";
import { ShoppingBag, Calendar, Truck, AlertCircle } from "lucide-react";

interface StockItem {
  id: string;
  name: string;
  category: string;
  price: number;
  status: string;
  photo?: string;
}

interface CalendarEvent {
  id: string;
  name: string;
  date: string;
  type: string;
  platform: string;
}

export default async function DashboardPage() {
  let stock: StockItem[] = [];
  let calendar: CalendarEvent[] = [];
  
  try {
    [stock, calendar] = await Promise.all([getStock(), getCalendar()]);
  } catch (error) {
    console.error("Dashboard data fetch error:", error);
  }

  const totalItems = stock.length;
  const availableItems = stock.filter(item => item.status === "Disponível").length;
  const upcomingFairs = calendar.length;

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      
      <main className="flex-1 p-8 overflow-y-auto">
        <header className="flex justify-between items-center mb-10">
          <div>
            <h1 className="text-4xl font-bold text-white tracking-tight">Overview</h1>
            <p className="text-sand/60 mt-1">Bem-vindo à central de comando da Trupe BR.</p>
          </div>
          
          <div className="flex gap-4">
            <div className="glass-card px-4 py-2 flex items-center gap-2 border-white/[0.05]">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-xs font-bold text-sand/80 uppercase">Notion Sync: OK</span>
            </div>
          </div>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          <StatCard 
            label="Total em Estoque" 
            value={totalItems} 
            icon={ShoppingBag} 
            trend="+12%" 
            trendUp={true} 
          />
          <StatCard 
            label="Disponíveis" 
            value={availableItems} 
            icon={Truck} 
          />
          <StatCard 
            label="Receita Total" 
            value="R$ 14.675,00" 
            icon={ShoppingBag} 
            trend="+12%"
            trendUp={true}
          />
          <StatCard 
            label="Lucro Líquido" 
            value="R$ 11.360,00" 
            icon={AlertCircle} 
            trend="77.4%"
            trendUp={true}
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Stock List */}
          <div className="lg:col-span-2 flex flex-col gap-6">
            <div className="glass-card overflow-hidden">
              <div className="p-6 border-b border-white/[0.05] flex justify-between items-center">
                <h3 className="font-bold text-white uppercase text-xs tracking-widest">Estoque Recente</h3>
                <button className="text-xs font-bold text-terracotta hover:underline">Ver tudo</button>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead className="bg-white/[0.02] text-[10px] uppercase tracking-wider text-sand/40">
                    <tr>
                      <th className="px-6 py-4">Produto</th>
                      <th className="px-6 py-4">Categoria</th>
                      <th className="px-6 py-4">Preço</th>
                      <th className="px-6 py-4">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/[0.05]">
                    {stock.slice(0, 6).map((item) => (
                      <tr key={item.id} className="hover:bg-white/[0.02] transition-colors group">
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-lg bg-earth-muted border border-white/[0.05] overflow-hidden">
                              {item.photo ? (
                                <img src={item.photo} alt={item.name} className="w-full h-full object-cover" />
                              ) : (
                                <div className="w-full h-full flex items-center justify-center text-[10px] text-sand/30">IMG</div>
                              )}
                            </div>
                            <span className="text-sm font-medium text-white">{item.name}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-sand/60">{item.category}</td>
                        <td className="px-6 py-4 text-sm font-bold text-sand/80">R$ {item.price.toFixed(2)}</td>
                        <td className="px-6 py-4">
                          <span className="text-[10px] font-bold uppercase px-2 py-1 rounded-md bg-terracotta/10 text-terracotta border border-terracotta/20">
                            {item.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Fairs / Calendar */}
          <div className="flex flex-col gap-6">
            <div className="glass-card">
              <div className="p-6 border-b border-white/[0.05]">
                <h3 className="font-bold text-white uppercase text-xs tracking-widest">Próximas Feiras</h3>
              </div>
              <div className="p-6 space-y-6">
                {calendar.slice(0, 5).map((event) => (
                  <div key={event.id} className="flex gap-4 items-start">
                    <div className="w-12 h-12 rounded-xl bg-white/[0.03] border border-white/[0.05] flex flex-col items-center justify-center">
                      <span className="text-[10px] font-bold text-terracotta uppercase">
                        {new Date(event.date).toLocaleDateString('pt-BR', { month: 'short' }).replace('.', '')}
                      </span>
                      <span className="text-lg font-bold text-white leading-none">
                        {new Date(event.date).getDate()}
                      </span>
                    </div>
                    <div>
                      <h4 className="text-sm font-bold text-white">{event.name}</h4>
                      <p className="text-xs text-sand/50 mt-0.5">{event.platform}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

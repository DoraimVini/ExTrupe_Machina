"use client";

import { useState } from "react";
import { Search, Filter, ExternalLink, Plus, RefreshCw, Edit2 } from "lucide-react";

interface StockItem {
  id: string;
  name: string;
  category: string;
  price: number;
  status: string;
  photo?: string;
}

export default function StockManager({ initialData }: { initialData: StockItem[] }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("Todas");
  const [stock, setStock] = useState(initialData);
  const [updatingId, setUpdatingId] = useState<string | null>(null);
  
  const categories = ["Todas", ...Array.from(new Set(stock.map(item => item.category)))];
  
  const filteredStock = stock.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = categoryFilter === "Todas" || item.category === categoryFilter;
    return matchesSearch && matchesCategory;
  });

  const handleStatusChange = async (id: string, newStatus: string) => {
    setUpdatingId(id);
    try {
      const res = await fetch("/api/notion/update", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          pageId: id,
          properties: {
            "Status": { "select": { "name": newStatus } }
          }
        })
      });

      if (!res.ok) throw new Error("Falha ao atualizar");

      setStock(prev => prev.map(item => 
        item.id === id ? { ...item, status: newStatus } : item
      ));
    } catch (error) {
      alert("Erro ao atualizar status no Notion");
    } finally {
      setUpdatingId(null);
    }
  };

  const notionDbUrl = "https://www.notion.so/35205465f1ab80a88de4e23cea9e7136";

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="flex flex-col md:flex-row gap-4 justify-between items-center bg-white/[0.02] p-4 rounded-2xl border border-white/[0.05]">
        <div className="flex flex-1 gap-4 w-full md:w-auto">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-sand/40" size={18} />
            <input 
              type="text" 
              placeholder="Buscar produto..."
              className="w-full bg-white/5 border border-white/10 rounded-xl py-2 pl-10 pr-4 text-white focus:outline-none focus:border-terracotta/50 transition-colors"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 text-sand/40" size={18} />
            <select 
              className="bg-white/5 border border-white/10 rounded-xl py-2 pl-10 pr-8 text-white appearance-none focus:outline-none focus:border-terracotta/50 transition-colors cursor-pointer"
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
            >
              {categories.map(cat => (
                <option key={cat} value={cat} className="bg-earth-dark text-white">{cat}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="flex gap-2 w-full md:w-auto">
          <button 
            onClick={() => window.location.reload()}
            className="glass-button flex items-center gap-2 text-xs font-bold whitespace-nowrap"
          >
            <RefreshCw size={14} className={updatingId ? "animate-spin" : ""} /> Sincronizar
          </button>
          <a 
            href={notionDbUrl} 
            target="_blank" 
            rel="noopener noreferrer"
            className="glass-button flex items-center gap-2 text-xs font-bold bg-terracotta/10 text-terracotta border-terracotta/20 hover:bg-terracotta/20 whitespace-nowrap"
          >
            <Plus size={14} /> Novo Item
          </a>
        </div>
      </div>

      {/* Table */}
      <div className="glass-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-white/[0.02] text-[10px] uppercase tracking-wider text-sand/40">
              <tr>
                <th className="px-6 py-4">Produto</th>
                <th className="px-6 py-4">Categoria</th>
                <th className="px-6 py-4">Preço</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4 text-right">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.05]">
              {filteredStock.map((item) => (
                <tr key={item.id} className="hover:bg-white/[0.02] transition-colors group">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-lg bg-earth-muted border border-white/[0.05] overflow-hidden">
                        {item.photo ? (
                          <img src={item.photo} alt={item.name} className="w-full h-full object-cover" />
                        ) : (
                          <div className="w-full h-full flex items-center justify-center text-[10px] text-sand/30 uppercase">Img</div>
                        )}
                      </div>
                      <span className="text-sm font-medium text-white">{item.name}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-xs text-sand/60 bg-white/5 px-2 py-1 rounded-md">{item.category}</span>
                  </td>
                  <td className="px-6 py-4 text-sm font-bold text-sand/80">
                    R$ {item.price.toFixed(2)}
                  </td>
                  <td className="px-6 py-4">
                    <select 
                      disabled={updatingId === item.id}
                      className={`text-[10px] font-bold uppercase px-2 py-1 rounded-md border bg-transparent cursor-pointer focus:outline-none ${
                        item.status.includes('OK') 
                          ? 'text-green-500 border-green-500/20' 
                          : 'text-terracotta border-terracotta/20'
                      }`}
                      value={item.status}
                      onChange={(e) => handleStatusChange(item.id, e.target.value)}
                    >
                      <option value="✅ OK" className="bg-earth-dark">✅ OK</option>
                      <option value="⚠️ Crítico" className="bg-earth-dark">⚠️ Crítico</option>
                      <option value="❌ Sem estoque" className="bg-earth-dark">❌ Sem estoque</option>
                    </select>
                    {updatingId === item.id && <RefreshCw size={10} className="inline ml-2 animate-spin text-sand/40" />}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex justify-end gap-2">
                      <a 
                        href={`${notionDbUrl}/${item.id.replace(/-/g, '')}`} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="p-2 hover:bg-white/10 rounded-lg text-sand/40 hover:text-white transition-colors"
                        title="Ver no Notion"
                      >
                        <ExternalLink size={14} />
                      </a>
                    </div>
                  </td>
                </tr>
              ))}
              {filteredStock.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-6 py-20 text-center text-sand/40 italic">
                    Nenhum produto encontrado com estes filtros.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

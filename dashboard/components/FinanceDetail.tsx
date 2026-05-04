"use client";

import { PieChart, TrendingUp, Info } from "lucide-react";

interface CategorySummary {
  Produto: string;
  "Receita (R$)": number;
  "Lucro (R$)": number;
  "Margem (%)": number;
  Qtd: number;
}

interface MonthlyStat {
  Data: string;
  "Receita (R$)": number;
  "Lucro (R$)": number;
}

interface FinanceData {
  totals: {
    receita: number;
    lucro: number;
    custo: number;
    margem_media: number;
  };
  monthly: MonthlyStat[];
  by_category: CategorySummary[];
  performance: {
    best_seller_revenue: string;
    best_seller_profit: string;
    low_margin_alerts: string[];
  };
  insights: string[];
}

export default function FinanceDetail({ data }: { data: FinanceData }) {
  // Sort categories by revenue
  const topCategories = [...data.by_category]
    .sort((a, b) => b["Receita (R$)"] - a["Receita (R$)"])
    .slice(0, 5);

  const maxMonthlyRevenue = Math.max(...(data.monthly?.map(m => m["Receita (R$)"]) || [1]));

  return (
    <div className="space-y-6">
      {/* Monthly Chart */}
      <div className="glass-card p-6">
        <h4 className="text-[10px] font-bold text-white uppercase tracking-[0.2em] mb-6 flex items-center gap-2">
          <TrendingUp size={14} className="text-terracotta" /> Histórico Mensal
        </h4>
        <div className="flex items-end gap-2 h-32">
          {data.monthly?.map((m) => (
            <div key={m.Data} className="flex-1 flex flex-col items-center gap-2 group">
              <div className="relative w-full flex items-end justify-center gap-0.5 h-full">
                {/* Revenue Bar */}
                <div 
                  className="w-full max-w-[20px] bg-white/10 rounded-t-sm group-hover:bg-white/20 transition-all"
                  style={{ height: `${(m["Receita (R$)"] / maxMonthlyRevenue) * 100}%` }}
                >
                   <div className="absolute -top-6 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity bg-earth-dark text-[8px] px-1 rounded border border-white/10 whitespace-nowrap">
                    R$ {m["Receita (R$)"].toLocaleString()}
                  </div>
                </div>
                {/* Profit Bar */}
                <div 
                  className="w-full max-w-[10px] bg-terracotta/40 rounded-t-sm"
                  style={{ height: `${(m["Lucro (R$)"] / maxMonthlyRevenue) * 100}%` }}
                />
              </div>
              <span className="text-[8px] text-sand/40 font-bold">{m.Data}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="glass-card p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-full bg-ochre/20 flex items-center justify-center text-ochre">
            <PieChart size={20} />
          </div>
          <div>
            <h3 className="font-bold text-white uppercase text-xs tracking-widest">Análise de Performance</h3>
            <p className="text-[10px] text-sand/40">Detalhamento por produto e lucratividade</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Detailed Stats */}
          <div className="space-y-6">
            <div>
              <h5 className="text-[10px] text-sand/40 uppercase mb-4 font-bold tracking-tighter">Ranking de Faturamento</h5>
              <div className="space-y-4">
                {topCategories.map((cat) => (
                  <div key={cat.Produto} className="group">
                    <div className="flex justify-between items-end mb-1">
                      <span className="text-xs font-medium text-sand/80">{cat.Produto}</span>
                      <span className="text-[10px] font-bold text-white">
                        R$ {cat["Receita (R$)"].toLocaleString("pt-BR")}
                      </span>
                    </div>
                    <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-terracotta to-ochre rounded-full transition-all duration-1000"
                        style={{ width: `${(cat["Receita (R$)"] / data.totals.receita) * 100}%` }}
                      />
                    </div>
                    <div className="flex justify-between mt-1">
                      <span className={`text-[9px] uppercase tracking-tighter ${cat["Margem (%)"] < 40 ? 'text-terracotta font-bold' : 'text-sand/30'}`}>
                        Margem: {cat["Margem (%)"].toFixed(1)}%
                      </span>
                      <span className="text-[9px] text-sand/30 uppercase tracking-tighter">{cat.Qtd} unidades</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Performance Badges */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white/5 p-3 rounded-xl border border-white/10">
                <p className="text-[8px] text-sand/40 uppercase font-bold">Estrela de Vendas</p>
                <p className="text-xs font-bold text-white truncate">{data.performance.best_seller_revenue}</p>
              </div>
              <div className="bg-white/5 p-3 rounded-xl border border-white/10">
                <p className="text-[8px] text-sand/40 uppercase font-bold">Maior Lucro Líquido</p>
                <p className="text-xs font-bold text-white truncate">{data.performance.best_seller_profit}</p>
              </div>
            </div>
          </div>

          {/* Insights Panel */}
          <div className="bg-white/[0.02] rounded-xl border border-white/[0.05] p-6 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-terracotta/5 blur-3xl -z-10 rounded-full" />
            
            <h4 className="text-[10px] font-bold text-terracotta uppercase tracking-[0.2em] mb-4 flex items-center gap-2">
              <Info size={14} /> Relatório de Gestão
            </h4>
            <ul className="space-y-4">
              {data.insights.map((insight, idx) => (
                <li key={idx} className="flex gap-3 text-sm text-sand/70 leading-relaxed italic">
                  <span className="text-terracotta font-bold">•</span>
                  {insight}
                </li>
              ))}
            </ul>
            
            <div className="mt-8 pt-6 border-t border-white/5 flex justify-between items-center">
              <div>
                <p className="text-[10px] text-sand/40 uppercase">Retorno Médio</p>
                <p className="text-xl font-bold text-white">{data.totals.margem_media.toFixed(1)}%</p>
              </div>
              <div className="text-right">
                <p className="text-[10px] text-sand/40 uppercase">Custo de Mercadoria</p>
                <p className="text-sm font-bold text-sand/80">R$ {data.totals.custo.toLocaleString("pt-BR")}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

import { LucideIcon } from "lucide-react";

interface StatCardProps {
  label: string;
  value: string | number;
  icon: LucideIcon;
  trend?: string;
  trendUp?: boolean;
}

export default function StatCard({ label, value, icon: Icon, trend, trendUp }: StatCardProps) {
  return (
    <div className="glass-card p-6 flex flex-col gap-4">
      <div className="flex justify-between items-start">
        <div className="p-3 rounded-xl bg-white/[0.03] border border-white/[0.05]">
          <Icon className="text-terracotta" size={24} />
        </div>
        {trend && (
          <span className={`text-xs font-bold px-2 py-1 rounded-full ${trendUp ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'}`}>
            {trend}
          </span>
        )}
      </div>
      <div>
        <p className="text-sand/50 text-xs font-bold uppercase tracking-wider">{label}</p>
        <p className="text-3xl font-bold mt-1 text-white">{value}</p>
      </div>
    </div>
  );
}

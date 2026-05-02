import Link from "next/link";
import { LayoutDashboard, ShoppingBag, Calendar, Settings, HelpCircle } from "lucide-react";

const menuItems = [
  { icon: LayoutDashboard, label: "Overview", href: "/" },
  { icon: ShoppingBag, label: "Estoque", href: "/stock" },
  { icon: Calendar, label: "Feiras", href: "/calendar" },
];

const secondaryItems = [
  { icon: Settings, label: "Configurações", href: "/settings" },
  { icon: HelpCircle, label: "Ajuda", href: "/help" },
];

export default function Sidebar() {
  return (
    <aside className="w-64 glass border-r border-glass-border flex flex-col h-screen sticky top-0">
      <div className="p-8 flex flex-col items-center">
        <img src="/logo.png" alt="Trupe BR Logo" className="w-24 h-auto hover:scale-110 transition-transform duration-700 ease-in-out" />
        <div className="mt-4 text-center">
          <p className="text-[10px] font-bold text-terracotta uppercase tracking-[0.4em] animate-fade-in">Tricô Artesanal</p>
        </div>
      </div>

      <nav className="flex-1 px-4 space-y-8 mt-4">
        <div>
          <h2 className="text-[10px] font-bold text-sand/40 uppercase tracking-[0.2em] px-4 mb-4">Menu Principal</h2>
          <div className="space-y-1">
            {menuItems.map((item) => (
              <Link
                key={item.label}
                href={item.href}
                className="flex items-center gap-3 px-4 py-3 rounded-xl text-sand/70 hover:text-white hover:bg-white/5 transition-all group"
              >
                <item.icon size={20} className="group-hover:text-terracotta transition-colors" />
                <span className="font-medium">{item.label}</span>
              </Link>
            ))}
          </div>
        </div>

        <div>
          <h2 className="text-[10px] font-bold text-sand/40 uppercase tracking-[0.2em] px-4 mb-4">Sistema</h2>
          <div className="space-y-1">
            {secondaryItems.map((item) => (
              <Link
                key={item.label}
                href={item.href}
                className="flex items-center gap-3 px-4 py-3 rounded-xl text-sand/70 hover:text-white hover:bg-white/5 transition-all group"
              >
                <item.icon size={20} className="group-hover:text-terracotta transition-colors" />
                <span className="font-medium">{item.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </nav>

      <div className="p-4">
        <div className="glass-card p-4 flex items-center gap-3 bg-white/[0.02]">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-terracotta to-ochre flex items-center justify-center font-bold text-white shadow-lg">
            V
          </div>
          <div>
            <p className="text-sm font-bold text-white">Vini</p>
            <p className="text-[10px] text-sand/50">Admin</p>
          </div>
        </div>
      </div>
    </aside>
  );
}

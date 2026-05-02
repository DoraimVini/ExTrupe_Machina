import Sidebar from "@/components/Sidebar";

export default function SettingsPage() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-8 overflow-y-auto">
        <header className="flex justify-between items-center mb-10">
          <div>
            <h1 className="text-4xl font-bold text-white tracking-tight">Configurações</h1>
            <p className="text-sand/60 mt-1">Ajustes do sistema e integrações.</p>
          </div>
        </header>
        
        <div className="glass-card p-12 text-center flex flex-col items-center justify-center min-h-[400px]">
          <h2 className="text-2xl font-bold text-white mb-4">Página em Construção</h2>
          <p className="text-sand/60 max-w-md mx-auto">Gerencie as chaves de API do Notion, configure exportações automáticas para o Excel e ajuste as preferências de estilo do Dashboard.</p>
        </div>
      </main>
    </div>
  );
}

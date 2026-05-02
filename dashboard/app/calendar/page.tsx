import Sidebar from "@/components/Sidebar";

export default function CalendarPage() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-8 overflow-y-auto">
        <header className="flex justify-between items-center mb-10">
          <div>
            <h1 className="text-4xl font-bold text-white tracking-tight">Feiras</h1>
            <p className="text-sand/60 mt-1">Calendário de eventos e agendamentos.</p>
          </div>
        </header>
        
        <div className="glass-card p-12 text-center flex flex-col items-center justify-center min-h-[400px]">
          <h2 className="text-2xl font-bold text-white mb-4">Página em Construção</h2>
          <p className="text-sand/60 max-w-md mx-auto">Esta página conterá o calendário completo de feiras, agendamentos de entregas e integrações com o Notion para a agenda da semana.</p>
        </div>
      </main>
    </div>
  );
}

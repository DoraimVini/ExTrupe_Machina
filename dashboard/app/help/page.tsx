import Sidebar from "@/components/Sidebar";

export default function HelpPage() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-8 overflow-y-auto">
        <header className="flex justify-between items-center mb-10">
          <div>
            <h1 className="text-4xl font-bold text-white tracking-tight">Ajuda</h1>
            <p className="text-sand/60 mt-1">Suporte e documentação do sistema.</p>
          </div>
        </header>
        
        <div className="glass-card p-12 text-center flex flex-col items-center justify-center min-h-[400px]">
          <h2 className="text-2xl font-bold text-white mb-4">Central de Ajuda</h2>
          <p className="text-sand/60 max-w-md mx-auto">Em breve, você encontrará aqui tutoriais em vídeo, documentação das integrações e contato com o suporte técnico da infraestrutura.</p>
        </div>
      </main>
    </div>
  );
}

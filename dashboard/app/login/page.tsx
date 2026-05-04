import LoginForm from "./login-form";

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center p-6 relative">
      {/* Decorative background elements */}
      <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-terracotta/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-ochre/10 rounded-full blur-[120px] pointer-events-none" />

      <div className="w-full max-w-md animate-fade-in">
        <div className="text-center mb-10">
          <img 
            src="/logo.png" 
            alt="Trupe BR Logo" 
            className="w-32 h-auto mx-auto mb-6 hover:scale-105 transition-transform duration-700"
          />
          <h1 className="text-3xl font-bold text-white tracking-tight">Dashboard de Gestão</h1>
          <p className="text-sand/50 mt-2">Bem-vinda de volta, Trupe.</p>
        </div>

        <div className="glass-card p-8 bg-white/[0.02]">
          <LoginForm />
        </div>

        <footer className="text-center mt-12">
          <p className="text-[10px] font-bold text-sand/20 uppercase tracking-[0.4em]">
            &copy; 2026 Trupe BR | Knitwear & Artesanato
          </p>
        </footer>
      </div>
    </div>
  );
}

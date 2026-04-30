import json
from pathlib import Path

def generate(log_file="logs/audit_trail.json", output_file="dashboard.html"):
    log_path = Path(log_file)
    if not log_path.exists():
        return

    with open(log_path, "r", encoding="utf-8") as f:
        logs = json.load(f)

    # Pegar os últimos 30 logs
    recent_logs = logs[-30:]
    recent_logs.reverse()

    log_rows = []
    for log in recent_logs:
        timestamp = log['timestamp'].split('T')[1][:8]
        agent = log['agent']
        agent_lower = agent.lower()
        action = log['action']
        details = log['details']
        
        row = f"""
                        <tr>
                            <td class="timestamp">{timestamp}</td>
                            <td><span class="agent-tag tag-{agent_lower}">{agent}</span></td>
                            <td class="action-cell">{action}</td>
                            <td class="details-cell">{details}</td>
                        </tr>"""
        log_rows.append(row)

    log_rows_html = "".join(log_rows)

    html_template = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trupe Br — Central de Comando</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&family=Playfair+Display:ital,wght@0,600;1,600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #ff7675;
            --secondary: #55efc4;
            --accent: #a29bfe;
            --dark: #1e272e;
            --glass: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --font-main: 'Outfit', sans-serif;
            --font-title: 'Playfair Display', serif;
        }

        body {
            background-color: var(--dark);
            background-image: 
                radial-gradient(at 0% 0%, rgba(255, 118, 117, 0.1) 0, transparent 50%), 
                radial-gradient(at 50% 0%, rgba(85, 239, 196, 0.05) 0, transparent 50%),
                radial-gradient(at 100% 0%, rgba(162, 155, 254, 0.1) 0, transparent 50%);
            color: #f1f2f6;
            font-family: var(--font-main);
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }

        .banner {
            width: 100%;
            height: 300px;
            background: url('banner.png') center/cover no-repeat;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            border-bottom: 1px solid var(--glass-border);
        }

        .banner::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(to bottom, rgba(30, 39, 46, 0.2), var(--dark));
        }

        .banner-content {
            position: relative;
            z-index: 1;
            text-align: center;
        }

        .banner h1 {
            font-family: var(--font-title);
            font-size: 3.5rem;
            margin: 0;
            letter-spacing: -1px;
            text-shadow: 0 10px 20px rgba(0,0,0,0.5);
        }

        .container {
            max-width: 1200px;
            margin: -50px auto 50px;
            padding: 0 20px;
            position: relative;
            z-index: 2;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding: 20px 30px;
            background: var(--glass);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            border: 1px solid var(--glass-border);
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        }

        .status-badge {
            background: rgba(39, 174, 96, 0.2);
            color: #2ecc71;
            padding: 8px 18px;
            border-radius: 50px;
            font-size: 14px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
            border: 1px solid rgba(39, 174, 96, 0.3);
        }

        .status-dot {
            width: 10px;
            height: 10px;
            background: #2ecc71;
            border-radius: 50%;
            box-shadow: 0 0 10px #2ecc71;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.4); opacity: 0.6; }
            100% { transform: scale(1); opacity: 1; }
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }

        .card {
            background: var(--glass);
            backdrop-filter: blur(20px);
            padding: 30px;
            border-radius: 24px;
            border: 1px solid var(--glass-border);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .card:hover {
            transform: translateY(-10px);
            border-color: var(--primary);
            background: rgba(255, 255, 255, 0.08);
        }

        .card h3 {
            margin: 0 0 10px 0;
            color: var(--primary);
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .card .value {
            font-size: 28px;
            font-weight: 600;
            margin: 10px 0;
        }

        .card .desc {
            font-size: 13px;
            color: rgba(255,255,255,0.5);
        }

        section h2 {
            font-family: var(--font-title);
            font-size: 2rem;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        section h2::after {
            content: '';
            flex: 1;
            height: 1px;
            background: var(--glass-border);
        }

        .log-container {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            border: 1px solid var(--glass-border);
            overflow: hidden;
            box-shadow: 0 20px 50px rgba(0,0,0,0.2);
        }

        .log-table {
            width: 100%;
            border-collapse: collapse;
        }

        .log-table th, .log-table td {
            padding: 20px;
            text-align: left;
            border-bottom: 1px solid var(--glass-border);
        }

        .log-table th {
            background: rgba(255,255,255,0.03);
            color: var(--accent);
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }

        .agent-tag {
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
        }

        .tag-atendimento { background: rgba(230, 126, 34, 0.2); color: #e67e22; border: 1px solid rgba(230, 126, 34, 0.3); }
        .tag-estoque { background: rgba(41, 128, 185, 0.2); color: #2980b9; border: 1px solid rgba(41, 128, 185, 0.3); }
        .tag-auditoria { background: rgba(142, 68, 173, 0.2); color: #8e44ad; border: 1px solid rgba(142, 68, 173, 0.3); }
        .tag-orchestrator { background: rgba(192, 57, 43, 0.2); color: #c0392b; border: 1px solid rgba(192, 57, 43, 0.3); }

        .timestamp {
            font-family: monospace;
            font-size: 13px;
            color: rgba(255,255,255,0.4);
        }

        .action-cell {
            font-weight: 600;
            font-size: 14px;
        }

        .details-cell {
            font-size: 14px;
            color: rgba(255,255,255,0.8);
        }
    </style>
</head>
<body>
    <div class="banner">
        <div class="banner-content">
            <h1>Trupe Br — Machina</h1>
            <p style="letter-spacing: 5px; opacity: 0.7;">AUTOMAÇÃO & INTELIGÊNCIA</p>
        </div>
    </div>

    <div class="container">
        <header>
            <div style="font-size: 18px; font-weight: 400; opacity: 0.8;">Bem-vinda ao seu centro de controle, <span style="color: var(--primary); font-weight: 600;">Erika</span>.</div>
            <div class="status-badge">
                <div class="status-dot"></div>
                Sistema Operacional
            </div>
        </header>

        <div class="grid">
            <div class="card">
                <h3>Logística</h3>
                <div class="value">Estoque</div>
                <div class="desc">Sincronizado via Notion & Nuvemshop</div>
                <div style="margin-top: 15px; color: #2ecc71; font-size: 12px; font-weight: 600;">✓ ATIVO</div>
            </div>
            <div class="card">
                <h3>Vendas</h3>
                <div class="value">Atendimento</div>
                <div class="desc">WhatsApp e Instagram humanizados</div>
                <div style="margin-top: 15px; color: #2ecc71; font-size: 12px; font-weight: 600;">✓ ATIVO</div>
            </div>
            <div class="card">
                <h3>Monitor</h3>
                <div class="value">Auditoria</div>
                <div class="desc">Saúde do catálogo e sincronia</div>
                <div style="margin-top: 15px; color: #2ecc71; font-size: 12px; font-weight: 600;">✓ SAUDÁVEL</div>
            </div>
        </div>

        <section>
            <h2>Atividade Recente dos Agentes</h2>
            <div class="log-container">
                <table class="log-table">
                    <thead>
                        <tr>
                            <th>Hora</th>
                            <th>Agente</th>
                            <th>Ação</th>
                            <th>Detalhes</th>
                        </tr>
                    </thead>
                    <tbody>
                        [LOG_ROWS]
                    </tbody>
                </table>
            </div>
        </section>

        <footer style="margin-top: 50px; text-align: center; font-size: 12px; opacity: 0.3; padding-bottom: 50px;">
            TRUPE BR — MACHINA | DESENVOLVIDO POR ANTIGRAVITY
        </footer>
    </div>
</body>
</html>
    """

    final_html = html_template.replace("[LOG_ROWS]", log_rows_html)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"[DASHBOARD] Gerado com sucesso: {output_file}")

if __name__ == "__main__":
    generate()

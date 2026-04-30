import os
from dotenv import load_dotenv
from harness.audit.logger import AuditLogger
from harness.agents.inventory import InventoryAgent
from harness.agents.marketing import MarketingAgent

def run_harness():
    # 0. Carrega variáveis de ambiente
    load_dotenv()
    notion_token = os.getenv("NOTION_TOKEN")
    db_estoque = os.getenv("DATABASE_ID_ESTOQUE", "35205465-f1ab-80a8-8de4-e23cea9e7136")

    if not notion_token:
        print("[AVISO] NOTION_TOKEN não encontrado no arquivo .env")
        print("Por favor, configure o arquivo .env baseado no .env.example")
        # Criando .env vazio se não existir para facilitar
        if not os.path.exists(".env"):
            with open(".env", "w") as f:
                f.write("NOTION_TOKEN=\nDATABASE_ID_ESTOQUE=35205465-f1ab-80a8-8de4-e23cea9e7136\n")
        return

    # 1. Inicializa o Auditor (O Coração do Harness)
    logger = AuditLogger()
    logger.log_action("Harness", "STARTUP", "Iniciando ciclo de automação real Trupe BR.")

    # 2. Configura os Agentes
    inventory = InventoryAgent(logger, database_id=db_estoque, notion_token=notion_token)
    marketing = MarketingAgent(logger, inspiration_dir="inspiracao")

    # 3. Executa Fluxo de Trabalho Integrado
    
    # Passo A: Automação de Galeria (Novas peças da pasta de inspiração)
    # Isso cria as páginas no Notion para cada foto encontrada
    new_items = inventory.register_inspiration_as_stock(inspiration_dir="inspiracao")
    
    # Passo B: Sincronizar Estoque Existente
    inventory.sync_stock()
    
    # Passo C: Analisar Inspiração e Gerar Conteúdo de Marketing
    marketing.analyze_inspiration()
    post_idea = marketing.generate_post_idea()

    # 4. Handoff para outra IA para refinamento criativo (Claude Code ou Gemini)
    logger.create_handoff(
        from_agent="Machina_Harness",
        to_agent="Claude_Code",
        task_description=f"Refine esta ideia de post para um tom artesanal e carioca: {post_idea}"
    )

    logger.log_action("Harness", "SHUTDOWN", "Ciclo de automação finalizado e auditado no Git.")

if __name__ == "__main__":
    run_harness()

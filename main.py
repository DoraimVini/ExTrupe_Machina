import os
from dotenv import load_dotenv
from harness.audit.logger import AuditLogger
from harness.agents.inventory import InventoryAgent
from harness.agents.atendimento import AgentAtendimento
from harness.agents.auditoria import AgentAuditoria
from harness.agents.orchestrator import OrchestratorAgent
from harness.audit import dashboard_gen

def run_harness():
    # 0. Carrega variáveis de ambiente
    load_dotenv()
    notion_token = os.getenv("NOTION_TOKEN")
    db_estoque = os.getenv("DATABASE_ID_ESTOQUE", "35205465-f1ab-80a8-8de4-e23cea9e7136")

    # 1. Inicializa o Auditor Central
    logger = AuditLogger()
    logger.log_action("Harness", "STARTUP", "Sistema Trupe BR Orchestrator Iniciado.")

    # 2. Inicializa os Agentes Especializados
    inventory = InventoryAgent(logger, database_id=db_estoque, notion_token=notion_token)
    atendimento = AgentAtendimento(logger, inventory_agent=inventory)
    auditoria = AgentAuditoria(logger)
    
    # 3. Inicializa o Orquestrador (Cérebro)
    orchestrator = OrchestratorAgent(logger, atendimento, inventory, auditoria)

    # 4. Simulação de Fluxo de Trabalho (Exemplos de Entrada)
    print("\n--- SIMULAÇÃO DE ENTRADAS ---\n")
    
    # Exemplo 1: Dúvida de Cliente (WhatsApp/DM)
    res1 = orchestrator.handle_input("WhatsApp", "Oi! Qual o material do top natural M e quanto custa?")
    print(f"RESPOSTA AGENTE: {res1}\n")

    # Exemplo 2: Venda na Feira
    res2 = orchestrator.handle_input("Feira", "Vendi 1 top_natural_M agora no dinheiro.")
    print(f"RESPOSTA AGENTE: {res2}\n")

    # Exemplo 3: Auditoria
    res3 = orchestrator.handle_input("Internal", "Gerar relatório de performance semanal.")
    report = auditoria.generate_weekly_report()
    print(f"RELATÓRIO GERADO: {report['recomendacao']}\n")

    logger.log_action("Harness", "SHUTDOWN", "Sessão finalizada.")
    
    # 5. Gera Dashboard Visual
    dashboard_gen.generate()

if __name__ == "__main__":
    run_harness()

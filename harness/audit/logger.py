import json
import datetime
import os
import subprocess
from pathlib import Path

class AuditLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.audit_file = self.log_dir / "audit_trail.json"
        
        if not self.audit_file.exists():
            with open(self.audit_file, "w", encoding="utf-8") as f:
                json.dump([], f)

    def log_action(self, agent_name, action_type, details, reasoning=None):
        """
        Registra uma ação realizada por um agente com rastreabilidade total.
        """
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "agent": agent_name,
            "action": action_type,
            "details": details,
            "reasoning": reasoning,
            "status": "logged"
        }
        
        with open(self.audit_file, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()
        
        print(f"[AUDIT] {agent_name} -> {action_type}: {details[:50]}...")
        
        # Auto-commit do log para garantir imutabilidade/histórico
        try:
            subprocess.run(["git", "add", str(self.audit_file)], capture_output=True)
            subprocess.run(["git", "commit", "-m", f"[AUDIT] {agent_name}: {action_type}"], capture_output=True)
        except Exception:
            pass # Silencioso se não houver git ou nada para comitar

    def create_handoff(self, from_agent, to_agent, task_description, priority="medium"):
        """
        Cria um arquivo .agent_task para comunicação entre IAs.
        """
        handoff_file = Path(f"{to_agent.lower()}_task.agent_task")
        task_data = {
            "from": from_agent,
            "to": to_agent,
            "priority": priority,
            "task": task_description,
            "created_at": datetime.datetime.now().isoformat(),
            "status": "pending"
        }
        
        with open(handoff_file, "w", encoding="utf-8") as f:
            json.dump(task_data, f, indent=4, ensure_ascii=False)
        
        self.log_action(from_agent, "CREATE_HANDOFF", f"Tarefa enviada para {to_agent}", reasoning=task_description)
        return handoff_file

if __name__ == "__main__":
    # Teste rápido
    logger = AuditLogger()
    logger.log_action("Antigravity", "SETUP", "AuditLogger inicializado com sucesso.")

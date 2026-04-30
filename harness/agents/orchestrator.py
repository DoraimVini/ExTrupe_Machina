class OrchestratorAgent:
    def __init__(self, logger, agent_atendimento, agent_estoque, agent_auditoria):
        self.logger = logger
        self.atendimento = agent_atendimento
        self.estoque = agent_estoque
        self.auditoria = agent_auditoria
        self.name = "ORCHESTRATOR"

    def handle_input(self, channel, content):
        """
        Ponto de entrada único para qualquer canal (WhatsApp, DM, Feira).
        """
        self.logger.log_action(self.name, "RECEIVE_INPUT", f"Canal: {channel} | Conteúdo: {content}")
        
        intent = self.identify_intent(content)
        self.logger.log_action(self.name, "INTENT_IDENTIFIED", intent)
        
        return self.route_to_agent(intent, content)

    def identify_intent(self, content):
        """
        Lógica de identificação de intenção (NLP simplificado ou LLM).
        """
        c = content.lower()
        if any(word in c for word in ["comprar", "quero", "preço", "valor", "frete", "tamanho", "disponível", "material", "quanto", "custa"]):
            return "AGENT_ATENDIMENTO"
        elif any(word in c for word in ["venda", "vendi", "estoque", "chegou", "produção"]):
            return "AGENT_ESTOQUE"
        elif any(word in c for word in ["auditoria", "relatório", "performance", "saúde"]):
            return "AGENT_AUDITORIA"
        else:
            return "AMBIGUOUS"

    def route_to_agent(self, agent_id, content):
        """
        Roteia o conteúdo para o agente especializado de forma sequencial.
        """
        if agent_id == "AGENT_ATENDIMENTO":
            return self.atendimento.process_request(content)
        elif agent_id == "AGENT_ESTOQUE":
            # Aqui poderíamos chamar métodos específicos do InventoryAgent
            self.logger.log_action(self.name, "ROUTING", "Encaminhando para AGENT_ESTOQUE")
            return "Encaminhado para processamento de estoque."
        elif agent_id == "AGENT_AUDITORIA":
            self.logger.log_action(self.name, "ROUTING", "Encaminhando para AGENT_AUDITORIA")
            return "Encaminhado para auditoria."
        elif agent_id == "AMBIGUOUS":
            self.logger.log_action(self.name, "ROUTING_WAIT", "Pedindo clarificação.")
            return "Oi! Não entendi bem se você quer ver o estoque ou falar sobre um pedido. Pode me explicar melhor?"
        else:
            return "Erro interno de roteamento."

class AgentAtendimento:
    def __init__(self, logger, inventory_agent):
        self.logger = logger
        self.inventory = inventory_agent
        self.name = "AgentAtendimento"
        self.templates = {
            "saudacao": "Oi! Aqui é a Trupe Br 🧶 Como posso te ajudar?",
            "indisponivel": "Essa peça acabou, mas posso te avisar quando chegar uma nova. Quer entrar na lista?",
            "escalada": "Vou chamar a Erika para te ajudar com isso, ela responde em breve!"
        }

    def process_request(self, user_input):
        self.logger.log_action(self.name, "PROCESS_REQUEST", f"Entrada: {user_input}")
        
        # Simulação de lógica de intenção interna do agente
        if any(word in user_input.lower() for word in ["preço", "valor", "quanto", "custa", "material", "tamanho"]):
            return self.handle_product_query(user_input)
        elif "frete" in user_input.lower():
            return self.handle_shipping_query(user_input)
        elif any(word in user_input.lower() for word in ["comprar", "pedido", "quero"]):
            return self.handle_order_intent(user_input)
        elif any(word in user_input.lower() for word in ["reclamar", "troca", "devolução", "errado"]):
            return self.escalate_to_human("Reclamação/Troca identificada")
        
        return self.templates["saudacao"]

    def handle_product_query(self, query):
        self.logger.log_action(self.name, "PRODUCT_QUERY", query)
        # Mock de resposta baseada no contexto da marca
        response = "Nossas peças são feitas em tricô manual (algodão e poliéster). "
        if "tamanho" in query.lower():
            response += "Temos tamanhos P, M e G. Qual você costuma usar?"
        return response

    def handle_shipping_query(self, query):
        self.logger.log_action(self.name, "SHIPPING_QUERY", query)
        return "Para calcular o frete, me passa o seu CEP? 🚚"

    def handle_order_intent(self, query):
        self.logger.log_action(self.name, "ORDER_INTENT", query)
        # Regra de Ouro: Nunca confirme sem checar estoque
        # Aqui o agente solicitaria o SKU para o usuário
        return "Legal! Qual peça você escolheu? Vou conferir se temos no estoque agora mesmo."

    def check_and_confirm_order(self, sku):
        stock_status = self.inventory.check_stock(sku)
        if stock_status > 0:
            self.logger.log_action(self.name, "ORDER_CONFIRMED", f"Estoque confirmado para {sku}")
            return f"Temos o {sku} disponível! Podemos fechar o pedido? O prazo de produção é de até 5 dias úteis."
        else:
            self.logger.log_action(self.name, "ORDER_FAILED", f"Sem estoque para {sku}")
            return self.templates["indisponivel"]

    def escalate_to_human(self, reason):
        self.logger.log_action(self.name, "HUMAN_ESCALATION", reason)
        return self.templates["escalada"]

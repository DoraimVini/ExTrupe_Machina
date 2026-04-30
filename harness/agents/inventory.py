import os
from notion_client import Client
from pathlib import Path

class InventoryAgent:
    def __init__(self, logger, database_id, notion_token):
        self.logger = logger
        self.database_id = database_id
        self.notion = Client(auth=notion_token)
        self.name = "InventoryAgent"

    def sync_stock(self):
        self.logger.log_action(self.name, "SYNC_START", f"Lendo database {self.database_id}")
        try:
            results = self.notion.databases.query(database_id=self.database_id).get("results", [])
            items_found = len(results)
            self.logger.log_action(self.name, "SYNC_COMPLETE", f"{items_found} itens encontrados.")
            return results
        except Exception as e:
            self.logger.log_action(self.name, "SYNC_ERROR", str(e))
            return []

    def check_stock(self, sku):
        """
        Verifica o estoque de um SKU específico (produto_cor_tamanho).
        """
        self.logger.log_action(self.name, "CHECK_STOCK", f"Verificando SKU: {sku}")
        # Simulação de consulta ao Notion por SKU
        # Em produção, faríamos uma query filtrando pelo campo 'SKU' ou 'Nome'
        return 5 # Mock de estoque disponível

    def register_sale(self, sku, quantity, channel="Feira"):
        """
        Registra uma venda e atualiza o estoque.
        """
        self.logger.log_action(self.name, "REGISTER_SALE", f"{quantity}x {sku} via {channel}")
        
        current_stock = self.check_stock(sku)
        new_stock = current_stock - quantity
        
        if new_stock < 0:
            self.logger.log_action(self.name, "SALE_ERROR", f"Estoque insuficiente para {sku}")
            return False
            
        # Alerta de estoque crítico
        if new_stock <= 2 and new_stock > 0:
            self.logger.log_action(self.name, "CRITICAL_STOCK_ALERT", f"SKU {sku} atingiu nível crítico: {new_stock}")
            
        if new_stock == 0:
            self.logger.log_action(self.name, "STOCK_ZERO_ALERT", f"SKU {sku} ESGOTADO. Bloqueando canais.")
            
        # Aqui enviaria o update para o Notion
        return True

    def register_production(self, sku, quantity):
        """
        Registra entrada de novas peças produzidas.
        """
        self.logger.log_action(self.name, "PRODUCTION_IN", f"Entrada de {quantity}x {sku}")
        # Update Notion logic here
        return True

    def register_inspiration_as_stock(self, inspiration_dir):
        """
        Lê a pasta de inspiração e cria entradas no Notion.
        """
        self.logger.log_action(self.name, "GALLERY_AUTO_INIT", f"Processando imagens em {inspiration_dir}")
        path = Path(inspiration_dir)
        extensions = ['*.jpeg', '*.jpg', '*.png']
        images = []
        for ext in extensions:
            images.extend(path.glob(ext))
        
        count = 0
        for img in images:
            name = img.stem
            try:
                self.notion.pages.create(
                    parent={"database_id": self.database_id},
                    properties={
                        "Nome": {"title": [{"text": {"content": f"Novo: {name}"}}]},
                        "Status": {"select": {"name": "Em Produção"}},
                        "Categoria": {"select": {"name": "Outros"}},
                        "Foto": {"rich_text": [{"text": {"content": f"file:///{img.absolute()}"}}]}
                    }
                )
                count += 1
            except Exception:
                pass
        
        self.logger.log_action(self.name, "GALLERY_COMPLETE", f"{count} novas peças registradas.")
        return count

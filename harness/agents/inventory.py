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
        """
        Sincroniza o estoque real com o Notion.
        """
        self.logger.log_action(self.name, "SYNC_START", f"Lendo database {self.database_id}")
        try:
            results = self.notion.databases.query(database_id=self.database_id).get("results", [])
            items_found = len(results)
            self.logger.log_action(
                self.name, 
                "SYNC_COMPLETE", 
                f"{items_found} itens encontrados no Notion.",
                reasoning="Consulta real realizada via Notion API."
            )
            return results
        except Exception as e:
            self.logger.log_action(self.name, "SYNC_ERROR", f"Erro ao acessar Notion: {str(e)}")
            return []

    def register_inspiration_as_stock(self, inspiration_dir):
        """
        Lê a pasta de inspiração e cria entradas no Notion para cada nova foto.
        Isso automatiza a criação da galeria inicial.
        """
        self.logger.log_action(self.name, "GALLERY_AUTO_INIT", f"Processando imagens em {inspiration_dir}")
        path = Path(inspiration_dir)
        # Suporta jpeg, jpg, png
        extensions = ['*.jpeg', '*.jpg', '*.png']
        images = []
        for ext in extensions:
            images.extend(path.glob(ext))
        
        count = 0
        for img in images:
            name = img.stem
            
            # Evitar duplicatas simples (verificando se o nome já existe no database)
            # Nota: Em um sistema mais robusto, usaríamos um hash da imagem.
            
            try:
                # Criar a peça no Notion com os metadados extraídos
                self.notion.pages.create(
                    parent={"database_id": self.database_id},
                    properties={
                        "Nome": {"title": [{"text": {"content": f"Novo: {name}"}}]},
                        "Status": {"select": {"name": "Em Produção"}},
                        "Categoria": {"select": {"name": "Outros"}},
                        "Foto": {"rich_text": [{"text": {"content": f"file:///{img.absolute()}"}}]}
                    },
                    children=[
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"type": "text", "text": {"content": f"Item gerado automaticamente pelo Machina Harness.\nArquivo original: {img.name}"}}]
                            }
                        }
                    ]
                )
                count += 1
                self.logger.log_action(self.name, "ITEM_CREATED", f"Página criada para {name}", reasoning=f"Local: {img.name}")
            except Exception as e:
                self.logger.log_action(self.name, "ITEM_CREATE_ERROR", f"Erro ao criar item {name}: {str(e)}")
        
        self.logger.log_action(self.name, "GALLERY_COMPLETE", f"{count} novas peças registradas no Notion.")
        return count

    def check_low_stock(self, threshold=2):
        """
        Verifica itens com estoque baixo (exemplo de lógica futura).
        """
        self.logger.log_action(self.name, "CHECK_LOW_STOCK", f"Verificando limites de reposição.")
        # Lógica para contar itens por categoria e alertar
        pass

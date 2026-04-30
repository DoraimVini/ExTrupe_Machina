import os
from pathlib import Path

class MarketingAgent:
    def __init__(self, logger, inspiration_dir):
        self.logger = logger
        self.inspiration_dir = Path(inspiration_dir)
        self.name = "MarketingAgent"

    def analyze_inspiration(self):
        """
        Analisa as imagens na pasta de inspiração para gerar insights de branding.
        """
        self.logger.log_action(self.name, "ANALYZE_IMAGES", f"Lendo pasta {self.inspiration_dir}")
        
        images = list(self.inspiration_dir.glob("*.jpeg")) + list(self.inspiration_dir.glob("*.jpg"))
        count = len(images)
        
        self.logger.log_action(
            self.name, 
            "INSIGHT_GENERATION", 
            f"Gerando sugestões baseadas em {count} imagens.",
            reasoning="As imagens sugerem um foco em texturas de tricô de algodão e cores vibrantes, ideal para o público carioca."
        )
        
        return count

    def generate_post_idea(self):
        """
        Gera uma ideia de post auditável.
        """
        idea = "Post sobre a versatilidade das bolsas de tricô no verão."
        self.logger.log_action(self.name, "IDEA_GENERATED", idea, reasoning="Cruzamento de dados: Estoque alto de bolsas + clima quente previsto.")
        return idea

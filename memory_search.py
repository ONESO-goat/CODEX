# memory_search.py


from typing import Dict, List


class MemorySearch:
    """Search through memories to find relevant context"""
    
    def __init__(self, user_memory):
        self.memory = user_memory
    
    def search_facts(self, query: str) -> List[Dict]:
        """
        Find facts relevant to current query
        Simple keyword matching for now
        """
        query_words = set(query.lower().split())
        relevant_facts = []
        copy = self.memory.get_current_user_info()
        for fact_name, fact_data in copy["facts"].items():
            # Check if any query word appears in fact name
            fact_words = set(fact_name.lower().split())
            
            if query_words & fact_words:  # Intersection
                relevant_facts.append({
                    "fact": fact_name,
                    "data": fact_data,
                    "relevance": len(query_words & fact_words) / len(query_words)
                })
        
        # Sort by relevance
        relevant_facts.sort(key=lambda x: x["relevance"], reverse=True)
        
        return relevant_facts[:3]  # Top 3 most relevant
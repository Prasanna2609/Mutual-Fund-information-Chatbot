"""
rag_chain.py
Orchestrates the full RAG pipeline from query to answer.
"""

import sys
from pathlib import Path
import torch
import torch.nn as nn

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_5_retrieval_pipeline.search_pipeline import run_retrieval_pipeline
from phase_6_llm_response.query_classifier import is_advisory_query, is_overview_query, is_relevant_query
from phase_6_llm_response.prompt_template import ADVISORY_REFUSAL_MESSAGE
from phase_6_llm_response.response_generator import ResponseGenerator

class RAGChain:
    def __init__(self):
        self.generator = ResponseGenerator()

    def query(self, user_query: str) -> dict:
        # 1. Catch Garbage / Irrelevant queries
        if not is_relevant_query(user_query):
            return {
                "answer": "I could not find any relevant information related to your query in the available sources.",
                "sources": []
            }

        # 2. Classify Advisory Query
        if is_advisory_query(user_query):
            return {
                "answer": ADVISORY_REFUSAL_MESSAGE,
                "sources": []
            }

        # 3. Handle Overview Queries (Metadata Only)
        if is_overview_query(user_query):
            from phase_5_retrieval_pipeline.search_pipeline import _get_retriever
            retriever = _get_retriever()
            schemes_dict = retriever.get_known_schemes_with_categories()
            
            # Group by category
            categories = {}
            for scheme, cat in schemes_dict.items():
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(scheme)
            
            answer = "Here is the complete list of mutual funds available in the dataset, grouped by category:\n\n"
            for cat, schemes in sorted(categories.items()):
                answer += f"**{cat}**\n"
                for s in sorted(schemes):
                    answer += f"- {s}\n"
                answer += "\n"
                
            return {
                "answer": answer.strip(),
                "sources": [] 
            }
            
        # 4. Handle AMC Only / Specific Filter Queries
        from phase_6_llm_response.query_classifier import is_amc_only_query
        detected_amc = is_amc_only_query(user_query)
        
        # 5. Retrieve Context
        try:
            # If it's an AMC only query, we can bias the retrieval or use it as is
            context_results = run_retrieval_pipeline(user_query)
        except Exception as e:
            return {"answer": f"Retrieval error: {e}", "sources": []}

        # 6. Generate Answer
        if detected_amc and not any(detected_amc in (c.get("amc") or "").lower() for c in context_results):
            # Fallback for AMC search if retrieval failed to find specific AMC chunks
            pass # Continue to LLM but LLM might say it doesn't know.
            
        answer = self.generator.generate_response(user_query, context_results)
        
        # 7. Map unique sources from chunks
        sources = []
        # No sources if response is a refusal or fallback
        if "I can only provide factual information" not in answer and \
           "I could not find any relevant information" not in answer:
            
            seen_schemes = set()
            for chunk in context_results:
                scheme_name = chunk.get("scheme_name")
                url = chunk.get("source_url")
                
                if scheme_name and url and scheme_name not in seen_schemes:
                    if url not in ["Dataset Overview", "No source available", "No source link available."]:
                        sources.append({
                            "scheme_name": scheme_name,
                            "url": url
                        })
                        seen_schemes.add(scheme_name)

        return {
            "answer": answer,
            "sources": sources
        }



if __name__ == "__main__":
    chain = RAGChain()
    
    # Test queries
    factual_q = "What is the NAV of SBI Bluechip Fund?"
    print(f"\nUser: {factual_q}")
    print(f"Bot: {chain.query(factual_q)}")

    advisory_q = "Which fund is best for me?"
    print(f"\nUser: {advisory_q}")
    print(f"Bot: {chain.query(advisory_q)}")
    
    garbage_q = "hello world"
    print(f"\nUser: {garbage_q}")
    print(f"Bot: {chain.query(garbage_q)}")

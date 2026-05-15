from typing import TypedDict, List, Dict, Any, Annotated, Sequence
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
import operator

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    repo_id: str
    context: Dict[str, Any]
    current_task: str
    findings: List[str]

class AetherOrchestrator:
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        workflow = StateGraph(AgentState)

        # Define nodes
        workflow.add_node("researcher", self._researcher_node)
        workflow.add_node("analyst", self._analyst_node)
        workflow.add_node("router", self._router_node)

        # Define edges
        workflow.set_entry_point("router")
        workflow.add_conditional_edges(
            "router",
            self._route_decision,
            {
                "research": "researcher",
                "analyze": "analyst",
                "end": END
            }
        )
        workflow.add_edge("researcher", "router")
        workflow.add_edge("analyst", "router")

        return workflow.compile()

    def _router_node(self, state: AgentState):
        # Decide what to do next based on messages
        prompt = f"""
        You are the Aether Orchestrator. 
        Current Task: {state['current_task']}
        Findings so far: {state['findings']}
        
        Decide if we need more 'research' (finding code) or 'analyze' (explaining/reasoning) or if we are 'end' (done).
        """
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return {"messages": [response]}

    def _route_decision(self, state: AgentState):
        content = state["messages"][-1].content.lower()
        if "research" in content:
            return "research"
        elif "analyze" in content:
            return "analyze"
        return "end"

    def _researcher_node(self, state: AgentState):
        # This node would interface with the Semantic Search and Graph engines
        # Mocking for now
        finding = f"Found relevant code blocks in {state['repo_id']} using semantic search."
        return {
            "findings": [finding],
            "messages": [AIMessage(content=f"Researcher: {finding}")]
        }

    def _analyst_node(self, state: AgentState):
        # This node would reason about the findings
        analysis = f"Analyzing the relationship between components based on research findings."
        return {
            "findings": [analysis],
            "messages": [AIMessage(content=f"Analyst: {analysis}")]
        }

    async def run(self, repo_id: str, query: str):
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "repo_id": repo_id,
            "context": {},
            "current_task": query,
            "findings": []
        }
        final_state = await self.workflow.ainvoke(initial_state)
        return final_state

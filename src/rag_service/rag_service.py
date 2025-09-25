from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.schema import BaseRetriever

from src.settings.settings import Settings
from src.rag_service.utils import format_docs


class RAGService:
    __slots__ = (
        "retriever",
        "llm_model",
        "summary_mem",
        "rewrite_prompt",
        "history_aware_retriever",
        "answer_prompt",
        "rag_chain",
    )

    def __init__(self, retriever: BaseRetriever, settings: Settings):
        self.retriever = retriever

        self.llm_model = ChatOpenAI(
            model=settings.MAIN_MODEL,
            temperature=0,
        )
        rewriter_llm = ChatOpenAI(
            model=settings.RETRIEVER_MODEL,
            temperature=0,
        )

        self.summary_mem = ConversationSummaryBufferMemory(
            llm=rewriter_llm, return_messages=True, memory_key="chat_history"
        )

        # todo: almost looks like a constant, how to store properly?
        self.rewrite_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Rewrite the user query into a standalone question "
                    "using the chat history if needed.",
                ),
                ("placeholder", "{chat_history}"),
                ("user", "{input}"),
            ]
        )

        self.history_aware_retriever = create_history_aware_retriever(
            rewriter_llm, self.retriever, self.rewrite_prompt
        )
        self.answer_prompt = ChatPromptTemplate.from_messages(
            [
                ("placeholder", "{chat_history}"),
                ("user", "{input}"),
                ("system", "Context:\n{context}"),
            ]
        )

        self.rag_chain = create_retrieval_chain(
            self.history_aware_retriever | RunnableLambda(format_docs),
            self.answer_prompt | self.llm_model | StrOutputParser(),
        )

    def get_llm_response(self, query: str) -> str:
        chat_history = self.summary_mem.load_memory_variables({})["chat_history"]

        answer = self.rag_chain.invoke({"input": query, "chat_history": chat_history})
        self.summary_mem.save_context({"input": query}, {"output": answer["answer"]})

        return answer["answer"]

from langchain_core.messages import HumanMessage
from langchain_core.prompts import load_prompt

from agents.config import get_llm_openrouter, get_llm_gemini, AgentLogger
from agents.config.settings import DOC_READER_MODEL, GEMINI_MODEL
from shared.schemas.upload_doc import UploadedDocument
from shared.schemas.expense import DocsExtractionSchema
from shared.utils.docs_preprocessor import DocumentPreprocessor

class DocReaderAgent:
    def __init__(self, temperatura:float = 0, session_id: int = None):
        self.llm = get_llm_gemini(model=GEMINI_MODEL,temperature=temperatura)
        #self.llm = get_llm_openrouter(model=DOC_READER_MODEL, temperature=temperatura)
        self.session_id = session_id
        self._local_observer = AgentLogger()

        self.prompt = load_prompt("resources/prompts/doc_reader_agent.yaml").format()
        self.preprocessor = DocumentPreprocessor()
        self.structured_llm = (self.llm.with_structured_output(DocsExtractionSchema))

    def extractor(self, documentos: list[UploadedDocument])-> DocsExtractionSchema:
        content = self.preprocessor.build_multimodal_content(documentos,self.prompt)
        response = self.structured_llm.invoke(
            [HumanMessage(content=content)],
            config={
                "callbacks": [self._local_observer]
            }
        )
        #response = self.llm.invoke([HumanMessage(content=content)])

        return response
        

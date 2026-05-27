import streamlit as st

from agents.doc_reader_agent import DocReaderAgent
from shared.schemas.upload_doc import UploadedDocument
from shared.repository import ExpenseRepository
from shared.storage import get_db


class UploadsPage:
    def __init__(self,session_id:int):
        self.session_id = session_id
        self.agente =  DocReaderAgent(session_id=session_id)
        db = get_db()
        self.expense_repository = ExpenseRepository(db)

    def render(self):
        st.title(f"You have selected {st.session_state['selected']}")
        upload_file = st.file_uploader(label="Envie os arquivos", accept_multiple_files=True, type=["pdf", "png", "jpg", "jpeg"])

        if upload_file:

            if st.button("Processar", type="primary"):

                documento = [UploadedDocument(
                        filename=file.name,
                        mime_type=file.type,
                        content=file.getvalue()
                    )
                    for file in upload_file
                ]
                
                response = self.agente.extractor(documento)
                
                if response:
                    st.success("Dados extraidos com sucesso")
                    st.json(response.model_dump())

                    total_despesas = len(response.despesas)

                    my_bar = st.progress(0)

                    for indice, despesa in enumerate(response.despesas, start=1):
                        self.expense_repository.create_expense(
                            session_id=self.session_id,
                            data=despesa.data,
                            descricao=despesa.descricao,
                            categoria=despesa.categoria,
                            valor=despesa.valor,
                        )

                        percentual = int((indice/total_despesas)*100)
                        my_bar.progress(percentual, text=f"Salvando despesa {indice}/{total_despesas}")
                    
                    
                        
                else:
                    st.error("Problema na extração dos dados")





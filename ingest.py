from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import os

# ---- Set up embeddings (no torch required) ----
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ---- Path to your folder of PDFs ----
pdf_folder_path = "books"

docs = []
for filename in os.listdir(pdf_folder_path):
    if filename.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(pdf_folder_path, filename))
        docs.extend(loader.load())

# ---- Split the texts ----
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# ---- Create vector store ----
vectorstore = FAISS.from_documents(splits, embeddings)
vectorstore.save_local("vectorstore")


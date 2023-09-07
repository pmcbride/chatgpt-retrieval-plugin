from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict
from enum import Enum


class Source(str, Enum):
    email = "email"
    file = "file"
    chat = "chat"


class ChatMetadata(BaseModel):
    """
    Metadata specific to chat conversations.
    """

    conversation_id: str = Field(..., description="The unique identifier for the conversation")
    message_id: str = Field(
        ..., description="The unique identifier for the message within the conversation"
    )
    author_role: str = Field(..., description="The role of the author (e.g., 'user', 'assistant')")
    create_time: str = Field(..., description="The timestamp when the message was created")
    update_time: Optional[str] = Field(
        None, description="The timestamp when the message was last updated"
    )
    subject: Optional[str] = Field(None, description="The subject or topic of the conversation")
    keywords: Optional[List[str]] = Field(
        None, description="Keywords for easier search and retrieval"
    )
    status: Optional[str] = Field(
        None, description="The status of the message (e.g., 'finished_successfully')"
    )
    extra_metadata: Optional[Dict] = Field(None, description="Any additional metadata")


class DocumentMetadata(BaseModel):
    """
    Metadata associated with a document.
    """

    source: str = Field(
        ..., description="The source of the document, e.g., 'email', 'file', 'chat'"
    )
    source_id: Optional[str] = Field(None, description="Unique identifier for the source")
    url: Optional[str] = Field(None, description="URL related to the document, if applicable")
    created_at: Optional[str] = Field(None, description="Timestamp when the document was created")
    author: Optional[str] = Field(None, description="The author of the document, if applicable")
    chat_metadata: Optional[ChatMetadata] = Field(
        None, description="Additional metadata specific to chat conversations"
    )


class DocumentChunkMetadata(DocumentMetadata):
    document_id: Optional[str] = None


class DocumentChunk(BaseModel):
    id: Optional[str] = None
    text: str
    metadata: DocumentChunkMetadata
    embedding: Optional[List[float]] = None


class DocumentChunkWithScore(DocumentChunk):
    score: float


class Document(BaseModel):
    """
    Represents a document to be upserted into the database.
    """

    id: Optional[str] = Field(None, description="Unique identifier for the document")
    text: str = Field(..., description="The text content of the document")
    metadata: DocumentMetadata = Field(..., description="Metadata associated with the document")


class DocumentWithChunks(Document):
    chunks: List[DocumentChunk]


class DocumentMetadataFilter(BaseModel):
    document_id: Optional[str] = None
    source: Optional[Source] = None
    source_id: Optional[str] = None
    author: Optional[str] = None
    start_date: Optional[str] = None  # any date string format
    end_date: Optional[str] = None  # any date string format


class Query(BaseModel):
    query: str
    filter: Optional[DocumentMetadataFilter] = None
    top_k: Optional[int] = 3


class QueryWithEmbedding(Query):
    embedding: List[float]


class QueryResult(BaseModel):
    query: str
    results: List[DocumentChunkWithScore]

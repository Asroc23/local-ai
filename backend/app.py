# ==========================================
# APLICACIÓN
# ==========================================

from backend.lmstudio import LMStudioClient
from backend.database import Database
from backend.conversation import ConversationService
from backend.memory import Memory
from backend.memory_service import MemoryService
from backend.summary_service import SummaryService
from backend.memory_extractor import MemoryExtractor
from backend.llm_service import LLMService
from backend.command_service import CommandService
from backend.file_service import FileService
from backend.document_service import DocumentService
from backend.conversation_file_service import ConversationFileService


class LocalAI:

    def __init__(self, system_message):

        self.system_message = system_message

        # ==========================================
        # LM STUDIO
        # ==========================================

        self.client = LMStudioClient()

        # ==========================================
        # DATABASE
        # ==========================================

        self.db = Database()

        # ==========================================
        # CONVERSATION SERVICE
        # ==========================================

        self.conversation = ConversationService(
            self.db
        )

        # ==========================================
        # LLM SERVICE
        # ==========================================

        self.llm_service = LLMService(
            self.client
        )

        # ==========================================
        # MEMORY
        # ==========================================

        self.memory = Memory(
            self.db,
            self.system_message,
            self.client
        )

        # ==========================================
        # MEMORY SERVICE
        # ==========================================

        self.memory_service = MemoryService(
            self.memory
        )

        # ==========================================
        # SUMMARY SERVICE
        # ==========================================

        self.summary_service = SummaryService(
            self.memory
        )

        # ==========================================
        # COMMAND SERVICE
        # ==========================================

        self.command_service = CommandService(
            self.conversation,
            self.memory_service,
            self.system_message
        )

        # ==========================================
        # MEMORIA AUTOMÁTICA
        # ==========================================

        self.memory_extractor = MemoryExtractor(
            self.client
        )

        # ==========================================
        # FILE SERVICE
        # ==========================================

        self.file_service = FileService()

        # ==========================================
        # DOCUMENT SERVICE
        # ==========================================

        self.document_service = DocumentService()

        self.conversation_file_service = ConversationFileService()
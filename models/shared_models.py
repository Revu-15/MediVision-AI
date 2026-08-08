from models.florence2 import FlorenceModel
from models.image_router import ImageRouter
from models.model_dispatcher import ModelDispatcher
from models.ai_report_engine import AIReportEngine
from utils.pdf_generator import PDFGenerator

# Shared models (loaded only once)

florence = FlorenceModel()

router = ImageRouter()

dispatcher = ModelDispatcher()

report_engine = AIReportEngine()

pdf_generator = PDFGenerator()
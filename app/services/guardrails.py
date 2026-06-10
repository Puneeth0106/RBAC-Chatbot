from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from app.services.logger import logger,get_extra
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client= OpenAI()

# We only use regex/checksum pattern recognizers (no PERSON/NER), so the small
# spaCy model is enough — identical tokenization without the ~420 MB of word
# vectors the large model ships. Build the engine and pass it to AnalyzerEngine.
nlp_engine = NlpEngineProvider(nlp_configuration={
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
}).create_engine()

analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
anonymizer = AnonymizerEngine()

PII_ENTITIES = ['CREDIT_CARD', 'US_SSN', 'EMAIL_ADDRESS', 'PHONE_NUMBER','IBAN_CODE', 'US_BANK_NUMBER']


def scrub_pii(text: str) -> str:
    results= analyzer.analyze(text=text, language='en',entities= PII_ENTITIES)
    if not results:
        return text
    anonymized= anonymizer.anonymize(
        text= text,
        analyzer_results= results,
        operators={"DEFAULT": OperatorConfig("replace", {"new_value": "[REDACTED]"})}
    )
    return anonymized.text


def is_toxic(text:str)->bool:
    try:
        resp = client.moderations.create(model="omni-moderation-latest", input=text)
        return resp.results[0].flagged
    except Exception:
        logger.warning("moderation_unavailable", extra=get_extra())
        return False





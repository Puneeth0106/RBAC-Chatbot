from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from app.services.logger import logger,get_extra
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client= OpenAI()

analyzer= AnalyzerEngine()
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





if __name__ == "__main__":
    text_to_anonymize = "His name is Mr. Jones and his phone number is 212-555-5555"
    analyzer_results= analyzer.analyze(text_to_anonymize,entities=['PHONE_NUMBER'],language='en')

    print(analyzer_results)


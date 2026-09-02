import logging
import json
import re

REDACT_PATTERNS = [re.compile(p, re.I) for p in [r".*(_KEY|_TOKEN)$", r"PASSWORD", r"SECRET", r"AUTHORIZATION"]]

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        data = {"message": message, "logger": record.name, "level": record.levelname}
        # Include extra fields except those matching redaction patterns
        for k, v in record.__dict__.items():
            if k in ("msg", "args", "levelname", "levelno", "name", "msg", "args"):
                continue
            try:
                if any(p.search(k) for p in REDACT_PATTERNS):
                    data[k] = "***REDACTED***"
                else:
                    # attempt json-serializable
                    data[k] = v
            except Exception:
                data[k] = str(v)
        return json.dumps(data)


def setup_logging(level: int = logging.INFO) -> None:
    root = logging.getLogger()
    if not root.handlers:
        handler = logging.StreamHandler()
        formatter = JSONFormatter()
        handler.setFormatter(formatter)
        root.addHandler(handler)
    root.setLevel(level)

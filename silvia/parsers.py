
import json

from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser


class StrictJSONParser(JSONParser):
    MAX_BODY_SIZE = 4096

    def parse(self, stream, media_type=None, parser_context=None):
        try:
            raw_data = stream.read(self.MAX_BODY_SIZE + 1)

            if not isinstance(raw_data, bytes):
                raise ParseError({"error": "invalid_request"})

            if len(raw_data) > self.MAX_BODY_SIZE:
                raise ParseError({"error": "invalid_request"})

            decoded = raw_data.decode("utf-8")

            data = json.loads(
                decoded,
                object_pairs_hook=self.reject_duplicate_keys,
            )

            if not isinstance(data, dict):
                raise ParseError({"error": "invalid_request"})

            return data

        except ParseError:
            raise

        except (
            UnicodeDecodeError,
            json.JSONDecodeError,
            ValueError,
            RecursionError,
        ):
            raise ParseError({"error": "invalid_request"})

    @staticmethod
    def reject_duplicate_keys(pairs):
        data = {}

        for key, value in pairs:
            if key in data:
                raise ValueError("Duplicate JSON key.")

            data[key] = value

        return data

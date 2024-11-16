import ast

from openai import OpenAI

from config import config
from misc import retry_on_failure


class OpenAIManager:
    def __init__(self):
        self._openai_manager = OpenAI(api_key=config.OPENAI_KEY.get_secret_value())

    @retry_on_failure()
    def detect_swear_words(self, text: str) -> list:
        completion = self._openai_manager.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": config.OPENAI_SWEAR_CHECKER_PROMPT},
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.0
        )
        answer = completion.choices[0].message.content
        swear_words = ast.literal_eval(answer)
        return swear_words

    @retry_on_failure()
    def generate_auto_reply(self, post_text: str, comment_text: str) -> str:
        content = f"Post text: {post_text}\n\nComment text: {comment_text}"

        completion = self._openai_manager.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": config.OPENAI_REPLY_GEN_PROMPT},
                {
                    "role": "user",
                    "content": content
                }
            ],
            temperature=1
        )
        answer = completion.choices[0].message.content
        return answer


openai_manager = OpenAIManager()

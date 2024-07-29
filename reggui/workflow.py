from regdbot.brain import RegDBot
from regdbot.brain.utils import extract_code_from_markdown

class Reggie:
    def __init__(self, model='gpt', language: str = "en_US"):
        self.bot = RegDBot(model=model, memory_db_url='sqlite:///memory.sqlite')
        self.bot.set_language(language)
        self.bot.ask(self.bot.context, None)
        # self.bot.set_context()

    def say(self, text):
        self.bot.say(text)

    def ask(self, question: str, table: str) -> str:
        """
        Ask Reggie a question.
        :param question: any textual prompt
        :param table: the table name
        :return:
        """
        try:
            resp = self.bot.ask(question, table)
        except KeyError:
            if table:
                resp =  f"Table *{table}* not found in the database. Please try again."
            else:
                resp = "No table specified. Please try again."
        return resp#, self.bot.last_response

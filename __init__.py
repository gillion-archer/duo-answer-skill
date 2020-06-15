from mycroft import MycroftSkill, intent_file_handler


class DuoAnswer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('answer.duo.intent')
    def handle_answer_duo(self, message):
        self.speak_dialog('answer.duo')


def create_skill():
    return DuoAnswer()


from aider.models import Model

from .ask_coder import AskCoder
from .base_coder import Coder
from .senior_prompts import SeniorPrompts


class SeniorCoder(AskCoder):
    edit_format = "senior"
    gpt_prompts = SeniorPrompts()

    def reply_completed(self):
        content = self.partial_response_content

        kwargs = dict(self.original_kwargs)
        kwargs["edit_format"] = self.main_model.junior_edit_format
        kwargs["suggest_shell_commands"] = False

        junior_coder = Coder.create(
            main_model=Model(self.main_model.junior_model_name),
            io=self.io,
            **kwargs,
        )
        junior_coder.run(with_message=content, preproc=False)
        self.move_back_cur_messages("I made those changes to the files.")
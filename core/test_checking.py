from .models import Test, UsersTest, IncorrectAnswers, Question
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.db import transaction
from django.utils import timezone


class TestChecking:
    test: Test
    user: get_user_model()
    request: HttpRequest
    user_test: UsersTest

    def __init__(self, user, test, request) -> None:
        self.user = user
        self.test = test
        self.request = request

        session = self.request.session
        if self.get_data is None:
            self.user_test = UsersTest.objects.create(user=self.user, test=self.test)
            session[f'test_{self.test.id}'] = {
                'id': self.user_test.id,
                'actions': [
                    {'question': question.id, 'answer': 0} \
                    for question in self.test.questions.all()
                ]
            }
        else:
            self.user_test = UsersTest.objects. \
                get(id=session[f'test_{self.test.id}']['id'])

    def set_answer(self, question_id, answer) -> bool:
        if self.get_data:
            actions = self.get_data['actions']
            for action in actions:
                if int(action['question']) == int(question_id):
                    action['answer'] = answer
                    self.request.session.modified = True
                    return True
        return False

    @transaction.atomic
    def complete_test(self) -> UsersTest or None:
        session = self.request.session
        if self.get_data is not None:
            actions = self.get_data['actions']
            for action in actions:
                question = Question.objects.get(id=action['question'])
                if question.true_answer != int(action['answer']):
                    IncorrectAnswers.objects.create(
                        user_test=self.user_test,
                        question=question,
                        answer=action['answer']
                    )
            self.user_test.status = UsersTest.COMPLETED
            self.user_test.save()
            del session[f'test_{self.test.id}']
            session.modified = True
            return self.user_test
        return None

    @property
    def get_data(self) -> dict or None:
        return self.request.session.get(f'test_{self.test.id}', None)

    @property
    def left_time(self):
        now = timezone.now()
        run_away_time = now - self.user_test.created_at
        left_time = self.test.time - int(run_away_time.total_seconds())
        return left_time

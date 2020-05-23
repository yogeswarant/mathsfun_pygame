import pygame
from mathsfunlib.qgenerator import generate_questions
from mathsfunlib.qgenerator import QType
from pygame import Rect

pygame.init()

SIZE = 500, 200
screen = pygame.display.set_mode(SIZE)

RED = (168, 50, 62)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
GREEN = (18, 128, 23)

SECONDS_EVENT = pygame.USEREVENT + 1
QUESTION_EVENT = pygame.USEREVENT + 2

ONE_SECOND_MS = 1000
ONE_QUESTION_MS = 10000
ONE_QUESTION_SECONDS = int(ONE_QUESTION_MS / 1000)

question_font = pygame.font.Font('freesansbold.ttf', 32)
timer_font = pygame.font.Font('freesansbold.ttf', 18)
status_font = pygame.font.Font('freesansbold.ttf', 12)


class Quiz(object):
    def __init__(self, questions):
        self.questions = questions
        self.attempted_count = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.current_question = None
        self.user_input = ''
        self.remaining_time = 0
        self.eoq = False

    def next_question(self):
        try:
            self.current_question = next(self.questions)
            self.user_input = ''
            self.attempted_count += 1
        except StopIteration:
            self.eoq = True
            print(self.status())

        self.reset_timer()
        return self.current_question

    def check_answer(self):
        try:
            answer = int(self.user_input)
            if answer == self.current_question.get_answer():
                self.correct_count += 1
                return "Correct!"
        except Exception:
            # no exception handling required
            pass

        self.wrong_count += 1
        return "Wrong!"

    def answer(self, user_input):
        if user_input == 'backspace':
            self.user_input = self.user_input[:-1]
        else:
            self.user_input += user_input

    def status(self):
        return "Total: {} Correct: {} Wrong: {}".format(self.attempted_count, self.correct_count,
                                                        self.wrong_count)

    def reset_timer(self):
        self.remaining_time = ONE_QUESTION_SECONDS

    def tick_down(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1

    def get_remaining_time(self):
        return self.remaining_time

    def has_ended(self):
        return self.eoq == True

    def get_user_input(self):
        return self.user_input

    def get_result(self):
        return {'total': self.attempted_count,
                'correct': self.correct_count,
                'wrong': self.wrong_count}

    def end(self):
        self.eoq = True


def main():
    qtypes = [QType.MULTIPLICATION, QType.XMULTIPLICATION, QType.DIVISION, QType.XDIVISION]
    questions = generate_questions(range(6, 12), qtypes)
    pygame.time.set_timer(SECONDS_EVENT, ONE_SECOND_MS)
    pygame.time.set_timer(QUESTION_EVENT, ONE_QUESTION_MS)
    end_rect = Rect(75, 150, 50, 20)
    pygame.display.set_caption("Multiplication tables speed test")
    quiz = Quiz(questions)
    question = quiz.next_question()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif quiz.has_ended():
                continue
            elif event.type == QUESTION_EVENT:
                quiz.check_answer()
                question = quiz.next_question()
                pygame.time.set_timer(QUESTION_EVENT, ONE_QUESTION_MS)
            elif event.type == SECONDS_EVENT:
                quiz.tick_down()
                pygame.time.set_timer(SECONDS_EVENT, ONE_SECOND_MS)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    quiz.check_answer()
                    question = quiz.next_question()
                    # reset the existing question event
                    pygame.time.set_timer(QUESTION_EVENT, 0)
                    pygame.time.set_timer(QUESTION_EVENT, ONE_QUESTION_MS)
                elif event.key == pygame.K_BACKSPACE:
                    key = pygame.key.name(event.key)
                    quiz.answer(key)
                else:
                    key = pygame.key.name(event.key)
                    if key.isnumeric():
                        quiz.answer(key)
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if end_rect.collidepoint(pos):
                    quiz.end()

        screen.fill(GRAY)

        if quiz.has_ended():
            result = quiz.get_result()
            result_x = 150
            result_y = 50
            status = "Total: {} Correct: {correct} Wrong: {wrong}".format((result['total'] - 1), **result)
            text = timer_font.render(status, True, BLACK)
            screen.blit(text, (result_x, result_y))
        else:
            text = timer_font.render("Remaining: {} seconds".format(quiz.get_remaining_time()),
                                     True, BLACK)
            screen.blit(text, (210, 20))

            iquestion = str(question).replace('_', quiz.get_user_input() + '_')
            text = question_font.render(iquestion, True, BLACK)
            screen.blit(text, (180, 90))

            result = quiz.get_result()
            total = result['total'] - 1
            status = "Total: {} Correct: {correct} Wrong: {wrong}".format(total, **result)
            text = status_font.render(status, True, BLACK)
            screen.blit(text, (300, 150))

            pygame.draw.rect(screen, BLACK, end_rect, 2)
            text = status_font.render("END", True, BLACK)
            screen.blit(text, (88, 155))

        pygame.display.flip()
        pygame.display.update()


if __name__ == '__main__':
    main()

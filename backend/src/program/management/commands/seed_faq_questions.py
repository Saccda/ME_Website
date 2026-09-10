"""File the questions an ME applicant usually asks, without answering them.

A question is safe to guess at; an answer is not. Tuition, entry requirements,
intake dates and credit counts are facts about this program, and inventing them
on a public university page would be worse than leaving the page empty. So each
entry arrives with its answer blank and unpublished, and cannot reach the site
until someone writes it -- `FaqItem.visible()` requires an answer as well as the
published tick.

Existing questions are matched on their text and left alone, so running this
again will never overwrite an answer.

    python manage.py seed_faq_questions
"""

from django.core.management.base import BaseCommand

from program.models import FaqItem

# (category, question)
QUESTIONS = [
    ("admissions", "What are the entry requirements for the ME program?"),
    ("admissions", "When does the application period open and close?"),
    ("admissions", "What subjects does the entrance examination cover?"),
    ("admissions", "Can I apply if I studied a non-science track at high school?"),
    ("admissions", "How many students are admitted each year?"),
    ("admissions", "How do I submit my application?"),
    ("program", "How long is the ME program?"),
    ("program", "What are DMP, TES, MAS and ECM, and do I have to choose one?"),
    ("program", "When do I choose my area of focus?"),
    ("program", "Is the program accredited?"),
    ("learning", "What language is the program taught in?"),
    ("learning", "How much of the program is practical rather than theory?"),
    ("learning", "Is there an internship or industry placement?"),
    ("learning", "What is the class schedule like?"),
    ("learning", "Can I do research as an undergraduate?"),
    ("facilities", "What equipment will I actually get to use?"),
    ("facilities", "Can I use the laboratory outside class hours?"),
    ("facilities", "Where is the ME laboratory located?"),
    ("careers", "What jobs do ME graduates go into?"),
    ("careers", "Does the program help with job placement?"),
    ("careers", "Which companies do you work with?"),
    ("careers", "Can I continue to a master's degree after this program?"),
    ("support", "How much does the program cost?"),
    ("support", "Are scholarships available?"),
    ("support", "Is there support for students who need to work while studying?"),
    # Asked by students who are still deciding whether engineering is for them,
    # rather than by applicants who have already chosen it.
    ("program", "What is the difference between mechanical engineering and the other engineering programs at RUPP?"),
    ("program", "Do I need to be good at mathematics to study mechanical engineering?"),
    ("program", "Will I learn to use CAD and other engineering software?"),
    ("program", "Do I need my own laptop, and what should it be able to run?"),
    ("learning", "How much programming is involved?"),
    ("learning", "What does a typical week look like?"),
    ("learning", "How are students assessed — examinations, projects, or both?"),
    ("learning", "What happens in the final-year project?"),
    ("facilities", "Do students work on real equipment or only simulations?"),
    ("facilities", "Can students propose their own laboratory projects?"),
    ("careers", "Can I work abroad with this degree?"),
    ("careers", "What do students do during the summer between years?"),
    ("admissions", "Can I transfer credits from another university or program?"),
    ("admissions", "Is there a preparatory or foundation year before the program?"),
    ("support", "Is accommodation available for students from the provinces?"),
    ("support", "Who do I talk to if I am struggling with a subject?"),
]


class Command(BaseCommand):
    help = (
        "File the questions applicants commonly ask, with blank answers, ready "
        "to be written in Wagtail. Never overwrites an existing question."
    )

    def handle(self, *args, **options):
        created = 0
        skipped = 0
        highest = FaqItem.objects.count()

        for index, (category, question) in enumerate(QUESTIONS):
            if FaqItem.objects.filter(question=question).exists():
                skipped += 1
                continue
            FaqItem.objects.create(
                sort_order=highest + index + 1,
                category=category,
                question=question,
                answer="",
                is_published=False,
            )
            created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Filed {created} question(s); left {skipped} already present."
            )
        )
        self.stdout.write(
            "\nNone of these are on the site yet, and none can be until they are"
            "\nanswered: a question with an empty answer is withheld whatever the"
            "\npublished tick says."
            "\n\nIn Wagtail, under Snippets > FAQs: write the answer, tick"
            "\nPublished, and it appears. Delete any question the program would"
            "\nrather not invite.\n"
        )

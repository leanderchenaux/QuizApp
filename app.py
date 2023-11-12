from collections import namedtuple
from random import shuffle

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# NamedTuple für eine Quiz-Frage
Question = namedtuple('Question', ['id', 'question', 'options', 'correct_answer'])

# Beispiel-Fragen für das Quiz
questions = [
    Question(id=1, question='Was ist die Hauptstadt von Deutschland?', options=['Berlin', 'Madrid', 'Paris', 'Rom'], correct_answer='Berlin'),
    Question(id=2, question='In welcher Programmiersprache ist Flask geschrieben?', options=['Java', 'Python', 'C#', 'JavaScript'], correct_answer='Python')
]

# Prozedur zum Mischen der Quiz-Fragen
def shuffle_questions(questions):
    shuffle(questions)

# Lambda-Ausdruck zur Überprüfung der Antwort
check_answer = lambda user_answer, correct_answer: user_answer == correct_answer

# Lambda-Ausdruck zur Berechnung des Punktestands für jede Frage
calculate_question_score = lambda user_answer, correct_answer: 1 if user_answer == correct_answer else 0

# Lambda-Ausdruck zur Berechnung des Gesamtpunktestands
calculate_total_score = lambda user_answers, questions: sum(calculate_question_score(user_answers[str(q.id)], q.correct_answer) for q in questions)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        user_answers = request.form.to_dict()
        score = calculate_total_score(user_answers, questions)
        return render_template('quiz.html', questions=questions, score=score)
    shuffle_questions(questions)  # Mische die Fragen vor dem Anzeigen
    return render_template('quiz.html', questions=questions, score=0)  # Initialisieren des Punktestands

if __name__ == '__main__':
    app.run(debug=True)


# def calculate_quiz_score(questions, user_answers):
#     # Initialisierung des Punktestands
#     score = 0
#
#     # Schleife durch die Fragen
#     for question in questions:
#         question_id = str(question.id)  # Änderung hier
#         if question_id in user_answers and user_answers[question_id] == question.correct_answer:
#             # Die Antwort ist korrekt, erhöhe den Punktestand
#             score += 1
#
#     # Der Punktestand ist das Endergebnis
#     return score
#
# # Funktionales Teilstück: Fragen anzeigen
# def display_questions(questions):
#     for question in questions:
#         print(f"Frage {question['id']}: {question['question']}")
#         print("Optionen:", ', '.join(question['options']))
#
# # Funktionales Teilstück: Benutzerantworten sammeln
# def get_user_answers(questions):
#     user_answers = {}
#     for question in questions:
#         user_answer = input(f"Ihre Antwort auf Frage {question['id']}: ")
#         user_answers[str(question['id'])] = user_answer
#     return user_answers
#
# # Funktionales Teilstück: Punktzahl berechnen
# def calculate_score(user_answers, questions):
#     score = 0
#     for question in questions:
#         if user_answers[str(question['id'])] == question['correct_answer']:
#             score += 1
#     return score
#
# # Funktion zur Anzeige von Fragen
# def display_question(question):
#     print(f"Frage {question['id']}: {question['question']}")
#     print("Optionen:", ", ".join(question['options']))
#
# # Funktion zur Überprüfung der Benutzerantwort
# def check_user_answer(user_answer, correct_answer):
#     return user_answer == correct_answer
#
# # Funktion zur Berechnung des Gesamtpunktestands
# def calculate_total_score(user_answers, questions):
#     total_score = 0
#     for question in questions:
#         user_answer = user_answers.get(str(question['id']), '')
#         total_score += check_user_answer(user_answer, question['correct_answer'])
#     return total_score
#
# # Funktion zur Überprüfung der Antwort
# def check_answer(user_answer, correct_answer):
#     return user_answer == correct_answer
#
# # Funktion zur Berechnung des Quiz-Scores
# def calculate_score(user_answers, check_function):
#     score = 0
#     for question in questions:
#         user_answer = user_answers.get(str(question['id']))
#         if user_answer is not None and check_function(user_answer, question['correct_answer']):
#             score += 1
#     return score
#
# # Funktion zur Berechnung des Punktestands für jede Frage
# def calculate_question_score(user_answer, correct_answer):
#     return 1 if user_answer == correct_answer else 0
#
# # Höherwertige Funktion, die die Punkte für das gesamte Quiz berechnet
# def process_quiz(user_answers, questions, score_function):
#     return sum(score_function(user_answers[str(q['id'])], q['correct_answer']) for q in questions)
#
#
# # Funktion, die eine Überprüfungsfunktion für Fragen zurückgibt
# def create_question_checker(correct_answer):
#     def check_question(user_answer):
#         return user_answer == correct_answer
#     return check_question
#
# # Funktion, die den Punktestand basierend auf einer Überprüfungsfunktion berechnet
# def calculate_score_pure(user_answers, question_checker):
#     return sum(question_checker(user_answers[str(q['id'])]) for q in questions)
#
#
# @app.route('/quizhigher', methods=['GET', 'POST'])
# def quiz_higher():
#     if request.method == 'POST':
#         user_answers = request.form.to_dict()
#
#         # Erstellen einer Überprüfungsfunktion für jede Frage
#         question_checkers = [create_question_checker(q['correct_answer']) for q in questions]
#
#         # Verwenden von Closures: Übergeben der Überprüfungsfunktion als Argument
#         score = calculate_score(user_answers, question_checkers)
#
#         return render_template('quiz.html', questions=questions, score=score)
#     return redirect(url_for('index'))
#
# def create_question_checker(correct_answer):
#     def check_question(user_answer):
#         return user_answer == correct_answer
#     return check_question
#
# def calculate_score_repeat(user_answers, question_checkers):
#     return sum(check(user_answers[str(q['id'])]) for q, check in zip(questions, question_checkers))
#
# def get_question_checkers():
#     return [create_question_checker(q['correct_answer']) for q in questions]
#
# def should_redirect_to_index():
#     return request.method != 'POST'
#
# @app.route('/quizrefactored', methods=['GET', 'POST'])
# def quiz_refactored():
#     if should_redirect_to_index():
#         return redirect(url_for('index'))
#
#     user_answers = request.form.to_dict()
#     question_checkers = get_question_checkers()
#     score = calculate_score(user_answers, question_checkers)
#
#     return render_template('quiz.html', questions=questions, score=score)
#
# user_ratings = {
#     '1': 4,
#     '2': 3,
# }
#
# # Anwendung der Map-Funktion, um eine Liste der Bewertungen zu generieren
# ratings_list = list(map(lambda q_id: user_ratings.get(q_id, 0), map(lambda q: str(q['id']), questions)))
#
# # Anwendung der Filter-Funktion, um nur nicht leere Bewertungen zu extrahieren
# non_empty_ratings = list(filter(lambda rating: rating > 0, ratings_list))
#
# # Anwendung der Reduce-Funktion, um den Durchschnitt der Bewertungen zu berechnen
# average_rating = reduce(lambda x, y: x + y, non_empty_ratings, 0) / len(non_empty_ratings) if non_empty_ratings else 0
#
# questionswithdificulty = [
#     {'id': 1, 'question': 'Was ist 1+1?', 'difficulty': 'einfach'},
#     {'id': 2, 'question': 'In welchem Jahr wurde Python veröffentlicht?', 'difficulty': 'mittel'},
#     {'id': 3, 'question': 'Was ist die Hauptstadt von Australien?', 'difficulty': 'schwierig'},
# ]
#
# # Funktion zur Zählung der Fragen eines bestimmten Schwierigkeitsgrads
# def count_questions_by_difficulty(questionswithdificulty, target_difficulty):
#     # Filtern der Fragen nach dem Schwierigkeitsgrad
#     filtered_questions = filter(lambda q: q['difficulty'] == target_difficulty, questionswithdificulty)
#
#     # Mapping, um für jede Frage eine '1' zu erzeugen
#     mapped_questions = map(lambda q: 1, filtered_questions)
#
#     # Reduzieren, um die Gesamtanzahl der Fragen zu erhalten
#     total_count = reduce(lambda x, y: x + y, mapped_questions, 0)
#
#     return total_count
#
# def calculate_user_score(self, user_answers):
#         # Verwendung von map und reduce:
#         # Mapping: Erstellen eines Tupels (user_answer, correct_answer) für jede Frage
#         # Mapping: Anwenden der calculate_question_score-Funktion auf jedes Tupel
#         # Reduce: Summieren der Punktzahlen
#         total_score = reduce(
#             lambda acc, tup: acc + self.calculate_question_score(*tup),
#             map(lambda q: (user_answers.get(str(q['id']), ''), q['correct_answer']), self.questionswithdificulty),
#             0
#         )
#         return total_score
#
# def calculate_average_score(self, user_scores):
#         # Verwendung von reduce: Summieren der Punktzahlen und Teilen durch die Anzahl der Benutzer
#         return reduce(lambda acc, score: acc + score, user_scores, 0) / len(user_scores)
#


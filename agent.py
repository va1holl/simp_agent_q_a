from db_layer import (
    get_connection,
    init_db,
    get_or_create_question,
    get_answers,
    create_answer,
    update_answer_rating,
)

import re


def normalize_question(text: str) -> str:
    text = text.strip().lower()

    tokens = re.findall(r"\w+", text, flags=re.UNICODE)

    tokens.sort()

    return " ".join(tokens)


def handle_no_answers(conn, question_id: int):
    print("У меня пока нет ответа на этот вопрос.")
    user_answer = input("Введите ответ: ").strip()

    if not user_answer:
        print("Тут пусто.")
        return

    create_answer(conn, question_id, user_answer)
    print("Ответ сохранён.")


def handle_one_answer(conn, question_id: int, answer):
    print("\nИзвестный ответ:")
    print(answer["text"])
    print()

    choice = input("1 – принять\n2 – добавить альтернативный\nВаш выбор: ").strip()
    if choice == "2":
        new_ans = input("Введите альтернативный ответ: ").strip()
        if new_ans:
            create_answer(conn, question_id, new_ans)
            print("Альтернативный ответ сохранён.")
        else:
            print("Пустой ответ, пропускаем.")
    else:
        print("Ответ принят.")


def avg_rating(a: dict) -> float:
    return a["rating_sum"] / a["rating_cnt"] if a["rating_cnt"] > 0 else 0.0


def choose_best(answers):
    return max(answers, key=avg_rating)


def rate_answer(conn, answer: dict):
    rating = input("Оцените от 1 до 5 (0 для пропуска): ").strip()
    try:
        rating = int(rating)
    except ValueError:
        rating = 0

    if 1 <= rating <= 5:
        update_answer_rating(conn, answer["id"], rating)
        print("Оценка сохранена.")
    else:
        print("Оценка пропущена.")


def handle_many_answers(conn, answers):
    best = choose_best(answers)

    while True:
        print("\nЛучший ответ:")
        print(best["text"])
        print(f"(средняя оценка: {avg_rating(best):.2f}, голосов: {best['rating_cnt']})\n")

        choice = input(
            "1 – оценить этот ответ\n"
            "2 – показать все ответы и выбрать другой\n"
            "0 – ничего не делать\n"
            "Ваш выбор: "
        ).strip()

        if choice == "1":
            rate_answer(conn, best)
            break

        elif choice == "2":
            print("\nВсе ответы:")
            for i, ans in enumerate(answers, start=1):
                print(
                    f"{i}. {ans['text']} "
                    f"(средняя: {avg_rating(ans):.2f}, голосов: {ans['rating_cnt']})"
                )
                print("-" * 40)

            idx = input("Введите номер ответа для оценки (0 – отмена): ").strip()
            try:
                idx = int(idx)
            except ValueError:
                idx = 0

            if idx == 0:
                print("Отмена выбора ответов.")
                break

            if 1 <= idx <= len(answers):
                chosen = answers[idx - 1]
                print("\nВыбранный ответ:")
                print(chosen["text"])
                rate_answer(conn, chosen)
                break
            else:
                print("Нет такого номера, попробуй ещё.")

        elif choice == "0":
            print("Оценку пропускаем.")
            break

        else:
            print("Неверный ввод, выбери 0, 1 или 2.")


def main():
    print("Агент 'вопрос–ответ'. exit — выход.\n")

    conn = get_connection()
    init_db(conn)

    try:
        while True:
            raw_q = input("Введите вопрос: ")

            if raw_q.strip().lower() == "exit":
                print("Выход.")
                break

            if not raw_q.strip():
                print("Пустой вопрос. Напиши снова\n")
                continue

            q = normalize_question(raw_q)

            q_id = get_or_create_question(conn, q)
            answers = get_answers(conn, q_id)

            if not answers:
                handle_no_answers(conn, q_id)
            elif len(answers) == 1:
                handle_one_answer(conn, q_id, answers[0])
            else:
                handle_many_answers(conn, answers)

            print()

    finally:
        conn.close()


if __name__ == "__main__":
    main()

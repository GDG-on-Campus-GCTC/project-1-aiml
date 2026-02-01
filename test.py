from dotenv import load_dotenv
load_dotenv()

from crew import run_crew

def test_question(question: str):
    print("\n" + "=" * 80)
    print("❓ QUESTION:")
    print(question)

    try:
        result = run_crew(question)
    except Exception as e:
        print("\n❌ ERROR DURING CREW EXECUTION:")
        print(e)
        return

    print("\n🧠 RAW RESULT:")
    print(result)

    if "NO_CONFIDENT_ANSWER" in str(result):
        print("\n📊 FINAL DECISION: LOW CONFIDENCE")
    else:
        print("\n📊 FINAL DECISION: HIGH CONFIDENCE")

    print("=" * 80)


if __name__ == "__main__":
    questions = [
        "What is Binary seaarch tree?",
    ]

    for q in questions:
        test_question(q)

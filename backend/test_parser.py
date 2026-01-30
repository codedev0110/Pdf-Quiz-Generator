"""
Sample test script to verify the parser works correctly
"""
from app.parser import PDFQuestionParser

sample_text = """
101. What is the capital of France?
A) London
B) Paris
C) Berlin
D) Madrid

102. What is the largest planet in our solar system?
A) Earth
B) Mars
C) Jupiter
D) Saturn

103. In what year did World War II end?
A) 1943
B) 1944
C) 1945
D) 1946

104. What is the chemical symbol for Gold?
A) Go
B) Gd
C) Au
D) Ag

105. Who wrote Romeo and Juliet?
A) Jane Austen
B) William Shakespeare
C) Charles Dickens
D) Oscar Wilde
"""

if __name__ == "__main__":
    parser = PDFQuestionParser()
    questions = parser.parse_questions(sample_text)
    
    print(f"✅ Parsed {len(questions)} questions\n")
    
    for q in questions:
        print(f"Q#{q.id}: {q.question}")
        for i, opt in enumerate(q.options):
            print(f"  {chr(65 + i)}) {opt}")
        print()
    
    # Test filtering
    print("Testing filter (101-103):")
    filtered = parser.filter_by_range(questions, 101, 103)
    print(f"Filtered to {len(filtered)} questions")

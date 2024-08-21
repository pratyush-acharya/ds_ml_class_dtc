import functools
import time
import string
from collections import Counter


def timer_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result

    return wrapper


def load_text(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def preprocess_text(text):
    # Convert to lowercase and remove punctuation
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text


@timer_decorator
def word_frequency(text):
    words = text.split()
    return Counter(words)


def create_word_filter(min_length):
    return lambda word: len(word) >= min_length


@timer_decorator
def get_long_words(text, min_length=5):
    words = text.split()
    long_word_filter = create_word_filter(min_length)
    return list(filter(long_word_filter, words))


def get_top_n_words(word_freq, n=10):
    return word_freq.most_common(n)


def calculate_average_word_length(text):
    words = text.split()
    total_length = sum(len(word) for word in words)
    return total_length / len(words) if words else 0


def generate_word_length_distribution(text):
    words = text.split()
    length_distribution = Counter(len(word) for word in words)
    return length_distribution


@timer_decorator
def analyze_text(filename):
    text = load_text(filename)
    processed_text = preprocess_text(text)

    word_freq = word_frequency(processed_text)
    long_words = get_long_words(processed_text)
    top_words = get_top_n_words(word_freq)
    avg_word_length = calculate_average_word_length(processed_text)
    length_distribution = generate_word_length_distribution(processed_text)

    return {
        "word_count": len(processed_text.split()),
        "unique_words": len(word_freq),
        "top_words": top_words,
        "long_words": long_words,
        "avg_word_length": avg_word_length,
        "length_distribution": length_distribution,
    }


def print_analysis_results(results):
    print("\n--- Text Analysis Results ---")
    print(f"Total words: {results['word_count']}")
    print(f"Unique words: {results['unique_words']}")
    print(f"\nTop 10 most common words:")
    for word, count in results["top_words"]:
        print(f"  {word}: {count}")
    print(f"\nNumber of long words (5+ characters): {len(results['long_words'])}")
    print(f"Average word length: {results['avg_word_length']:.2f}")
    print("\nWord length distribution:")
    for length, count in sorted(results["length_distribution"].items()):
        print(f"  {length} characters: {count}")


def main():
    filename = input("Enter the name of the text file to analyze: ")
    try:
        results = analyze_text(filename)
        print_analysis_results(results)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()

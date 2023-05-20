#A01747237 Lizbeth Paulina Ayala Parra #
#A01746643 Alejandro Perez Gonzalez
import csv
import sys
from typing import List, Tuple

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score



TEST_SIZE = 0.4
MONTHS = {'jan': 0,
          'feb': 1,
          'mar': 2,
          'apr': 3,
          'may': 4,
          'jun': 5,
          'jul': 6,
          'aug': 7,
          'sep': 8,
          'oct': 9,
          'nov': 10,
          'dec': 11}


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data_filename.csv")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    # use train_test_split to split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)
    accuracy = accuracy_score(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")
    print(f"Accuracy: {accuracy:.2f}")


def _get_month_index(month):
    return MONTHS[month.lower()[:3]]


def load_data(filename: str) -> Tuple[List[List], List]:
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Returns a tuple (evidence, labels).
    evidence is a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)
    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Get entry for evidence
            evidence.append([
                int(row['Administrative']),
                float(row['Administrative_Duration']),
                int(row['Informational']),
                float(row['Informational_Duration']),
                int(row['ProductRelated']),
                float(row['ProductRelated_Duration']),
                float(row['BounceRates']),
                float(row['ExitRates']),
                float(row['PageValues']),
                float(row['SpecialDay']),
                _get_month_index(row['Month']),
                int(row['OperatingSystems']),
                int(row['Browser']),
                int(row['Region']),
                int(row['TrafficType']),
                1 if row['VisitorType'] == 'Returning_Visitor' else 0,
                1 if row['Weekend'] == 'TRUE' else 0
            ])
            # Get entry for labels
            labels.append(1 if row['Revenue'] == 'TRUE' else 0)

    return (evidence, labels)


def train_model(evidence: List, labels: List) -> KNeighborsClassifier:
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels: List, predictions: List) -> Tuple[float, float]:
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_positive = sum(1 for label, pred in zip(labels, predictions) if label ==1 and pred == 1)
    true_negative = sum(1 for label, pred in zip(labels, predictions) if label == 0 and pred == 0)
    positive_labels = sum(1 for label in labels if label == 1)
    negative_labels = sum(1 for label in labels if label == 0)

    sensitivity = true_positive / positive_labels if positive_labels > 0 else 0
    specificity = true_negative / negative_labels if negative_labels > 0 else 0

    return sensitivity, specificity


if __name__ == "__main__":
    main()

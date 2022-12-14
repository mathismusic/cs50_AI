import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.75


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model, make predictions and evaluate performance
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
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
    months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            labels.append(1 if row[17] == "TRUE" else 0)
            row.pop()
            for i in [1, 3, 5, 6, 7, 8, 9]:
                row[i] = float(row[i])
            for i in [0, 2, 4, 11, 12, 13, 14]:
                row[i] = int(row[i])
            row[10] = months.index(row[10])
            row[15] = 1 if row[15] == "Returning_Visitor" else 0
            row[16] = 1 if row[16] == "TRUE" else 0
            evidence.append(row)

        ''' the above takes up less memory, so better for large csv files. The below is a DictReader implementation.
        reader = csv.DictReader(file)  # csv.reader returns each row as list, so index required. A Dict is easier here
        next(reader)
        for row in reader:
            labels.append(1 if row["Revenue"] == "TRUE" else 0)
            row.pop("Revenue")  # dict.pop(x) removes kv pair with key = x
            # float parameters
            for parameter in (["Administrative_Duration", "Informational_Duration",
                    "ProductRelated_Duration", "BounceRates", "ExitRates","PageValues","SpecialDay"]):
                row[parameter] = float(row[parameter])
            for parameter in (["Administrative", "Informational", "ProductRelated",
                    "OperatingSystems", "Browser", "Region", "TrafficType"]):
                row[parameter] = int(row[parameter])  # else row[p] = '1' (string called 1), not 1

            row["VisitorType"] = 1 if row["VisitorType"] == "Returning_Visitor" else 0
            row["Weekend"] = 1 if row["Weekend"] == "TRUE" else 0
            row["Month"] = months.index(row["Month"])

            evidence.append(list(row.values()))
            '''
    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)

    # the inputs to model.fit must both be lists, with (firstvar)[i] = i+1th traincase's evidence as a list, (secondvar)[i] = i+1th traincase's label
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    correct_pred_pos = actual_positives = correct_pred_neg = actual_negatives = 0
    # return values of model.predict are not exactly lists, they aren't list objects
    for i in range(len(predictions)):
        if labels[i] == 1:
            actual_positives += 1
            if predictions[i] == 1:
                correct_pred_pos += 1
        elif labels[i] == 0:
            actual_negatives += 1
            if predictions[i] == 0:
                correct_pred_neg += 1

    sensitivity = correct_pred_pos / actual_positives
    specificity = correct_pred_neg / actual_negatives
    return sensitivity, specificity


if __name__ == "__main__":
    main()

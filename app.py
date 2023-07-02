from flask import Flask, jsonify
import math
import re

from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


def load_vocab():
    vocab_idf_values = {}
    with open('vocab.txt', 'r') as f:
        terms = f.readlines()
    with open('idf-values.txt', 'r') as f:
        idf_terms = f.readlines()
    for (index, line) in zip(idf_terms, terms):
        vocab_idf_values[line.strip()] = int(index.strip())
    return vocab_idf_values


def load_documents():
    l_document = []
    with open('documents.txt', 'r') as f:
        documents = f.readlines()
    l_document = [document.strip().split() for document in documents]
    return l_document


def load_difficulty():
    l_document = []
    with open('difficulty.txt', 'r') as f:
        documents = f.readlines()
    l_document = [document.strip() for document in documents]
    return l_document


def load_links():
    l_links = []
    with open('links.txt', 'r') as f:
        links = f.readlines()
    l_links = [link.strip() for link in links]
    return l_links


def load_inverted_index():
    inverted_index = {}
    with open('inverted_index.txt', 'r') as f:
        inverted_index_terms = f.readlines()
    for index in range(0, len(inverted_index_terms), 2):
        term = inverted_index_terms[index].strip()
        documents = inverted_index_terms[index+1].strip().split()
        inverted_index[term] = documents
    return inverted_index


vocab_idf_values = load_vocab()
documents = load_documents()
inverted_index = load_inverted_index()
links = load_links()
difficulty = load_difficulty()


def get_tf_dictionary(term):
    tf_terms = {}
    # no of appearences in the doc / total wordds in the doc
    if term in inverted_index:
        for document in inverted_index[term]:
            if document not in tf_terms:
                tf_terms[document] = 1
            else:
                tf_terms[document] += 1

    for document in tf_terms:
        try:
            tf_terms[document] /= len(documents[int(document)])
        except (ZeroDivisionError, ValueError, IndexError) as e:
            print(e)
            print("Erro in document:", document)

    return tf_terms


def get_idf_value(term):
    return math.log(len(documents)/vocab_idf_values[term])


def calculate_sorted_order_of_documents(query_terms):
    potential_documents = {}
    document_info_list_easy = []  # List to store document information
    document_info_list_medium = []
    document_info_list_hard = []

    for term in query_terms:
        if vocab_idf_values[term] == 0:
            continue
        tf_values_by_document = get_tf_dictionary(term)
        idf_value = get_idf_value(term)

        for document in tf_values_by_document:
            if document not in potential_documents:
                potential_documents[document] = tf_values_by_document[document] * idf_value
            potential_documents[document] += tf_values_by_document[document] * idf_value

    for document in potential_documents:
        try:
            potential_documents[document] /= len(query_terms)
        except (ZeroDivisionError, ValueError, IndexError) as e:
            print(e)
            print("Erro in document:", document)

    potential_documents = dict(
        sorted(potential_documents.items(), key=lambda item: item[1], reverse=True))

    names = []
    delimiter = ' '

    for document in documents:
        joined_names = delimiter.join(document)
        names.append(joined_names.capitalize())

    for document_index in list(potential_documents)[:20]:
        if (difficulty[int(document_index)] == "Easy"):
            document_info = {
                'names': names[int(document_index)],
                'Link': links[int(document_index)]
            }
            document_info_list_easy.append(document_info)

        elif (difficulty[int(document_index)] == "Medium"):
            document_info = {
                'names': names[int(document_index)],
                'Link': links[int(document_index)]
            }
            document_info_list_medium.append(document_info)

        elif (difficulty[int(document_index)] == "Hard"):
            document_info = {
                'names': names[int(document_index)],
                'Link': links[int(document_index)]
            }
            document_info_list_hard.append(document_info)

    return document_info_list_easy, document_info_list_medium, document_info_list_hard


app = Flask(__name__)
app.config['SECRET_KEY'] = 'code-engine'
# query = input('Enter your query: ')
# q_terms = [term.lower() for term in query.strip().split()]

# print(q_terms)
# print(calc_docs_sorted_order(q_terms)[0])
# print(len(calc_docs_sorted_order(q_terms)))


class SearchForm(FlaskForm):
    search = StringField('Enter your search term')
    submit = SubmitField('Search')


@app.route("/", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    results_easy = []
    results_medium = []
    results_hard = []
    if form.validate_on_submit():
        query = form.search.data
        q_terms = [term.lower() for term in query.strip().split()]
        results_easy, results_medium, results_hard = calculate_sorted_order_of_documents(
            q_terms)
        print(results_easy)
    return render_template('index.html', form=form, easy_results=results_easy, medium_results=results_medium, hard_results=results_hard)


if __name__ == '__main__':
    app.run()
# query_string = input('Enter your query: ')
# query_terms = [term.lower() for term in query_string.strip().split() if term.isalnum()]
# print(query_terms)
# calculate_sorted_order_of_documents(query_terms)

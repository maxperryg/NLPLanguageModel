import math

# Add <s>'s and </s>'s where they belong
# Lower case the whole thing


def pre_process(corpus):

    # open the training file to read, assign the content variables
    #   processed_corpus
    #   brown_test_corpus
    #   learner_test_corpus
    processed_corpus = open(corpus, "r").readlines()

    # lowercase and pad all corpora with <s> and </s>
    processed_corpus = lower_and_pad(processed_corpus)

    return processed_corpus
    # brown_test_corpus = open(brown_test, "r").readlines()
    # learner_test_corpus = open(learner_test, "r").readlines()

    # brown_test_corpus = lower_and_pad(brown_test_corpus)
    # learner_test_corpus = lower_and_pad(learner_test_corpus)

    # create dictionaries and fill it with all the tokens and frequencies of them
    # training_dictionary_without_unk = count(processed_corpus)
    # brown_test_dictionary_without_unk = count(brown_test_corpus)
    # learner_test_dictionary_without_unk = count(learner_test_corpus)

    #replace words only seen once with <unk>
    # training_dictionary_with_unk = augment_train_with_unk(training_dictionary_without_unk)

    #relace any word seen in test but not corpus with unk and count unk
    # brown_test_dictionary_with_unk = augment_test_with_unk(training_dictionary_without_unk, brown_test_dictionary_without_unk)
    # learner_test_dictionary_with_unk = augment_test_with_unk(training_dictionary_without_unk, learner_test_dictionary_without_unk)

    # return \
    #     {
    #         "training":
    #             {
    #                 "without_unk": training_dictionary_without_unk,
    #                 "with_unk": training_dictionary_with_unk
    #             },
    #         "brown_test":
    #             {
    #                 "without_unk": brown_test_dictionary_without_unk,
    #                 "with_unk": brown_test_dictionary_with_unk
    #             },
    #         "learner_test":
    #             {
    #                 "without_unk": learner_test_dictionary_without_unk,
    #                 "with_unk": learner_test_dictionary_with_unk
    #             }
    #     }


def lower_and_pad(array_of_sentences):
    return "<s> " + " <s> ".join(array_of_sentences).replace("\n", " </s>").lower()


def add_unk_to_training_corpus(corpus_without_unk):
    dictionary = count(corpus_without_unk)
    new_corpus = ""
    for token in corpus_without_unk.split(" "):
        if dictionary[token] != 1:
            new_corpus += str(token) + " "
        else:
            new_corpus += "<unk> "
    return new_corpus.rstrip()


def add_unk_to_testing_corpus(training_corpus_without_unk, testing_corpus_without_unk):
    dictionary = count(training_corpus_without_unk)
    new_corpus = ""
    for token in testing_corpus_without_unk.split(" "):
        if token in dictionary:
            new_corpus += str(token) + " "
        else:
            new_corpus += "<unk> "
    return new_corpus.rstrip()


def count(sentences):
    array_of_sentences = sentences.split(" ")
    dictionary = {}
    for token in array_of_sentences:
        if token in dictionary:
            dictionary[token] += 1
        else:
            dictionary[token] = 1

    return dictionary


def calculate_percentage_types(test, train):
    word_types_in_test = len(test)
    word_types_in_test_not_in_train = len(set(test.keys()) - set(train.keys()))
    return float(word_types_in_test_not_in_train) / float(word_types_in_test) * 100


def calculate_percentage_tokens(test, train):
    word_types_in_test_not_in_train = set(test.keys()) - set(train.keys())
    tokens_in_test_not_in_train = 0
    tokens_in_test = sum(test.values())
    for key in word_types_in_test_not_in_train:
        tokens_in_test_not_in_train += test[key]
    return tokens_in_test_not_in_train/tokens_in_test * 100


def calculate_unigram(training_corpus):
    new = dict(training_corpus.items())
    if "<s>" in new:
        del new["<s>"]
    total = sum(new.values())
    ans = {key: value/total for key, value in new.items()}
    return ans


def calculate_bigram(training_corpus, training_dictionary, addn):
    text = training_corpus.split()
    #bigram = dict(training_dictionary)
    keys = {key: addn for key, value in training_dictionary.items()}.items()
    bigram = {key: dict(keys) for key, value in keys}
    for i in range(len(text)-1):
        bigram[text[i]][text[i + 1]] = bigram[text[i]][text[i + 1]] + 1 / training_dictionary[text[i]]
    return bigram


#all_dictionaries = pre_process("training.txt", "brown-test.txt", "learner-test.txt")

brown_training_corpus_without_unk = pre_process("brown-train.txt")
brown_testing_corpus_without_unk = pre_process("brown-test.txt")
learner_testing_corpus_without_unk = pre_process("learner-test.txt")

brown_training_corpus_with_unk = add_unk_to_training_corpus(brown_training_corpus_without_unk)
brown_testing_corpus_with_unk = add_unk_to_testing_corpus(brown_training_corpus_without_unk, brown_testing_corpus_without_unk)
learner_testing_corpus_with_unk = add_unk_to_testing_corpus(brown_training_corpus_without_unk, learner_testing_corpus_without_unk)

brown_training_dictionary_without_unk = count(brown_training_corpus_without_unk)
brown_testing_dictionary_without_unk = count(brown_testing_corpus_without_unk)
learner_testing_dictionary_without_unk = count(learner_testing_corpus_without_unk)

brown_training_dictionary_with_unk = count(brown_training_corpus_with_unk)
brown_testing_dictionary_with_unk = count(brown_testing_corpus_with_unk)
learner_testing_dictionary_with_unk = count(learner_testing_corpus_with_unk)

unigram_of_training = calculate_unigram(brown_training_dictionary_with_unk)
bigram_of_training = calculate_bigram(brown_training_corpus_with_unk, brown_training_dictionary_with_unk, 0)
bigram_add_one_of_training = calculate_bigram(brown_training_corpus_with_unk, brown_training_dictionary_with_unk, 1)


print("done")

print(sum(brown_training_dictionary_with_unk.values()))
answers = open("Answers.txt", "w")

answers.writelines("1) How many word types (unique words) are there in the training corpus? Please include "
                   "the padding symbols and the unknown token.\n\n"
                   "Word types (unique words) in training corpus: " + str(len(brown_training_dictionary_with_unk.keys())) + "\n\n")

answers.writelines("2) How many word tokens are there in the training corpus?\n\n"
                   "Word tokens in training corpus: " + str(sum(brown_training_dictionary_with_unk.values())) + "\n\n")

answers.writelines("3) What percentage of word tokens and word types in each of the test corpora did not "
                   "occur in training (before you mapped the unknown words to <unk> in training and test data)?\n\n")

answers.writelines("Percentage of word types in brown test corpus that are not in training: "
                   + str(calculate_percentage_types(brown_testing_dictionary_without_unk, brown_training_dictionary_without_unk))
                   + "%\n\n")

answers.writelines("Percentage of word tokens in brown test corpus that are not in training: "
                   + str(calculate_percentage_tokens(brown_testing_dictionary_without_unk, brown_training_dictionary_without_unk))
                   + "%\n\n")

answers.writelines("Percentage of word types in learner test corpus that are not in training: "
                   + str(calculate_percentage_types(learner_testing_dictionary_without_unk, brown_training_dictionary_without_unk))
                   + "%\n\n")

answers.writelines("Percentage of word tokens in learner test corpus that are not in training: "
                   + str(calculate_percentage_tokens(learner_testing_dictionary_without_unk, brown_training_dictionary_without_unk))
                   + "%\n\n")


# wordtypes = len(dict["training_dictionary"])
# wordtokens = sum(dict["training_dictionary"].values())
#
# print("Word types in training trainingdictionary: " + str(wordtypes) + "\n\n\n\n")
# print("Word tokens in training trainingdictionary: " + str(wordtokens) + "\n\n\n\n")

def pre_process(train, brown_test, learner_test):

    # open the training file to read, assign the content variables
    #   training_corpus
    #   brown_test_corpus
    #   learner_test_corpus
    training_corpus = open(train, "r").readlines()
    brown_test_corpus = open(brown_test, "r").readlines()
    learner_test_corpus = open(learner_test, "r").readlines()

    # lowercase and pad all corpora with <s> and </s>
    training_corpus = lower_and_pad(training_corpus)
    brown_test_corpus = lower_and_pad(brown_test_corpus)
    learner_test_corpus = lower_and_pad(learner_test_corpus)

    # create dictionaries and fill it with all the tokens and frequencies of them
    training_dictionary_without_unk = count(training_corpus)
    brown_test_dictionary_without_unk = count(brown_test_corpus)
    learner_test_dictionary_without_unk = count(learner_test_corpus)

    #replace words only seen once with <unk>
    training_dictionary_with_unk = augment_train_with_unk(training_dictionary_without_unk)

    #relace any word seen in test but not train with unk and count unk
    brown_test_dictionary_with_unk = augment_test_with_unk(training_dictionary_without_unk, brown_test_dictionary_without_unk)
    learner_test_dictionary_with_unk = augment_test_with_unk(training_dictionary_without_unk, learner_test_dictionary_without_unk)

    return \
        {
            "training":
                {
                    "without_unk": training_dictionary_without_unk,
                    "with_unk": training_dictionary_with_unk
                },
            "brown_test":
                {
                    "without_unk": brown_test_dictionary_without_unk,
                    "with_unk": brown_test_dictionary_with_unk
                },
            "learner_test":
                {
                    "without_unk": learner_test_dictionary_without_unk,
                    "with_unk": learner_test_dictionary_with_unk
                }
        }


def count(sentences):
    array_of_sentences = sentences.split(" ")
    dictionary = {}
    for token in array_of_sentences:
        if token in dictionary:
            dictionary[token] += 1
        else:
            dictionary[token] = 1

    return dictionary


def augment_train_with_unk(dictionary):
    dictionary_with_unk = {}
    dictionary_with_unk["<unk>"] = 0
    for key in dictionary:
        if dictionary[key] == 1:
            dictionary_with_unk["<unk>"] += 1
        else:
            dictionary_with_unk[key] = dictionary[key]

    return dictionary_with_unk


def augment_test_with_unk(train, test):
    dictionary_with_unk = {}
    dictionary_with_unk["<unk>"] = 0
    for key in test:
        if train.has_key(key):
            dictionary_with_unk[key] = test[key]
        else:
            dictionary_with_unk["<unk>"] += test[key]
    return dictionary_with_unk


def lower_and_pad(array_of_sentences):
    return "<s> " + " <s> ".join(array_of_sentences).replace("\n", " </s>").lower()

def calculate_percentage_types(test, train):
    word_types_in_test = len(test)
    word_types_in_test_not_in_train = len(set(test.keys()) - set(train.keys()))
    return float(word_types_in_test_not_in_train) / float(word_types_in_test) * 100

def calculate_percentage_tokens(test, train):
    word_types_in_test_not_in_train = set(test.keys()) - set(train.keys())
    tokens_in_test_not_in_train = 0
    tokens_in_test = sum(test.values())
    for key in word_types_in_test_not_in_train:
        tokens_in_test_not_in_train+=test[key]
    return float(tokens_in_test_not_in_train) / float(tokens_in_test) * 100


all_dictionaries = pre_process("brown-train.txt", "brown-test.txt", "learner-test.txt")

answers = open("Answers.txt", "w")

answers.writelines("1) How many word types (unique words) are there in the training corpus? Please include "
                   "the padding symbols and the unknown token.\n\n"
                   "Word types (unique words) in training corpus: " + str(len(all_dictionaries["training"]["with_unk"].keys())) + "\n\n")

answers.writelines("2) How many word tokens are there in the training corpus?\n\n"
                   "Word tokens in training corpus: " + str(sum(all_dictionaries["training"]["with_unk"].values())))

answers.writelines("3) What percentage of word tokens and word types in each of the test corpora did not"
                   "occur in training (before you mapped the unknown words to <unk> in training and test data)?\n\n")

answers.writelines("Percentage of word types in brown test corpus that are not in training: "
                   + str(calculate_percentage_types(all_dictionaries["brown_test"]["without_unk"], all_dictionaries["training"]["without_unk"]))
                   + "%\n\n")

answers.writelines("Percentage of word tokens in brown test corpus that are not in training: "
                   + str(calculate_percentage_tokens(all_dictionaries["brown_test"]["without_unk"], all_dictionaries["training"]["without_unk"]))
                   + "%\n\n")

answers.writelines("Percentage of word types in learner test corpus that are not in training: "
                   + str(calculate_percentage_types(all_dictionaries["learner_test"]["without_unk"], all_dictionaries["training"]["without_unk"]))
                   + "%\n\n")

answers.writelines("Percentage of word tokens in learner test corpus that are not in training: "
                   + str(calculate_percentage_tokens(all_dictionaries["learner_test"]["without_unk"], all_dictionaries["training"]["without_unk"]))
                   + "%\n\n")
# wordtypes = len(dict["training_dictionary"])
# wordtokens = sum(dict["training_dictionary"].values())
#
# print("Word types in training trainingdictionary: " + str(wordtypes) + "\n\n\n\n")
# print("Word tokens in training trainingdictionary: " + str(wordtokens) + "\n\n\n\n")

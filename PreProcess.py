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


def add_unk_to_testing_corpus(training_corpus_with_unk, testing_corpus_without_unk):
    dictionary = count(training_corpus_with_unk)
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
    ans = {key: value for key, value in new.items()}
    return ans


def calculate_bigram(training_corpus, training_dictionary, addn):
    text = training_corpus.split()
    #bigram = dict(training_dictionary)
    keys = {key: addn for key, value in training_dictionary.items()}
    bigram = {key: dict(keys.items()) for key, value in keys.items()}
    for i in range(len(text)-1):
        bigram[text[i]][text[i + 1]] += 1
    # / training_dictionary[text[i]]
    return bigram


def calculate_bigram_percentage_unseen(bigram_test, bigram_train):
    in_test = set()
    in_train = set()
    count_tokens_in_test_not_in_train = 0
    count_tokens_in_test = 0
    for key in bigram_test.keys():
        for second_key in bigram_test[key]:
            if bigram_test[key][second_key] != 0:
                tup = (key, second_key)
                in_test.add(tup)
    for key in bigram_train.keys():
        for second_key in bigram_train[key]:
            if bigram_train[key][second_key] != 0:
                tup = (key, second_key)
                in_train.add(tup)
    in_test_not_in_train = set(in_test - in_train)
    for tup in in_test_not_in_train:
        count_tokens_in_test_not_in_train += bigram_test[tup[0]][tup[1]]
    for tup in in_test:
        count_tokens_in_test += bigram_test[tup[0]][tup[1]]

    percent_types = len(in_test_not_in_train) / len(in_test) * 100
    percent_tokens = count_tokens_in_test_not_in_train / count_tokens_in_test * 100
    # for i in range(len(test_text)-1):
    #     if test_text[i] in bigram_train:
    #         if test_text[i+1] in bigram_train[test_text[i]]:
    #             intersection.add({test_text[i]:test_text[i+1]})
    #         else:
    #             only_test.add({test_text[i]:test_text[i+1]})



    return [percent_types, percent_tokens]\


def unigram_log_prob_of(test_sentence, unigram_count_of_training):
    ans = ""
    text = test_sentence.replace("<s> ", "").split(" ")
    total = sum(unigram_count_of_training.values())
    log_prob = 0
    for key in unigram_count_of_training:
        unigram_count_of_training[key] /= total
    for word in text:
        log_prob += math.log(unigram_count_of_training[word], 2)
        ans += "log probability of " + word + " ( " + str(math.log(unigram_count_of_training[word], 2)) + ") + \n"
    ans += "= " + str(log_prob) + "\n\n"
    ans += "average log probability is log probability(" + str(log_prob) + ") / " + "the amount of words in the test sentence (" + str(len(text)) + ") = "
    avg_log_prob = log_prob/len(text)
    ans += str(avg_log_prob) + "\n\n"
    ans += "perplexity is 2^(-average log probability) = "
    perplexity = 2 ** -avg_log_prob
    ans += str(perplexity) + "\n\n"
    return ans


def unigram_log_prob_of_test(test_sentence, unigram_count_of_training):
    ans = ""
    text = test_sentence.replace("<s> ", "").split(" ")
    total = sum(unigram_count_of_training.values())
    log_prob = 0
    for key in unigram_count_of_training:
        unigram_count_of_training[key] /= total
    for word in text:
        log_prob += math.log(unigram_count_of_training[word], 2)
    avg_log_prob = log_prob/len(text)
    ans += "perplexity is = "
    perplexity = 2 ** -avg_log_prob
    ans += str(perplexity) + "\n\n"
    return ans


def bigram_log_prob_of(test_sentence, bigram_count_of_training, training_dictionary_with_unk):
    ans = ""
    text = test_sentence.split(" ")
    log_prob = 0
    for i in range(len(text)-1):
        if bigram_count_of_training[text[i]][text[i+1]] == 0:
            ans = ""
            ans += "'" + text[i] + ", " + text[i+1] + "' and possibly more parameters is/are unseen so probability of the sentence is undefined"
            return ans
        else:
            this_one = math.log((bigram_count_of_training[text[i]][text[i + 1]] / (training_dictionary_with_unk[text[i]])), 2)
            ans += "log probability of " + text[i] + " " + text[i + 1] + " ( " + str(this_one) + ") + \n"
            log_prob += this_one
    ans += "= " + str(log_prob) + "\n\n"
    ans += "average log probability is log probability(" + str(
        log_prob) + ") / " + "the amount of words in the test sentence (" + str(len(text)) + ") = "
    avg_log_prob = log_prob / len(text)
    ans += str(avg_log_prob) + "\n\n"
    ans += "perplexity is 2^(-average log probability) = "
    perplexity = 2 ** -avg_log_prob
    ans += str(perplexity) + "\n\n"
    return ans


def bigram_log_prob_of_test(test_sentence, bigram_count_of_training, training_dictionary_with_unk):
    ans = ""
    text = test_sentence.split(" ")
    log_prob = 0
    for i in range(len(text)-1):
        if bigram_count_of_training[text[i]][text[i+1]] == 0:
            ans = ""
            ans += "'" + text[i] + ", " + text[i+1] + "' and possibly more parameters is/are unseen so probability of the sentence is undefined"
            return ans
        else:
            this_one = math.log((bigram_count_of_training[text[i]][text[i + 1]] / (training_dictionary_with_unk[text[i]])), 2)
            log_prob += this_one
    avg_log_prob = log_prob / len(text)
    ans += "perplexity is = "
    perplexity = 2 ** -avg_log_prob
    ans += str(perplexity) + "\n\n"
    return ans


def bigram_add_one_log_prob_of(test_sentence, bigram_count_of_training, training_dictionary_with_unk):
    ans = ""
    text = test_sentence.split(" ")
    log_prob = 0
    for i in range(len(text)-1):
        this_one = math.log((bigram_count_of_training[text[i]][text[i+1]] / (training_dictionary_with_unk[text[i]] + len(training_dictionary_with_unk))), 2)
        ans += "log probability of " + text[i] + " " + text[i+1] + " ( " + str(this_one) + ") + \n"
        log_prob += this_one
    ans += "is " + str(log_prob) + "\n\n"
    ans += "average log probability is log probability(" + str(log_prob) + ") / " + "the amount of words in the test sentence (" + str(len(text)) + ") = "
    avg_log_prob = log_prob / len(text)
    ans += str(avg_log_prob) + "\n\n"
    ans += "perplexity is 2^(-average log probability) = "
    perplexity = 2 ** -avg_log_prob
    ans += str(perplexity) + "\n\n"
    return ans


def bigram_add_one_log_prob_of_test(test_sentence, bigram_count_of_training, training_dictionary_with_unk):
    ans = ""
    text = test_sentence.split(" ")
    log_prob = 0
    for i in range(len(text)-1):
        this_one = math.log((bigram_count_of_training[text[i]][text[i+1]] / (training_dictionary_with_unk[text[i]] + len(training_dictionary_with_unk))), 2)
        log_prob += this_one
    avg_log_prob = log_prob / len(text)
    ans += "perplexity is = "
    perplexity = 2 ** -avg_log_prob
    ans += str(perplexity) + "\n\n"
    return ans

#all_dictionaries = pre_process("training.txt", "brown-test.txt", "learner-test.txt")


brown_training_corpus_without_unk = pre_process("brown-train.txt")
brown_testing_corpus_without_unk = pre_process("brown-test.txt")
learner_testing_corpus_without_unk = pre_process("learner-test.txt")

brown_training_corpus_with_unk = add_unk_to_training_corpus(brown_training_corpus_without_unk)
brown_testing_corpus_with_unk = add_unk_to_testing_corpus(brown_training_corpus_with_unk, brown_testing_corpus_without_unk)
learner_testing_corpus_with_unk = add_unk_to_testing_corpus(brown_training_corpus_with_unk, learner_testing_corpus_without_unk)

brown_training_dictionary_without_unk = count(brown_training_corpus_without_unk)
brown_testing_dictionary_without_unk = count(brown_testing_corpus_without_unk)
learner_testing_dictionary_without_unk = count(learner_testing_corpus_without_unk)

brown_training_dictionary_with_unk = count(brown_training_corpus_with_unk)
brown_testing_dictionary_with_unk = count(brown_testing_corpus_with_unk)
learner_testing_dictionary_with_unk = count(learner_testing_corpus_with_unk)

unigram_count_of_training = calculate_unigram(brown_training_dictionary_with_unk)

bigram_count_of_training = calculate_bigram(brown_training_corpus_with_unk, brown_training_dictionary_with_unk, 0)
bigram_count_add_one_of_training = calculate_bigram(brown_training_corpus_with_unk, brown_training_dictionary_with_unk, 1)
bigram_count_of_brown_test = calculate_bigram(brown_testing_corpus_with_unk, brown_testing_dictionary_with_unk, 0)
bigram_count_of_learner_test = calculate_bigram(learner_testing_corpus_with_unk, learner_testing_dictionary_with_unk, 0)

percentage_brown_bigram_unseen = calculate_bigram_percentage_unseen(bigram_count_of_brown_test, bigram_count_of_training)
percentage_learner_bigram_unseen = calculate_bigram_percentage_unseen(bigram_count_of_learner_test, bigram_count_of_training)

quest6test1 = pre_process("quest6test1.txt")
quest6test2 = pre_process("quest6test2.txt")
quest6test3 = pre_process("quest6test3.txt")

quest6test1_with_unk = add_unk_to_testing_corpus(brown_training_corpus_with_unk, quest6test1)
quest6test2_with_unk = add_unk_to_testing_corpus(brown_training_corpus_with_unk, quest6test2)
quest6test3_with_unk = add_unk_to_testing_corpus(brown_training_corpus_with_unk, quest6test3)



print("done")

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

answers.writelines("4) What percentage of bigrams (bigram types and bigram tokens) in each of the test corpora that did"
                   " not occur in training (treat <unk> as a token that has been observed)?\n\n")

answers.writelines("Percentage of word types in brown test bigram that are not in training: "
                   + str(percentage_brown_bigram_unseen[0]) + "%\n\n")

answers.writelines("Percentage of word tokens in brown test bigram that are not in training: "
                   + str(percentage_brown_bigram_unseen[1]) + "%\n\n")

answers.writelines("5 & 6)\n\n"
                   "    5)Compute the log probabilities of the following sentences under the three models \n"
                   "(ignore capitalization and pad each sentence as described above). Please list all of the\n"
                    "parameters required to compute the probabilities and show the complete calculation.\n"
                    "Which of the parameters have zero values under each model? Use log base 2 in your\n"
                    "calculations. Map words not observed in the training corpus to the <unk> token.\n"
                    "• He was laughed off the screen .\n"
                    "• There was no compulsion behind them .\n"
                    "• I look forward to hearing your reply .\n\n"
                    "   6) Compute the perplexities of each of the sentences above under each of the models.\n\n"
                   + "UNIGRAM MLE for " + quest6test1 + "\n\n" + unigram_log_prob_of(quest6test1_with_unk, unigram_count_of_training) + "\n\n"
                   + "UNIGRAM MLE for " + quest6test2 + "\n\n" + unigram_log_prob_of(quest6test2_with_unk, unigram_count_of_training) + "\n\n"
                   + "UNIGRAM MLE for " + quest6test3 + "\n\n" + unigram_log_prob_of(quest6test3_with_unk, unigram_count_of_training) + "\n\n"
                   + "BIGRAM MLE for " + quest6test1 + "\n\n" + bigram_log_prob_of(quest6test1_with_unk, bigram_count_of_training, brown_training_dictionary_with_unk) + "\n\n"
                   + "BIGRAM MLE for " + quest6test2 + "\n\n" + bigram_log_prob_of(quest6test2_with_unk, bigram_count_of_training, brown_training_dictionary_with_unk) + "\n\n"
                   + "BIGRAM MLE for " + quest6test3 + "\n\n" + bigram_log_prob_of(quest6test3_with_unk, bigram_count_of_training, brown_training_dictionary_with_unk) + "\n\n"
                   + "BIGRAM ADD ONE for " + quest6test1 + "\n\n" + bigram_add_one_log_prob_of(quest6test1_with_unk, bigram_count_add_one_of_training, brown_training_dictionary_with_unk) + "\n\n"
                   + "BIGRAM ADD ONE for " + quest6test2 + "\n\n" + bigram_add_one_log_prob_of(quest6test2_with_unk, bigram_count_add_one_of_training, brown_training_dictionary_with_unk) + "\n\n"
                   + "BIGRAM ADD ONE for " + quest6test3 + "\n\n" + bigram_add_one_log_prob_of(quest6test3_with_unk, bigram_count_add_one_of_training, brown_training_dictionary_with_unk) + "\n\n")

answers.writelines("7) Compute the perplexities of the entire test corpora, separately for the brown-test.txt"
                    " and learner-test.txt under each of the models. Discuss the differences in the results you obtained.\n\n"
                   + "UNIGRAM MLE for brown test"+ "\n\n" + unigram_log_prob_of_test(brown_testing_corpus_with_unk, unigram_count_of_training) + "\n\n"
                    + "UNIGRAM MLE for learner test"+ "\n\n" + unigram_log_prob_of_test(learner_testing_corpus_with_unk, unigram_count_of_training) + "\n\n"
                   + "BIGRAM MLE for brown test"+ "\n\n" + bigram_log_prob_of_test(brown_testing_corpus_with_unk, bigram_count_of_training, brown_training_dictionary_with_unk) + "\n\n"
                   + "BIGRAM MLE for learner test" + "\n\n" + bigram_log_prob_of_test(learner_testing_corpus_with_unk, bigram_count_of_training, brown_training_dictionary_with_unk) + "\n\n"
                    + "BIGRAM ADD ONE for brown test" + "\n\n" + bigram_add_one_log_prob_of_test(brown_testing_corpus_with_unk, bigram_count_add_one_of_training, brown_training_dictionary_with_unk) + "\n\n"
                    + "BIGRAM ADD ONE for learner test" + "\n\n" + bigram_add_one_log_prob_of_test(learner_testing_corpus_with_unk, bigram_count_add_one_of_training, brown_training_dictionary_with_unk) + "\n\n")

# answers.writelines("Percentage of word types in learner test bigram that are not in training: "
#                    + str(percentage_learner_bigram_unseen[0]) + "%\n\n")
#
# answers.writelines("Percentage of word tokens in learner test bigram that are not in training: "
#                    + str(percentage_learner_bigram_unseen[1]) + "%\n\n")

# wordtypes = len(dict["training_dictionary"])
# wordtokens = sum(dict["training_dictionary"].values())
#
# print("Word types in training trainingdictionary: " + str(wordtypes) + "\n\n\n\n")
# print("Word tokens in training trainingdictionary: " + str(wordtokens) + "\n\n\n\n")

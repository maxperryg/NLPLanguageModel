def pre_process(train, brown_test, lerner_test):

    # open the training file to read and the resulting file to be written to
    training_corpus = open(train, "r")
    brown_test_corpus = open(brown_test, "r")
    learner_test_corpus = open(lerner_test, "r")

    #post = open(out_file, "w")

    # assign the array of each line to training_sentences
    training_sentences = training_corpus.readlines()
    brown_test_sentences = brown_test_corpus.readlines()
    lerner_test_sentences = learner_test_corpus.readlines()

    # join training_sentences elements by " <S> " and replace all newline characters with " </S>
    training_sentences = " <s> ".join(training_sentences)
    training_sentences = training_sentences.replace("\n", " </s>")

    brown_test_sentences = " <s> ".join(brown_test_sentences)
    brown_test_sentences = brown_test_sentences.replace("\n", " </s>")

    lerner_test_sentences = " <s> ".join(lerner_test_sentences)
    lerner_test_sentences = lerner_test_sentences.replace("\n", " </s>")

    # add "<S> to the beginning of the whole thing
    training_sentences = "<s> " + training_sentences
    brown_test_sentences = "<s> " + brown_test_sentences
    lerner_test_sentences = "<s> " + lerner_test_sentences

    # convert the whole thing to lower case
    training_sentences = training_sentences.lower()
    brown_test_sentences = brown_test_sentences.lower()
    lerner_test_sentences = lerner_test_sentences.lower()

    # write it to the resulting file
    #post.writelines(training_sentences.replace("</s> ", "</s> \n"))

    #create an array of all the tokens split by " "
    training_sentences_array = training_sentences.split(" ")
    brown_test_sentences_array = brown_test_sentences.split(" ")
    lerner_test_sentences_array = lerner_test_sentences.split(" ")


    # create training_dictionary and fill it with all the tokens and frequencies of them
    training_dictionary = count(training_sentences_array)
    brown_test_dictionary = count(brown_test_sentences_array)
    lerner_test_dictionary = count(lerner_test_sentences_array)


    #replace words only seen once with <unk>
    training_dictionary_with_unk = replace_with_unk(training_dictionary)

    #relace any word seen in test but not train with unk and count unk
    brown_test_dictionary_with_unk = replace_disjoint_with_unk(training_dictionary, brown_test_dictionary)
    lerner_test_dictionary_with_unk = replace_disjoint_with_unk(training_dictionary, brown_test_dictionary)



    return {"training_dictionary": training_dictionary, "brown_test_dictionary": brown_test_dictionary, "lerner_test_dictionary": lerner_test_dictionary}

    # post.writelines("\nFull Corpus\n--------------\n")
    # post.writelines(str(training_dictionary).replace(",", ",\n") + "\n")
    # post.writelines("\nCorpus with <unk>\n--------------\n")
    # post.writelines(str(training_dictionary).replace(",", ",\n")+"\n")
    # training_corpus.close()
    # post.close()

def count(array_of_sentences):

    dictionary = {}
    for token in array_of_sentences:
        if token in dictionary:
            dictionary[token] += 1
        else:
            dictionary[token] = 1

    return dictionary


def replace_with_unk(dictionary):

    dictionary_with_unk = {}
    dictionary_with_unk["<unk>"] = 0
    for key in dictionary:
        if dictionary[key] == 1:
            dictionary_with_unk["<unk>"] += 1
        else:
            dictionary_with_unk[key] = dictionary[key]

    return dictionary_with_unk


def replace_disjoint_with_unk(train, test):
    words_not_in_trainer = list(set(test.keys()) - set(train.keys()))
    for key in words_not_in_trainer:
        if test.has_key(key):
            del test[key]
    test["<unk>"] = len(words_not_in_trainer)
    return test

#def find_percent_of_unk(train, test):
    #return test["<unk>"] /


dict = pre_process("brown-train.txt", "brown-test.txt", "learner-test.txt")
wordtypes = len(dict["training_dictionary"])
wordtokens = sum(dict["training_dictionary"].values())

print("Word types in training trainingdictionary: " + str(wordtypes) + "\n\n\n\n")
print("Word tokens in training trainingdictionary: " + str(wordtokens) + "\n\n\n\n")

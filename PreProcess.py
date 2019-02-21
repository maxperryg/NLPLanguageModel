def pre_process(in_file, out_file):
    # open the training file to read and the resulting file to be written to
    pre = open(in_file, "r")
    post = open(out_file, "w")

    # assign the array of each line to sentences
    sentences = pre.readlines()

    # join sentences elements by "<S>" and replace all newline characters with "</S>
    sentences = " <s> ".join(sentences).replace("\n", " </s>")


    # add "<S> to the beginning of the whole thing and add "</S>" to the end of the whole thing
    sentences = "<S> " + sentences + " </S> "

    # convert the whole thing to lower case
    sentences = sentences.lower()

    # write it to the resulting file
    post.writelines(sentences.replace("</s> ", "</s> \n"))

    #create an array of all the tokens split by " "
    sentences = sentences.split(" ")

    # create corpus and fill it with all the tokens and frequencies of them
    corpus = {}
    for token in sentences:
        if token in corpus:
            corpus[token] += 1
        else:
            corpus[token] = 1

    # create new corpus and fill it with same tokens but replace those that have a frequency of 1 with "<unk>"
    corpuswithunk = {}
    corpuswithunk["<unk>"] = 0
    for key in corpus:
        if corpus[key] == 1:
            corpuswithunk["<unk>"] += 1
        else:
            corpuswithunk[key] = corpus[key]
    post.writelines("\nFull Corpus\n--------------\n")
    post.writelines(str(corpus).replace(",", ",\n") + "\n")
    post.writelines("\nCorpus with <unk>\n--------------\n")
    post.writelines(str(corpuswithunk).replace(",", ",\n")+"\n")
    pre.close()
    post.close()


pre_process("Train.txt", "Processed.txt")

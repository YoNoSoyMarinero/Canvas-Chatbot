import nltk
from nltk.tokenize import word_tokenize
from typing import TypeVar, Callable, Sequence
from functools import reduce
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import demoji
import string

#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('omw-1.4')


class MessagePreprocessingPipelineService:
    T = TypeVar('T')

    #defining steps of preprocessing pipeline
    @classmethod
    def preprocess_message_pipeline(cls, raw_message: string) -> string:
        pipeline_steps : list = [cls.__remove_emojis,
                                 cls.__tokenize_message,
                                 cls.__remove_punctuation,
                                 cls.__lowercase_message,
                                 cls.__remove_stopwords,
                                 cls.__word_lemmatizer,
                                 cls.__get_preprocessed_message]
        return cls.__custom_pipeline(raw_message= raw_message, function_pipeline=pipeline_steps)

    #custom pipeline using reduce function
    @classmethod
    def __custom_pipeline(cls, raw_message: T, function_pipeline: Sequence[Callable[[T], T]]):
        return reduce(lambda message, function: function(message), function_pipeline, raw_message)

    #turning message into tokens
    @classmethod
    def __tokenize_message(cls, raw_message: string) -> list:
        return word_tokenize(raw_message)

    #removing all punctuation
    @classmethod
    def __remove_punctuation(cls, bag_of_words: list) -> list:
        punctuation_free_message: list = [''.join(char for char in word if char not in string.punctuation) for word in bag_of_words]
        return [word for word in punctuation_free_message if word]

    #turning all punctuation to lowercase
    @classmethod
    def __lowercase_message(cls, bag_of_words: list) -> list:
        return list(map(lambda word: word.lower(), bag_of_words))

    #removing all stopwords from nltk set
    @classmethod
    def __remove_stopwords(cls, bag_of_words: list) -> list:
        stop_words: set = set(stopwords.words('english'))
        return [word for word in bag_of_words if word not in stop_words]

    #removing emojis from message
    @classmethod
    def __remove_emojis(cls, raw_message: string) -> string:
        return demoji.replace(raw_message, "")

    #turininig tokens into lemmas
    @classmethod
    def __word_lemmatizer(cls, bag_of_words: list) -> list:
        wnl: WordNetLemmatizer = WordNetLemmatizer()
        return [wnl.lemmatize(word, pos='v') for word in bag_of_words]

    #turning tokens into processed message
    @classmethod
    def __get_preprocessed_message(cls, bag_of_words):
        return " ".join(bag_of_words)




import numpy as np
import re
import csv

class Data(object):
    """
    Class to handle loading and processing of raw datasets.
    """

    def __init__(self, data_source, y_dict= {"c": 0, "e": 1, "i": 2, "o": 3, "p": 4},
                 alphabet="abcdefghijklmnopqrstuvwxyz0123456789-,;.!?:'\"/\\|_@#$%^&*~`+-=<>()[]{}",
                 input_size=256, num_of_classes=5):

        self.alphabet = alphabet
        self.alphabet_size = len(self.alphabet)
        self.dict = {}  # Maps each character to an integer
        self.y_dict = y_dict
        self.no_of_classes = num_of_classes
        for idx, char in enumerate(self.alphabet):
            self.dict[char] = idx + 1
        self.length = input_size
        self.data_source = data_source

    def load_data(self, row_text_nbr=3, row_label_nbr=0):

        data = []
        with open(self.data_source, 'r', encoding='utf-8') as f:
            rdr = csv.reader(f, delimiter='\t', quotechar='"')
            header = True
            for row in rdr:
                if header:
                    header = False
                    continue
                txt = re.sub("\\\/", "/", row[row_text_nbr])
                txt = re.sub('@([A-Za-z0-9_]+)', "@", txt)
                txt = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                             "URL", txt)
                data.append((self.y_dict[row[row_label_nbr]], txt))  # format: (label, text)
        self.data = np.array(data)
        print("Data loaded from " + self.data_source)

    def get_all_data(self):
        """
        Return all loaded data from data variable.

        Returns:
            (np.ndarray) Data transformed from raw to indexed form with associated one-hot label.

        """
        data_size = len(self.data)
        start_index = 0
        end_index = data_size
        batch_texts = self.data[start_index:end_index]
        batch_indices = []
        one_hot = np.eye(self.no_of_classes, dtype='int64')
        classes = []
        for c, s in batch_texts:
            batch_indices.append(self.str_to_indexes(s))
            c = int(c) - 1
            classes.append(one_hot[c])
        return np.asarray(batch_indices, dtype='int64'), np.asarray(classes)

    def str_to_indexes(self, s):
        """
        Convert a string to character indexes based on character dictionary.

        Args:
            s (str): String to be converted to indexes

        Returns:
            str2idx (np.ndarray): Indexes of characters in s

        """
        s = s.lower()
        max_length = min(len(s), self.length)
        str2idx = np.zeros(self.length, dtype='int64')
        for i in range(1, max_length + 1):
            c = s[-i]
            if c in self.dict:
                str2idx[i - 1] = self.dict[c]
        return str2idx



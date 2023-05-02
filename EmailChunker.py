import numpy as np
from pandas import Series


class EmailChunker:
    def __init__(self, chunk_size):
        self.chunk_size = chunk_size

    def chunk_emails(self, emails: Series) -> np.ndarray:
        """
        This function splits a pandas.Series into a numpy.ndarray containing chunks of the same size.
        """
        num_chunks = int(np.ceil(len(emails) / self.chunk_size))  # round up to the nearest integer
        chunks = np.array_split(emails, num_chunks)  # split the Series into chunks
        return chunks


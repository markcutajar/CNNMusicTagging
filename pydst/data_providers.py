# -*- coding: utf-8 -*-
"""Data providers.
This module provides classes for loading datasets and iterating over batches of
data points.
"""

import os
import numpy as np
from pydst import DEFAULT_SEED


class DataProvider(object):
    """Generic data provider."""

    def __init__(self, inputs, targets, label_map, num_tags, batch_size, max_num_batches=-1,
                 shuffle_order=True, rng=None):
        """Create a new data provider object.

        Args:
            inputs (ndarray): Array of data input features of shape
                (num_data, input_dim).
            targets (ndarray): Array of data output targets of shape
                (num_data, output_dim) or (num_data,) if output_dim == 1.
            batch_size (int): Number of data points to include in each batch.
            max_num_batches (int): Maximum number of batches to iterate over
                in an epoch. If `max_num_batches * batch_size > num_data` then
                only as many batches as the data can be split into will be
                used. If set to -1 all of the data will be used.
            shuffle_order (bool): Whether to randomly permute the order of
                the data before each epoch.
            rng (RandomState): A seeded random number generator.
        """
        self.inputs = inputs
        self.targets = targets
        if batch_size < 1:
            raise ValueError('batch_size must be >= 1')
        self._batch_size = batch_size
        if max_num_batches == 0 or max_num_batches < -1:
            raise ValueError('max_num_batches must be -1 or > 0')
        self._max_num_batches = max_num_batches
        self._update_num_batches()
        self.shuffle_order = shuffle_order
        self._current_order = np.arange(inputs.shape[0])
        if rng is None:
            rng = np.random.RandomState(DEFAULT_SEED)
        self.rng = rng
        self.new_epoch()

    @property
    def batch_size(self):
        """Number of data points to include in each batch."""
        return self._batch_size

    @batch_size.setter
    def batch_size(self, value):
        if value < 1:
            raise ValueError('batch_size must be >= 1')
        self._batch_size = value
        self._update_num_batches()

    @property
    def max_num_batches(self):
        """Maximum number of batches to iterate over in an epoch."""
        return self._max_num_batches

    @max_num_batches.setter
    def max_num_batches(self, value):
        if value == 0 or value < -1:
            raise ValueError('max_num_batches must be -1 or > 0')
        self._max_num_batches = value
        self._update_num_batches()

    def _update_num_batches(self):
        """Updates number of batches to iterate over."""
        # maximum possible number of batches is equal to number of whole times
        # batch_size divides in to the number of data points which can be
        # found using integer division
        possible_num_batches = self.inputs.shape[0] // self.batch_size
        if self.max_num_batches == -1:
            self.num_batches = possible_num_batches
        else:
            self.num_batches = min(self.max_num_batches, possible_num_batches)

    def __iter__(self):
        """Implements Python iterator interface.

        This should return an object implementing a `next` method which steps
        through a sequence returning one element at a time and raising
        `StopIteration` when at the end of the sequence. Here the object
        returned is the DataProvider itself.
        """
        return self

    def new_epoch(self):
        """Starts a new epoch (pass through data), possibly shuffling first."""
        self._curr_batch = 0
        if self.shuffle_order:
            self.shuffle()

    def reset(self):
        """Resets the provider to the initial state."""
        inv_perm = np.argsort(self._current_order)
        self._current_order = self._current_order[inv_perm]
        self.inputs = self.inputs[inv_perm]
        self.targets = self.targets[inv_perm]
        self.new_epoch()

    def shuffle(self):
        """Randomly shuffles order of data."""
        perm = self.rng.permutation(self.inputs.shape[0])
        self._current_order = self._current_order[perm]
        self.inputs = self.inputs[perm]
        self.targets = self.targets[perm]

    def next(self):
        """Returns next data batch or raises `StopIteration` if at end."""
        if self._curr_batch + 1 > self.num_batches:
            # no more batches in current iteration through data set so start
            # new epoch ready for another pass and indicate iteration is at end
            self.new_epoch()
            raise StopIteration()
        # create an index slice corresponding to current batch number
        batch_slice = slice(self._curr_batch * self.batch_size,
                            (self._curr_batch + 1) * self.batch_size)
        inputs_batch = self.inputs[batch_slice]
        targets_batch = self.targets[batch_slice]
        self._curr_batch += 1
        return inputs_batch, targets_batch

    # Python 3.x compatibility
    def __next__(self):
        return self.next()


class OneOfKDataProvider(DataProvider):
    """1-of-K classification target data provider.

    Transforms integer target labels to binary 1-of-K encoded targets.

    Derived classes must set self.num_classes appropriately.
    """

    def next(self):
        """Returns next data batch or raises `StopIteration` if at end."""
        inputs_batch, targets_batch = super(OneOfKDataProvider, self).next()
        return inputs_batch, self.to_one_of_k(targets_batch)

    def to_one_of_k(self, int_targets):
        """Converts integer coded class target to 1-of-K coded targets.

        Args:
            int_targets (ndarray): Array of integer coded class targets (i.e.
                where an integer from 0 to `num_classes` - 1 is used to
                indicate which is the correct class). This should be of shape
                (num_data,).

        Returns:
            Array of 1-of-K coded targets i.e. an array of shape
            (num_data, num_classes) where for each row all elements are equal
            to zero except for the column corresponding to the correct class
            which is equal to one.
        """
        one_of_k_targets = np.zeros((int_targets.shape[0], self.num_classes))
        one_of_k_targets[range(int_targets.shape[0]), int_targets] = 1
        return one_of_k_targets


class MGTAT_DataProvider(OneOfKDataProvider):
    # TODO: What does function do?
    """"""

    def __init__(self, which_set='train', batch_size=100, max_num_batches=-1,
                 shuffle_order=True, rng=None, num_tags=-1, root='magnatagatune/'):
        # TODO: Do the Function docstring
        """
        """

        # Check a valid which_set was provided
        assert which_set in ['train', 'valid', 'test'], (
            'Expected which_set to be either train, valid or test '
            'Got {}'.format(which_set)
        )

        # Check a valid num_tags is given
        assert num_tags == -1 or num_tags > 0, (
            'Expected num_tags to be either -1 (full) or a positive number '
            'Got {}'.format(num_tags)
        )

        # Set data path for archives
        self.which_set = which_set
        data_path = root + '{}_archive.npz'.format(self.which_set)

        # Check if file required is available
        assert os.path.isfile(data_path), (
            'Data file does not exist at expected path: ' + data_path
        )

        # load data from compressed numpy file
        loaded = np.load(data_path)
        inputs, targets = loaded['inputs'], loaded['targets']

        # flatten inputs to vectors and upcast to float32
        inputs = inputs.reshape((inputs.shape[0], -1)).astype('float32')
        # label map gives strings corresponding to integer label targets
        label_map = loaded['label_map']

        # pass the loaded data to the parent class __init__
        super(MGTAT_DataProvider, self).__init__(
            inputs, targets, label_map, num_tags, batch_size, max_num_batches, shuffle_order, rng)
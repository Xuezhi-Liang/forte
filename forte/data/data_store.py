from typing import Union, Type, List, Iterator

import uuid
from forte.data.ontology.core import EntryType
from forte.data.base_store import BaseStore


class DataStore(BaseStore):
    def __init__(self):
        """An implementation from the dataframe-like data store object.

        A DataStore object is used to store a collection of NLP entries in a piece of text.
        We store every entry in a data structure `elements`, which is a list of `entry lists`.
        Every `entry list` is a SortedList, storing the same type of entries.
        For example, subtypes of annotations, including Sentence, Documents, and Phrase, are stored in separate 
        SortedLists:
        [ <Document SortedList>, <Sentence SortedList>, ...]
        Different `entry lists` are ordered by the `type id` of the type of entries storing in this list.

        Entries are stored as `entry data` in each entry list.
        Each `entry data` in the `entry list` is represented by a list of attributes,
        e.g. [<begin>, <end>, <entry_type>, <tid>, <attr_1>, <attr_2>, ..., <attr_n>].
        
        The first four fields are compulsory for every `entry data`. They are always in the order of 
        `begin`, `end`, `entry type`, and `tid`.
        `Begin` and `end` are the begin and end character index of this entry in the text.
        `Entry type` is the type of this entry. `tid` is a unique id of every entry, usually generated by uuid.uuid4()
        Each entry type has a fixed field of attributes.
        E.g. an `entry data` with type Document has the following structure:
        [<begin>, <end>, <entry_type>, <tid>, <document_class>, <sentiment>, <classifications>]

        Different entries are sorted by the `begin` attribute of the entry. 
        If two entries have the same begin position, then we used the `end` attribute to sort them.

        Args:
            pack_name (Optional[str], optional): A name for this data store.
        """
        super().__init__()
        self._text = ""

        """
        The _type_attributes is a private dictionay that provides a mapping of entry types
        to their attribues.
        The keys are all valid ontology types, including all the
        types defined in ft.onto and ftx.onto.
        The values are all the valid attributes for this type, also defined in
        ft.onto and ftx.onto.
        This structure is supposed to be generated by another function
        get_type_attributes() and ready to use in DataStore.

        Example:
        _type_attributes = {
            "ft.onto.base_ontology.Token": ["pos", "ud_xpos", "lemma", "chunk", "ner", "sense",
                    "is_root", "ud_features", "ud_misc"],
            "ft.onto.base_ontology.Document": ["document_class", "sentiment", "classifications"],
            "ft.onto.base_ontology.Sentence": ["speaker", "part_id", "sentiment", "classification",
                        "classifications"],
        }
        TODO: implement get_type_attributes() (Issue #570)
        """
        # self._type_attributes: dict = get_type_attributes()
        self._type_attributes: dict = {}

        """
        Element is an underlying storage structure for all the entry data added by
        user in this DataStore class.
        It is a list that stores sorted `entry lists` by the order of `type id`.

            Example:
            self.elements = [
                Token SortedList(),
                Document SortedList(),
                Sentence SortedList(),
                ...
            ]
        """
        self.elements: List = []

        """
        A dictionary that keeps record of all entrys with their tid.
        It is a key-value map of {tid: entry data in list format}.

        e.g., {1423543453: [begin, end, type, tid, attr_1, ..., attr_n]}
        """
        self.entry_dict: dict = {}

    def _new_entry(self, type: str, begin, end):
        """
        generate a new entry with default fields.
        called by add_entry_raw() to create a new entry with type, begin, end.

        Args:
            type (str): type of this entry
        Returns:
            A list representing a new entry
        """

        tid: int = uuid.uuid4().int
        entry = [type, tid, begin, end]
        entry += len(self._type_attributes[type]) * [None]
        return entry
    
    def _generate_attr_index(self):
        """
        For every type in type_attributes, we need to convert the attribute list to
        a dictionary, mapping each attribute string to a unique index.
        The index should be the actual index of this attribute in the entry's list.
        Index 0, 1, 2, and 3 should be reserved for begin, end, tid and type.

        For example, for type `ft.onto.base_ontology.Sentence`, the attribute ``speaker`` 
        has index 4, and attribute ``part_id`` has index 5.

        """
        raise NotImplementedError

    def add_annotation_raw(self, type_id: int, begin: int, end: int) -> int:
        r"""This function adds an annotation entry with `begin` and `end` index
        to the sortedlist at index `type_id` of the array which records all
        sortedlists, return tid for the entry.

        Args:
            type_id (int): The index of Annotation sortedlist in the array.
            begin (int): begin index of the entry.
            end (int): end index of the entry.

        Returns:
            The tid of the entry.
        """
        # We should create the entry list with the format
        # [entry_type, tid, begin, end, None, ...].
        # A helper function _new_entry() can be used to generate a entry list
        # with default fields.
        # A reference to the entry should be store in both self.elements and
        # self.entry_dict.
        raise NotImplementedError

    def set_attr(self, tid: int, attr_name: str, attr_value):
        r"""This function locates the entry list with tid and sets its
        attribute `attr_name` with value `attr_value`.

        Args:
            tid (int): Unique id of the entry.
            attr_name (str): name of the attribute.
            attr_value: value of the attribute.

        """
        # We retrieve the entry list from entry_dict using tid. We get its
        # entry type. We then locate the index of the attribute using the entry
        # type, field dictionary and attr_name, and update the attribute.

        raise NotImplementedError

    def get_attr(self, tid: int, attr_name: str):
        r"""This function locates the entry list with tid and gets the value
        of `attr_name` of this entry.

        Args:
            tid (int): Unique id of the entry.
            attr_name (str): name of the attribute.

        Returns:
            The value of attr_name for the entry with tid.
        """
        # We retrieve the entry list from entry_dict using tid. We get its
        # entry type. We then locate the index of the attribute using the entry
        # type, field dictionary and attr_name, and get the attribute.

        raise NotImplementedError

    def delete_entry(self, tid: int):
        r"""This function locates the entry list with tid and removes it
        from the data store. It removes the entry list from both entry_dict
        and the sortedlist of its type.

        Args:
            tid (int): Unique id of the entry.

        """
        # We retrieve the entry list from entry_dict using tid. We get its
        # entry type, type id, begin and end indexes. Then, we find the
        # `entry_type` sortedlist using type id. We bisect the sortedlist
        # to find the entry list. We then remove the entry list from both
        # entry_dict and the `entry_type` sortedlist.

        raise NotImplementedError

    def get_entry(self, tid: int) -> List:
        r"""Look up the entry_dict with key `tid`.

        Args:
            tid (int): Unique id of the entry.

        Returns:
            The entry which tid corresponds to.

        """
        raise NotImplementedError

    def get(
        self, entry_type: Union[str, Type[EntryType]], **kwargs
    ) -> Iterator[List]:
        """
        Implementation of this method should provide to obtain the entries of
        type entry_type.

        Args:
            entry_type: The type of the entry to obtain.

        Returns:
            An iterator of the entries matching the provided arguments.

        """
        # We find the type id according to entry_type and locate sortedlist.
        # We create an iterator to generate entries from the sortedlist.

        raise NotImplementedError

    def next_entry(self, tid: int) -> List:
        r"""Get the next entry of the same type as the tid entry.

        Args:
            tid (int): Unique id of the entry.

        Returns:
            The next entry of the same type as the tid entry.

        """
        # We retrieve the entry list from entry_dict using tid. We can get its
        # entry type, type id, begin and end indexes from the list. 
        # Then, we find the `entry_type` sortedlist using type id. We bisect the sortedlist
        # to find the next same type entry.

        raise NotImplementedError

    def prev_entry(self, tid: int) -> List:
        r"""Get the previous entry of the same type as the tid entry.

        Args:
            tid (int): Unique id of the entry.

        Returns:
            The previous entry of the same type as the tid entry.

        """
        # We retrieve the entry list from entry_dict using tid. We get its
        # entry type, type id, begin and end indexes. Then, we find the
        # `entry_type` sortedlist using type id. We bisect the sortedlist
        # to find the next same type entry.

        raise NotImplementedError
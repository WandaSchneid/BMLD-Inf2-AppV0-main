import fsspec, posixpath
import streamlit as st
import pandas as pd
from utils.data_handler import DataHandler

class DataManager:
    """
    A singleton class for managing application data persistence and user-specific storage.
    """

    def __new__(cls, *args, **kwargs):
        """
        Implements singleton pattern by returning existing instance from session state if available.
        """
        if 'data_manager' in st.session_state:
            return st.session_state.data_manager
        else:
            instance = super(DataManager, cls).__new__(cls)
            st.session_state.data_manager = instance
            return instance

    def __init__(self, fs_protocol='file', fs_root_folder='app_data'):
        """
        Initialize the data manager with filesystem configuration.
        """
        if hasattr(self, 'fs'):  # Check if instance is already initialized
            return

        self.fs_root_folder = fs_root_folder
        self.fs = self._init_filesystem(fs_protocol)
        self.app_data_reg = {}
        self.user_data_reg = {}

    @staticmethod
    def _init_filesystem(protocol: str):
        """
        Creates and configures an fsspec filesystem instance.
        """
        if protocol == 'webdav':
            secrets = st.secrets['webdav']
            return fsspec.filesystem('webdav',
                                     base_url=secrets['base_url'],
                                     auth=(secrets['username'], secrets['password']))
        elif protocol == 'file':
            return fsspec.filesystem('file')
        else:
            raise ValueError(f"DataManager: Invalid filesystem protocol: {protocol}")

    def _get_data_handler(self, subfolder: str = None):
        """
        Creates a DataHandler instance for the specified subfolder.
        """
        if subfolder is None:
            return DataHandler(self.fs, self.fs_root_folder)
        else:
            return DataHandler(self.fs, posixpath.join(self.fs_root_folder, subfolder))

    def load_app_data(self, session_state_key, file_name, initial_value=None, **load_args):
        """
        Load application data from a file and store it in the Streamlit session state.
        """
        if session_state_key in st.session_state:
            return

        dh = self._get_data_handler()
        data = dh.load(file_name, initial_value, **load_args)
        st.session_state[session_state_key] = data
        self.app_data_reg[session_state_key] = file_name

    def load_user_data(self, session_state_key, file_name, initial_value=None, **load_args):
        """
        Load user-specific data from a file in the user's data folder.
        """
        username = st.session_state.get('username', None)
        if username is None:
            # Clear user data if no user is logged in
            for key in self.user_data_reg:
                st.session_state.pop(key, None)
            self.user_data_reg = {}
            return

        if session_state_key in st.session_state:
            return

        user_data_folder = f'user_data_{username}'
        dh = self._get_data_handler(user_data_folder)
        data = dh.load(file_name, initial_value, **load_args)
        st.session_state[session_state_key] = data
        self.user_data_reg[session_state_key] = dh.join(user_data_folder, file_name)

    @property
    def data_reg(self):
        """
        Combine app_data_reg and user_data_reg into a single dictionary.
        """
        return {**self.app_data_reg, **self.user_data_reg}

    def save_data(self, session_state_key):
        """
        Saves data from session state to persistent storage using the registered data handler.
        """
        if session_state_key not in self.data_reg:
            raise ValueError(f"DataManager: No data registered for session state key {session_state_key}")

        if session_state_key not in st.session_state:
            raise ValueError(f"DataManager: Key {session_state_key} not found in session state")

        file_path = self.data_reg[session_state_key]
        data = st.session_state[session_state_key]
        dh = self._get_data_handler(posixpath.dirname(file_path))
        dh.save(posixpath.basename(file_path), data)

    def save_all_data(self):
        """
        Saves all valid data from the session state to the persistent storage.
        """
        for key in self.data_reg.keys():
            if key in st.session_state:
                self.save_data(key)

    def append_record(self, session_state_key, record_dict):
        """
        Append a new record to a value stored in the session state.
        """
        if session_state_key not in st.session_state:
            raise ValueError(f"DataManager: Key {session_state_key} not found in session state")

        data_value = st.session_state[session_state_key]

        if not isinstance(record_dict, dict):
            raise ValueError(f"DataManager: The record_dict must be a dictionary")

        if isinstance(data_value, pd.DataFrame):
            data_value = pd.concat([data_value, pd.DataFrame([record_dict])], ignore_index=True)
        elif isinstance(data_value, list):
            data_value.append(record_dict)
        else:
            raise ValueError(f"DataManager: The session state value for key {session_state_key} must be a DataFrame or a list")

        st.session_state[session_state_key] = data_value
        self.save_data(session_state_key)
import io
import os
import re

from contextlib import contextmanager

from dodoware.pylib.proc._stream_settings import StreamSettings
from dodoware.pylib.proc._process_thread import ProcessThread


class StreamHandler(ProcessThread):
    """
    This class is used to read data from a stream, and handle the data,
    as specified in a `StreamSettings` object.
    """

    def __init__(self, stream: io.BufferedReader, settings: StreamSettings):
        """
        Args:
            stream (io.BufferedReader):
                The stream.
            settings (StreamSettings):
                Stream settings.
        """

        super().__init__()

        self._stream = stream

        self.settings = settings

        self._stash = io.BytesIO() if self.settings.max_stash_kb > 0 else None

        self._stash_bytes_remaining = self.settings.max_stash_kb * 1024

    def get_bytes(self) -> bytes:
        """
        Get the contents of the stash buffer as a `bytes` object.

        Returns:
            bytes:
                The content of the stash buffer, or `None` if the
                stash was not enabled.
        """

        with self.rlock():
            return self._stash.getvalue() if self._stash else None

    def get_text(self) -> str:
        """
        Decode the contents of the stash buffer into a string.

        Returns:
            str:
                The contents of the stash buffer decoded into a string,
                or `None` if the stash was not enabled.
        """
        data = self.get_bytes()

        if data is None:
            return None

        return str(data, "UTF-8")

    def get_lines(self) -> str:
        """
        Decode the contents of the stash buffer into a list of output lines.

        Returns:
            List[str]:
                A list of output lines, or `None` if the stash was not enabled.
        """
        text = self.get_text()

        if text is None:
            return None

        if not text:
            return []

        return re.split("\r?\n", text)

    @contextmanager
    def _open_output_file(self) -> None:
        """
        Create a context with the output file open then yield the output
        file stream to the caller.
        """

        if not self.settings.outfile:
            yield None
            return

        if not self.settings.overwrite:
            if os.path.exists(self.settings.outfile):
                raise FileExistsError(f"outfile exists: {self.settings.outfile}")

        with open(self.settings.outfile, mode="wb") as outfile_stream:
            yield outfile_stream

    def _run_ex(self):
        """
        Read and process stream data as specified in the settings until
        EOF is reached.
        """
        with self._open_output_file() as output:

            while True:

                data = self._stream.readline(self.settings.read_bytes)

                if not data:
                    break

                if output:
                    output.write(data)

                if self._stash and self._stash_bytes_remaining > 0:
                    with self.rlock():
                        self._stash.write(data)
                        self._stash_bytes_remaining -= len(data)

                if self.settings.logger:
                    self.settings.logger.log(
                        self.settings.log_level,
                        "%s%s",
                        self.settings.log_prefix,
                        str(data, encoding="UTF-8").rstrip(),
                    )

import os
import numpy as np
import threading


class V4L2Output:
    def __init__(self, device="/dev/video10"):
        self.device = device
        self.fd = None
        self.lock = threading.Lock()
        self._enabled = False
        self.width = 640
        self.height = 480

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, val):
        if val and not self._enabled:
            self._open()
        elif not val and self._enabled:
            self._close()
        self._enabled = val

    def _open(self):
        try:
            self.fd = os.open(self.device, os.O_WRONLY)
            return True
        except OSError as e:
            self.fd = None
            return False

    def _close(self):
        with self.lock:
            if self.fd is not None:
                try:
                    os.close(self.fd)
                except OSError:
                    pass
                self.fd = None

    def write_frame(self, frame: np.ndarray):
        if not self._enabled or self.fd is None:
            return False
        h, w = frame.shape[:2]
        if frame.dtype != np.uint8:
            frame = np.clip(frame * 255, 0, 255).astype(np.uint8)
        if frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        with self.lock:
            try:
                os.write(self.fd, frame.tobytes())
                return True
            except OSError:
                self._close()
                return False

    def release(self):
        self._close()

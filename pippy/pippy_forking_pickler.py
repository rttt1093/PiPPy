import copyreg
import cloudpickle


class PiPPyForkingPickler(cloudpickle.Pickler):
    """Pickler subclass used by multiprocessing."""
    _extra_reducers = {}
    _copyreg_dispatch_table = copyreg.dispatch_table

    def __init__(self, *args):
        super().__init__(*args)
        self.dispatch_table = self._copyreg_dispatch_table.copy()
        self.dispatch_table.update(self._extra_reducers)

    @classmethod
    def register(cls, type, reduce):
        """Register a reduce function for a type."""
        cls._extra_reducers[type] = reduce

    @classmethod
    def dumps(cls, obj, protocol=None):
        return cloudpickle.dumps(obj, protocol)

    loads = cloudpickle.loads

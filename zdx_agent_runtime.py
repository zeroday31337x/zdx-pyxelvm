"""Registry-driven runtime for standard and spatial PyxelVM execution."""

from pyxel_registry import PyxelRegistry


class ZDXAgentRuntime:
    """Run registered VM programs and optionally persist execution state."""

    def __init__(self, registry: PyxelRegistry):
        self.registry = registry

    def _memory(self):
        try:
            return self.registry.get("memory")
        except KeyError:
            return None

    def _persist_state(self, vm, mem, *, spatial_layout=None):
        if mem is None:
            return
        mem.remember("shared_state", dict(vm.shared))
        mem.remember("register_state", {k: dict(v) for k, v in vm.registers.items()})
        if spatial_layout is not None:
            payload = spatial_layout.to_dict() if hasattr(spatial_layout, "to_dict") else spatial_layout
            mem.remember("spatial_layout", payload)

    def run(self, image_path: str) -> dict:
        vm = self.registry.get("vm")
        mem = self._memory()
        vm.execute_texture(image_path)
        self._persist_state(vm, mem)
        return vm.registers

    def run_spatial(self, image_path: str) -> dict:
        """Execute one spatial PNG without reconstructing source or bytecode.

        The registered VM must provide ``execute_spatial`` and a ``layout``
        geometry contract.  X/Y remains the implicit address/topology and RGB
        remains the executable/data cell representation.
        """
        vm = self.registry.get("vm")
        if not hasattr(vm, "execute_spatial"):
            raise TypeError("registered VM does not support spatial PNG execution")
        mem = self._memory()
        vm.execute_spatial(image_path)
        self._persist_state(vm, mem, spatial_layout=getattr(vm, "layout", None))
        return vm.registers


if __name__ == "__main__":
    from zdx_parallel_vm import ParallelPyxelVM, SimpleCompiler
    from zdx_pixel_memory import ZDXAgentMemory
    import tempfile
    import os

    compiler = SimpleCompiler()
    prog = [["SET_A 10", "SET_B 5", "ADD", "COPY_OUT", "STORE_MEM 0", "HALT"]]
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp.close()
    compiler.compile(prog, tmp.name)

    registry = PyxelRegistry()
    registry.register("vm", ParallelPyxelVM(threads=1))
    registry.register("memory", ZDXAgentMemory(agent_id="example_agent"))
    runtime = ZDXAgentRuntime(registry)
    print("registers:", runtime.run(tmp.name))
    os.unlink(tmp.name)

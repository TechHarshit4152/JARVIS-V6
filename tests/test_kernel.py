from jarvis_v6.core.kernel import kernel


def test_kernel_boot_and_shutdown():
    kernel.boot()
    kernel.shutdown()
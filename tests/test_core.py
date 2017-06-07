import pytest

from PyBuild.core.actions import *

def test_register():
    def foo():
        pass

    register_action(foo, "foo", [])
    assert "foo" in ACTIONS
    assert ACTIONS["foo"][0] == foo
    
    with pytest.raises(AssertionError):
        register_action(foo, "foo", [])

    unregister_action("foo")
    assert "foo" not in ACTIONS

    with pytest.raises(AssertionError):
        unregister_action("foo")


def test_action():
    @action("test", [])
    def foo():
        return 1

    assert "test" in ACTIONS
    assert len(ACTIONS["test"][1]) == 0
    assert ACTIONS["test"][0]() == 1


def test_execute_action():
    executed = False

    def foo(val):
        assert val == 5
        nonlocal executed
        executed = True

    register_action(foo, "foo", [(["--val"], {"action": "store", "type": int})])
    execute_action("foo", ["--val", "5"])

    assert executed
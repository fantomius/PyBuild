"""Base code for all build-actions in system"""

import argparse


# ACTIONS - global dict for all actions
ACTIONS = {}


def register_action(function, name, arguments):
    """
    Register function as build-action with name and commandline args
    """
    reg_name = name.lower()

    assert reg_name not in ACTIONS, "Action {} already registered".format(reg_name)
    ACTIONS[reg_name] = (function, arguments)


def unregister_action(name):
    """
    Unregister build-action with name
    """
    reg_name = name.lower()
    assert reg_name in ACTIONS, "Action {} not registered".format(reg_name)
    del ACTIONS[reg_name]


def action(name, arguments):
    """
    Decorator for registering action
    """
    def inner(func):
        register_action(func, name, arguments)
        return func

    return inner


def execute_action(name, arguments):
    """
    Base code for executing action
    Trying to search code in ACTIONS dict, process arguments with argparse and executes it
    """
    call_name = name.lower()
    assert call_name in ACTIONS, "Action not registered: {}".format(call_name)

    call_func, call_arguments = ACTIONS[call_name]
    parser = argparse.ArgumentParser(description="Arguments for command {}".format(call_name))
    for arg in call_arguments:
        parser.add_argument(*arg[0], **arg[1])
    args = parser.parse_args(arguments)

    call_func(**vars(args))





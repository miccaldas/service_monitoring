"""
Starts and orchestrates all functions in the app.
"""
# import snoop
# from snoop import pp

from dropdown import dropdown
from systemd_methods import Answers


# def type_watch(source, value):
#     return f"type({source})", type(value)


# snoop.install(watch_extras=[type_watch])


# @snoop
def attrlst(ans, action):
    """
    Creates 'actionmethod' if there's just one action.
    """
    for i in action:
        actionmethod = getattr(ans, i)
        actionmethod()


# @snoop
def attrstr(ans, action):
    """
    Creates 'actionmethod' if there's a list of actions.
    """
    actionmethod = getattr(ans, action)
    actionmethod()


# @snoop
def main():
    """
    With the information taken from the 'dropdown' function
    , ['service_name', 'action_name'], I call the 'Answer'
    class in 'systemd_methods', choosing one of its methods.
    """
    # 'dropdown' is a function who shows two 'Questionary' dropdowns: one for choosing a service
    # another to choose an action. It returns these bits of information in a tuple.
    drop = dropdown()
    # 'Answers()' is the class that houses all the action's methods. It has one argument, the name
    # of the service.
    ans = Answers(drop[0])
    # The getattr() function returns the value of the specified attribute from the specified object.
    if type(drop[1]) is list:
        attrlst(ans, drop[1])
    else:
        attrstr(ans, drop[1])


if __name__ == "__main__":
    main()

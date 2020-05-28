from message_handlers import orders, start, users
import permission_list

COMMANDS_LIST = (
    orders.NewOrderHandler(),
    users.AddUserHandler(),
    users.GetUsersHandler(),
    users.DeleteUserHandler(),
    users.AdminChangeUserHandler(),
)

PERMISSIONS_LIST = (
    permission_list.isAdmin,
    permission_list.isCustomer,
)

from message_handlers import orders, start, users
import permission_list

COMMANDS_LIST = (
    start.StartHandler(),
    start.StartAdminHandler(),
    orders.NewOrderHandler(),
    orders.AddOrderHandler(),
    users.AddUserHandler(),
    users.GetUsersHandler(),
    users.DeleteUserHandler(),
    users.AdminChangeUserHandler(),
)

PERMISSIONS_LIST = (
    permission_list.isAdmin,
    permission_list.isCustomer,
    permission_list.isManager,
    permission_list.hasPayload,
)

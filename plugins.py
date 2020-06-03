from message_handlers import orders, start, users
import permission_list

COMMANDS_LIST = (
    start.StartHandler(),
    start.StartAdminHandler(),
    orders.NewOrderHandler(),
    orders.AddOrderHandler(),
    orders.AcceptOrderHandler(),
    users.AddUserHandler(),
    users.GetUsersHandler(),
    users.DeleteUserHandler(),
    users.AdminChangeUserHandler(),
)
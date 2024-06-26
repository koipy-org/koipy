from bot.queue.message import MessageDeleteQueue, MessageEditQueue
from bot.queue.handler import HandlerQueue


__all__ = [
    "MessageEditQueue",
    "MessageDeleteQueue",
    "HandlerQueue",
    "message_delete_queue",
    "message_edit_queue",
    "handler_delete_queue"
]


message_delete_queue = MessageDeleteQueue()
message_edit_queue = MessageEditQueue()
handler_delete_queue = HandlerQueue()
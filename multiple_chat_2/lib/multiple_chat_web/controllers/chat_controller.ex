defmodule MultipleChatWeb.ChatController do
  use MultipleChatWeb, :controller

  alias MultipleChat.Chats

  def show(conn, %{"id" => room}) do
    messages = Chats.list_messages_by_room(room)
    render(conn, "show.html", room: room, messages: messages)
  end
end

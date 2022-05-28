defmodule MultipleChatWeb.PageController do
  use MultipleChatWeb, :controller

  def index(conn, _params) do
    render(conn, "index.html")
  end

  def message(conn,params) do
    IO.puts(Map.get(params, "room"))
    msgs = MultipleChat.Chats.list_messages_by_room(Map.get(params, "room"))
    json(conn, %{messages: msgs})
  end


end

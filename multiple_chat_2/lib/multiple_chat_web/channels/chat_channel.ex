defmodule MultipleChatWeb.ChatChannel do
  use MultipleChatWeb, :channel

  alias MultipleChat.Chats

  def join("chat:" <> _room, payload, socket) do
    send(self(), {:after_join, payload} )
    {:ok, socket}
  end

  def handle_info({:after_join, payload}, socket) do
    broadcast socket, "shout", %{new_user: payload}
    {:noreply, socket}
  end
  @spec handle_in(<<_::40>>, map, Phoenix.Socket.t()) :: {:noreply, Phoenix.Socket.t()}
  def handle_in("shout", payload, socket) do
    "chat:" <> room = socket.topic
    payload = Map.merge(payload, %{"room" => room})
    Chats.create_message(payload)
    broadcast socket, "shout", payload
    {:noreply, socket}
  end

end

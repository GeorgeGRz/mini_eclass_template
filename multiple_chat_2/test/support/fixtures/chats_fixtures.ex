defmodule MultipleChat.ChatsFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `MultipleChat.Chats` context.
  """

  @doc """
  Generate a message.
  """
  def message_fixture(attrs \\ %{}) do
    {:ok, message} =
      attrs
      |> Enum.into(%{
        body: "some body",
        name: "some name",
        room: "some room"
      })
      |> MultipleChat.Chats.create_message()

    message
  end
end

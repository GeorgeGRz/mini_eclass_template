defmodule MultipleChat.Chats.Message do
  use Ecto.Schema
  import Ecto.Changeset

  @derive {Jason.Encoder, only: [:body,:name,:room,:inserted_at]}
  schema "messages" do
    field :body, :string
    field :name, :string
    field :room, :string

    timestamps()
  end

  @doc false
  def changeset(message, attrs) do
    message
    |> cast(attrs, [:name, :body, :room])
    |> validate_required([:name, :body, :room])
  end
end

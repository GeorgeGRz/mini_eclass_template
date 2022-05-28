import Config

# Configure your database
#
# The MIX_TEST_PARTITION environment variable can be used
# to provide built-in test partitioning in CI environment.
# Run `mix help test` for more information.
config :multiple_chat, MultipleChat.Repo,
  username: "postgres",
  password: "postgres",
  database: "multiple_chat_test#{System.get_env("MIX_TEST_PARTITION")}",
  hostname: "localhost",
  pool: Ecto.Adapters.SQL.Sandbox,
  pool_size: 10

# We don't run a server during test. If one is required,
# you can enable the server option below.
config :multiple_chat, MultipleChatWeb.Endpoint,
  http: [ip: {127, 0, 0, 1}, port: 4002],
  secret_key_base: "3pQ4sVTI8Q4UKXIdeiMnu9zQg/cpLH08IcfCOuqQ+1tumdjPkaSah4tvjQKk0pj4",
  server: false

# In test we don't send emails.
config :multiple_chat, MultipleChat.Mailer, adapter: Swoosh.Adapters.Test

# Print only warnings and errors during test
config :logger, level: :warn

# Initialize plugs at runtime for faster test compilation
config :phoenix, :plug_init_mode, :runtime

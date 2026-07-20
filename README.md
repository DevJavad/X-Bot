# Install &‌ Initialization & Run

### Clone the repository:
```bash
git clone https://github.com/DevJavad/X-Bot.git
```

### Go to project directory:
```bash
cd X-Bot/src
```

### Install dependencies:
```bash
pip install -r app/requirements.txt
```

### Create environment file:
```bash
cp app/.env.example app/.env
```

### Edit your configuration:
```bash
nano app/.env
```

### Run the bot:
```bash
python -m app.main
```


# Environment Variables

| Variable | Description | Required |
|---|---|---|
| `BOT__TOKEN` | Telegram Bot API token | ✅ |
| `BOT__OWNER_ID` | Telegram user ID of bot owner | ✅ |
| `BOT__CHANNEL_USERNAME` | Telegram channel username for membership verification | ✅ |
| | | |
| `XUI__HOST` | X-UI panel hostname or IP address | ✅ |
| `XUI__PORT` | X-UI panel port | ✅ |
| `XUI__PATH` | X-UI panel API path | ✅ |
| `XUI__TOKEN` | X-UI authentication token | ✅ |
| `XUI__SUBSCRIPTION_PORT` | Subscription URL server port | ✅ |
| `XUI__SUBSCRIPTION_PATH` | Subscription URL path | ✅ |
| `XUI__SUBSCRIPTION_HOST` | Subscription URL hostname | ✅ |
| | | |
| `PAYMENT__CARD_NUMBER` | Payment card number for manual payments | ✅ |
| | | |
| `DATABASE__NAME` | Database name | ✅ |
| `DATABASE__HOST` | Database host address | ✅ |
| `DATABASE__PORT` | Database port | ✅ |
| `DATABASE__USERNAME` | Database username | ✅ |
| `DATABASE__PASSWORD` | Database password | ✅ |
| | | |
| `REDIS__HOST` | Redis server host | ❌ |
| `REDIS__PORT` | Redis server port | ❌ |
| | | |
| `LOGGER__LEVEL` | Application logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) | ❌ |
| `LOGGER__ENABLED` | Enable or disable application logging | ❌ |
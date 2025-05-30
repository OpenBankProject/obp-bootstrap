### Usage:

### Requirements

- OBP-API backend instance at OBP_BASE_URL
- Keycloak Identity Provider instance KEYCLOAK_URL

**Directory structure:**

```
bash/
├── create_user.sh
├── create_consumer.sh
├── input.env
└── output.env
```

**Run it like:**

```bash
cd bash
chmod +x create_user.sh
./create_user.sh                     # Auto-loads .env or input.env
./create_user.sh --env-file=my.env   # Loads my.env explicitly

chmod +x create_user.sh
./create_consumer.sh                     # Auto-loads .env or input.env
./create_consumer.sh --env-file=my.env   # Loads my.env explicitly
```